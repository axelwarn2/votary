from fastapi import APIRouter, WebSocket, Depends, WebSocketException, Query
from sqlalchemy.orm import Session
import subprocess
import json
import os
import logging
import whisper
import asyncio
from pydub import AudioSegment
from datetime import datetime, timedelta
from backend.utlis.db import get_db
from backend.models.EmployeeModel import EmployeeModel
from backend.models.MeetingModel import MeetingModel
from backend.models.TaskModel import TaskModel, StatusEnum
from backend.services.AuthService import get_current_user_from_session

router = APIRouter()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TEMP_AUDIO_PATH = "/app/temp_audio_{}.webm"
UPLOAD_DIR = "/app/backend/upload"
FRAGMENT_DURATION = 30
TRANSCRIPTION_FILE = "/app/transcription.txt"

STOP_WORDS = {"стоп", "stop", "стап", "стоб"}

if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

@router.websocket("/record")
async def record_audio(websocket: WebSocket, session_id: str = Query(...), db: Session = Depends(get_db)):
    await websocket.accept()
    logger.info("WebSocket connection established")

    try:
        session = get_current_user_from_session(session_id)
    except Exception as e:
        await websocket.send_json({"error": str(e)})
        await websocket.close()
        logger.error("Unauthorized WebSocket connection attempt: %s", str(e))
        return

    if session.get("role") != "руководитель":
        await websocket.send_json({"error": "Unauthorized: Only leaders can record meetings"})
        await websocket.close()
        logger.error("Unauthorized WebSocket connection attempt: not a leader")
        return

    leader_id = session["id"]
    await websocket.send_json({"status": "connected"})

    employees = db.query(EmployeeModel).all()
    employee_names = [(e.surname.lower(), e.name.lower(), e.id) for e in employees]
    logger.info("Loaded %d employees: %s", len(employees), employee_names)

    full_text = []
    tasks = []
    fragment_index = 0
    start_time = None
    end_time = None
    audio_file = None
    current_audio_path = None
    final_audio_path = None

    try:
        while True:
            if not audio_file:
                current_audio_path = TEMP_AUDIO_PATH.format(fragment_index)
                audio_file = open(current_audio_path, "wb")
                logger.info("Opened new audio fragment: %s", current_audio_path)

            current_time = asyncio.get_event_loop().time()
            if start_time and (current_time - datetime.fromisoformat(start_time).timestamp() >= FRAGMENT_DURATION):
                if audio_file:
                    audio_file.close()
                    audio_file = None
                    text, wav_path = await process_audio_fragment(current_audio_path, db, employee_names, tasks, full_text, websocket, leader_id, start_time)
                    if text:
                        full_text.append(text)
                    fragment_index += 1
                    current_audio_path = None
                    final_audio_path = wav_path

            try:
                msg = await asyncio.wait_for(websocket.receive(), timeout=600)
                if msg.get("type") == "websocket.disconnect":
                    logger.info("WebSocket disconnected by client")
                    break

                if msg.get("text"):
                    data = json.loads(msg["text"])
                    if data.get("type") == "start" and data.get("time_start"):
                        start_time = data["time_start"]
                        logger.info("Received start_time: %s", start_time)
                    elif data.get("type") == "stop" and data.get("time_end"):
                        end_time = data["time_end"]
                        logger.info("Received end_time: %s", end_time)
                        if audio_file:
                            audio_file.close()
                            audio_file = None
                        break
                    elif data.get("type") == "ping":
                        logger.info("Received ping")
                        continue

                data = msg.get("bytes")
                if data:
                    logger.info("Received audio chunk of size: %d bytes", len(data))
                    audio_file.write(data)
                    audio_file.flush()

            except asyncio.TimeoutError:
                logger.info("WebSocket receive timeout, closing connection")
                break

    except Exception as e:
        logger.error("WebSocket handler error: %s", str(e))
        if websocket.state == 1:
            await websocket.send_json({"error": str(e)})
            logger.info("Sent error message to client")

    finally:
        if audio_file:
            audio_file.close()
            audio_file = None

        if current_audio_path and os.path.exists(current_audio_path):
            logger.info("Processing final audio fragment: %s, size: %d bytes", current_audio_path, os.path.getsize(current_audio_path))
            text, wav_path = await process_audio_fragment(current_audio_path, db, employee_names, tasks, full_text, websocket, leader_id, start_time)
            if text:
                full_text.append(text)
            else:
                logger.warning("No text transcribed for final fragment")
            final_audio_path = wav_path

        meeting_text = " ".join(full_text)
        if meeting_text and start_time and end_time:
            try:
                start_dt = datetime.fromisoformat(start_time.replace('Z', '+00:00'))
                end_dt = datetime.fromisoformat(end_time.replace('Z', '+00:00'))
                meeting = MeetingModel(
                    date_event=start_dt,
                    time_start=start_dt.time(),
                    time_end=end_dt.time(),
                    text=meeting_text,
                    audio_path=final_audio_path
                )
                db.add(meeting)
                db.commit()
                db.refresh(meeting)
                logger.info("Saved meeting with ID %d, start_time: %s, end_time: %s, audio_path: %s", meeting.id, start_time, end_time, final_audio_path)
            except ValueError as e:
                logger.error("Error parsing timestamps: %s", str(e))
                await websocket.send_json({"error": "Invalid timestamp format"})
                return

            for task in tasks:
                db_task = TaskModel(
                    date_created=datetime.now(),
                    deadline=datetime.now() + timedelta(days=7),
                    description=task["description"],
                    status=StatusEnum.выполняется,
                    employee_id=task["employee_id"],
                    meeting_id=meeting.id,
                    leader_id=leader_id
                )
                db.add(db_task)
            db.commit()
            logger.info("Saved %d tasks", len(tasks))

            with open(TRANSCRIPTION_FILE, "a", encoding="utf-8") as f:
                f.write(meeting_text + "\n")

        logger.info("Cleaning up temporary files")
        for i in range(fragment_index + 1):
            temp_path = TEMP_AUDIO_PATH.format(i)
            wav_path = temp_path.replace(".webm", ".wav")
            if os.path.exists(temp_path):
                os.remove(temp_path)
            if os.path.exists(wav_path) and wav_path != final_audio_path:
                os.remove(wav_path)

        if websocket.state == 1:
            await websocket.close()
            logger.info("WebSocket closed by server")

async def process_audio_fragment(audio_path: str, db: Session, employee_names: list, tasks: list, full_text: list, websocket: WebSocket, leader_id: int, start_time: str = None):
    wav_path = audio_path.replace(".webm", ".wav")
    final_wav_path = None
    try:
        logger.info("Converting audio to WAV: %s, input size: %d bytes", audio_path, os.path.getsize(audio_path))
        subprocess.run(
            [
                "ffmpeg", "-y", "-loglevel", "quiet", "-i", audio_path,
                "-f", "wav", "-acodec", "pcm_s16le", "-ac", "1", "-ar", "44100", wav_path
            ],
            check=True
        )
        logger.info("Audio converted to WAV: %s", wav_path)

        try:
            audio = AudioSegment.from_wav(wav_path)
            audio = audio.normalize().apply_gain(+5.0)
            audio = audio.low_pass_filter(3000).high_pass_filter(300)
            audio.export(wav_path, format="wav")
            logger.info("Audio processed with pydub")
        except Exception as e:
            logger.error("Pydub processing error: %s", str(e))

        if start_time:
            try:
                start_dt = datetime.fromisoformat(start_time.replace('Z', '+00:00'))
                file_name = f"Собрание от {start_dt.strftime('%Y-%m-%d %H-%M-%S')}.wav"
                final_wav_path = os.path.join(UPLOAD_DIR, file_name)
                os.rename(wav_path, final_wav_path)
                logger.info("Moved WAV file to: %s", final_wav_path)
            except Exception as e:
                logger.error("Error moving WAV file: %s", str(e))
                final_wav_path = None

        model = whisper.load_model("small")
        result = model.transcribe(wav_path if not final_wav_path else final_wav_path, language="ru", fp16=False, temperature=0.0)
        text = result["text"].strip()
        logger.info("Recognized text: %s", text)

        if text:
            text_lower = text.lower()
            logger.info("Processing text_lower: %s", text_lower)

            sentences = []
            current_sentence = []
            words = text.split()
            for word in words:
                current_sentence.append(word)
                if word.lower() in STOP_WORDS:
                    sentences.append(" ".join(current_sentence))
                    current_sentence = []
            if current_sentence:
                sentences.append(" ".join(current_sentence))

            logger.info("Split into sentences: %s", sentences)

            for sentence in sentences:
                sentence_lower = sentence.lower()
                logger.info("Processing sentence: %s", sentence)
                for surname, name, emp_id in employee_names:
                    if surname in sentence_lower or name in sentence_lower:
                        logger.info("Found employee: surname=%s, name=%s, emp_id=%d", surname, name, emp_id)
                        surname_index = sentence_lower.find(surname) if surname in sentence_lower else len(sentence_lower)
                        name_index = sentence_lower.find(name) if name in sentence_lower else len(sentence_lower)
                        start_index = min(surname_index, name_index)
                        if start_index == len(sentence_lower):
                            logger.warning("Name found but indices invalid for emp_id=%d", emp_id)
                            continue
                        task_text = sentence[start_index:]
                        task_text_lower = task_text.lower()
                        stop_indices = [task_text_lower.find(stop_word) for stop_word in STOP_WORDS if stop_word in task_text_lower]
                        if stop_indices:
                            stop_index = min(i for i in stop_indices if i >= 0)
                            task_text = task_text[:stop_index].strip()
                        if task_text:
                            task = {
                                "employee_id": emp_id,
                                "description": task_text,
                                "leader_id": leader_id
                            }
                            tasks.append(task)
                            logger.info("Task created for employee ID %d: %s, leader_id=%d", emp_id, task_text, leader_id)
                        else:
                            logger.warning("Task text is empty for employee ID %d", emp_id)

        return text, final_wav_path

    except subprocess.CalledProcessError as e:
        logger.error("FFmpeg conversion error: %s", str(e))
        if websocket.state == 1:
            await websocket.send_json({"error": "Failed to convert audio"})
            logger.info("Sent FFmpeg error to client")
        return "", None
    except Exception as e:
        logger.error("Whisper transcription error: %s", str(e))
        if websocket.state == 1:
            await websocket.send_json({"error": str(e)})
            logger.info("Sent Whisper error to client")
        return "", None
    