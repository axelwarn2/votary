from fastapi import APIRouter, WebSocket
import subprocess
import json
import os
import logging
import whisper
import asyncio
from pydub import AudioSegment

router = APIRouter()

# Путь для временного аудиофайла
TEMP_AUDIO_PATH = "/app/temp_audio.webm"
TRANSCRIPTION_FILE = "/app/transcription.txt"

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@router.websocket("/record")
async def record_audio(websocket: WebSocket):
    await websocket.accept()
    logger.info("WebSocket connection established")
    await websocket.send_json({"status": "connected"})

    # Создаем или очищаем временный файл для аудио
    try:
        with open(TEMP_AUDIO_PATH, "wb") as audio_file:
            timeout = 30  # Таймаут 30 секунд для ожидания данных
            last_received = asyncio.get_event_loop().time()
            while True:
                try:
                    msg = await asyncio.wait_for(websocket.receive(), timeout=timeout)
                    current_time = asyncio.get_event_loop().time()
                    if current_time - last_received > timeout:
                        logger.info("No data received for %d seconds, closing WebSocket", timeout)
                        break

                    if msg.get("type") == "websocket.disconnect":
                        logger.info("WebSocket disconnected by client")
                        break

                    data = msg.get("bytes")
                    if not data:
                        continue

                    logger.info("Received audio chunk of size: %d bytes", len(data))
                    audio_file.write(data)
                    audio_file.flush()
                    last_received = current_time

                except asyncio.TimeoutError:
                    logger.info("WebSocket receive timeout, closing connection")
                    break

    except Exception as e:
        logger.error(f"WebSocket handler error: {e}")
        if websocket.client_state == websocket.WebSocketState.CONNECTED:
            await websocket.send_json({"error": str(e)})
            logger.info("Sent error message to client")
        return

    # Конвертация WebM в WAV
    wav_path = TEMP_AUDIO_PATH.replace(".webm", ".wav")
    try:
        subprocess.run(
            [
                "ffmpeg", "-y", "-loglevel", "quiet", "-i", TEMP_AUDIO_PATH,
                "-f", "wav", "-acodec", "pcm_s16le", "-ac", "1", "-ar", "44100", wav_path
            ],
            check=True
        )
        logger.info("Audio converted to WAV")
    except subprocess.CalledProcessError as e:
        logger.error(f"FFmpeg conversion error: {e}")
        if websocket.client_state == websocket.WebSocketState.CONNECTED:
            await websocket.send_json({"error": "Failed to convert audio"})
            logger.info("Sent FFmpeg error to client")
        return

    # Обработка аудио с pydub
    try:
        audio = AudioSegment.from_wav(wav_path)
        audio = audio.normalize().apply_gain(+5.0)  # Нормализация и усиление громкости
        audio = audio.low_pass_filter(3000).high_pass_filter(300)  # Подавление шума
        audio.export(wav_path, format="wav")
        logger.info("Audio processed with pydub")
    except Exception as e:
        logger.error(f"Pydub processing error: {e}")
        # Продолжаем, даже если pydub не сработал

    # Распознавание с помощью Whisper
    try:
        model = whisper.load_model("small")  # Используем модель small
        result = model.transcribe(wav_path, language="ru", fp16=False, temperature=0.0)
        text = result["text"].strip()

        if text:
            logger.info("Recognized text: %s", text)
            # Записываем текст в файл
            with open(TRANSCRIPTION_FILE, "a", encoding="utf-8") as f:
                f.write(text + "\n")
            # Отправляем текст клиенту, если WebSocket открыт
            if websocket.client_state == websocket.WebSocketState.CONNECTED:
                await websocket.send_json({"text": text})
                logger.info("Sent text to client")
            else:
                logger.warning("WebSocket closed before sending text")
        else:
            logger.warning("No text recognized")
            if websocket.client_state == websocket.WebSocketState.CONNECTED:
                await websocket.send_json({"text": ""})
                logger.info("Sent empty text to client")

    except Exception as e:
        logger.error(f"Whisper transcription error: {e}")
        if websocket.client_state == websocket.WebSocketState.CONNECTED:
            await websocket.send_json({"error": str(e)})
            logger.info("Sent Whisper error to client")

    finally:
        # Даем фронтенду время обработать сообщение
        await asyncio.sleep(2.0)
        # Очистка временных файлов
        logger.info("Cleaning up temporary files")
        for path in [TEMP_AUDIO_PATH, wav_path]:
            if os.path.exists(path):
                os.remove(path)
        if websocket.client_state == websocket.WebSocketState.CONNECTED:
            await websocket.close()
            logger.info("WebSocket closed by server")