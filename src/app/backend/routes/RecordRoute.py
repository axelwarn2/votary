from fastapi import APIRouter, WebSocket, Depends
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

router = APIRouter()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TEMP_AUDIO_PATH = "/app/temp_audio_{}.webm"
FRAGMENT_DURATION = 30
TRANSCRIPTION_FILE = "/app/transcription.txt"

STOP_WORDS = {"стоп", "stop", "стап", "стоб"}

@router.websocket("/record")
async def record_audio(websocket: WebSocket, db: Session = Depends(get_db)):
    await websocket.accept()
    logger.info("WebSocket connection established")
    await websocket.send_json({"status": "connected"})

    employees = db.query(EmployeeModel).all()
    employee_names = [(e.surname.lower(), e.name.lower(), e.id) for e in employees]
    logger.info("Loaded %d employees: %s", len(employees), employee_names)

    full_text = []
    tasks = []
    fragment_index = 0
    start_time = datetime.now()
    audio_file = None

    try:
        while True:
            if audio_file is None:
                audio_path = TEMP_AUDIO_PATH.format(fragment_index)
                audio_file = open(audio_path, "wb")
                logger.info("Opened new audio fragment: %s", audio_path)

            current_time = asyncio.get_event_loop().time()
            if current_time - start_time.timestamp() >= FRAGMENT_DURATION:
                if audio_file:
                    audio_file.close()
                    audio_file = None
                    text = await process_audio_fragment(audio_path, db, employee_names, tasks, full_text, websocket)
                    if text:
                        full_text.append(text)
                    fragment_index += 1
                    start_time = datetime.now()

            try:
                msg = await asyncio.wait_for(websocket.receive(), timeout=600)  # 10 минут
                if msg.get("type") == "websocket.disconnect":
                    logger.info("WebSocket disconnected by client")
                    break

                data = msg.get("bytes")
                if not data:
                    continue

                logger.info("Received audio chunk of size: %d bytes", len(data))
                audio_file.write(data)
                audio_file.flush()

            except asyncio.TimeoutError:
                logger.info("WebSocket receive timeout, closing connection")
                break

    except Exception as e:
        logger.error(f"WebSocket handler error: %s", str(e))
        if websocket.state == 1:
            await websocket.send_json({"error": str(e)})
            logger.info("Sent error message to client")

    finally:
        if audio_file:
            audio_file.close()
            text = await process_audio_fragment(audio_path, db, employee_names, tasks, full_text, websocket)
            if text:
                full_text.append(text)

        meeting_text = " ".join(full_text)
        if meeting_text:
            end_time = datetime.now()
            meeting = MeetingModel(
                date_event=start_time,
                time_start=start_time.time(),
                time_end=end_time.time(),
                text=meeting_text
            )
            db.add(meeting)
            db.commit()
            db.refresh(meeting)
            logger.info("Saved meeting with ID %d", meeting.id)

            for task in tasks:
                db_task = TaskModel(
                    date_created=datetime.now(),
                    deadline=datetime.now() + timedelta(days=7),
                    description=task["description"],
                    status=StatusEnum.выполняется,
                    employee_id=task["employee_id"],
                    meeting_id=meeting.id
                )
                db.add(db_task)
            db.commit()
            logger.info("Saved %d tasks", len(tasks))

            with open(TRANSCRIPTION_FILE, "a", encoding="utf-8") as f:
                f.write(meeting_text + "\n")

        logger.info("Cleaning up temporary files")
        for i in range(fragment_index + 1):
            for path in [TEMP_AUDIO_PATH.format(i), TEMP_AUDIO_PATH.format(i).replace(".webm", ".wav")]:
                if os.path.exists(path):
                    os.remove(path)

        if websocket.state == 1:
            await websocket.close()
            logger.info("WebSocket closed by server")

async def process_audio_fragment(audio_path: str, db: Session, employee_names: list, tasks: list, full_text: list, websocket: WebSocket):
    wav_path = audio_path.replace(".webm", ".wav")
    try:
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
            logger.error(f"Pydub processing error: %s", str(e))

        model = whisper.load_model("small")
        result = model.transcribe(wav_path, language="ru", fp16=False, temperature=0.0)
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
                            task = {"employee_id": emp_id, "description": task_text}
                            tasks.append(task)
                            logger.info("Task completed for employee ID %d: %s", emp_id, task_text)
                        else:
                            logger.warning("Task text is empty for employee ID %d", emp_id)

        return text

    except subprocess.CalledProcessError as e:
        logger.error(f"FFmpeg conversion error: %s", str(e))
        if websocket.state == 1:
            await websocket.send_json({"error": "Failed to convert audio"})
            logger.info("Sent FFmpeg error to client")
        return ""
    except Exception as e:
        logger.error(f"Whisper transcription error: %s", str(e))
        if websocket.state == 1:
            await websocket.send_json({"error": str(e)})
            logger.info("Sent Whisper error to client")
        return ""