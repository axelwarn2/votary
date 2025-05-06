from fastapi import APIRouter, WebSocket
from vosk import Model, KaldiRecognizer
import subprocess
import json
import os
import logging

router = APIRouter()

# Путь к новой модели
MODEL_PATH = "/app/backend/config/vosk-model-small-ru-0.22"
TRANSCRIPTION_FILE = "/app/transcription.txt"

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Проверка существования модели
if not os.path.exists(MODEL_PATH):
    logger.error(f"Model path does not exist: {MODEL_PATH}")
    raise FileNotFoundError(f"Model path does not exist: {MODEL_PATH}")

@router.websocket("/record")
async def record_audio(websocket: WebSocket):
    await websocket.accept()
    logger.info("WebSocket connection established")
    # Отправляем подтверждение клиенту
    await websocket.send_json({"status": "connected"})

    # Загрузка модели Vosk
    model = Model(MODEL_PATH)
    recognizer = KaldiRecognizer(model, 16000)

    # Запуск FFmpeg для преобразования WebM в PCM16LE mono@16k
    process = subprocess.Popen(
        [
            "ffmpeg", "-loglevel", "quiet", "-i", "pipe:0",
            "-f", "s16le", "-acodec", "pcm_s16le", "-ac", "1", "-ar", "16000", "pipe:1"
        ],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    try:
        while True:
            msg = await websocket.receive()
            # Проверка на закрытие соединения клиентом
            if msg.get("type") == "websocket.disconnect":
                logger.info("WebSocket disconnected by client")
                break

            data = msg.get("bytes")
            if not data:
                continue  # Пропускаем, если данных нет

            # Логируем размер полученного аудиофрагмента
            logger.info("Received audio chunk of size: %d bytes", len(data))

            # Передача данных в FFmpeg
            process.stdin.write(data)
            process.stdin.flush()

            # Чтение PCM-данных от FFmpeg
            pcm = process.stdout.read(4096)
            if not pcm:
                continue

            # Логируем размер PCM-данных
            logger.info("Processed PCM chunk of size: %d bytes", len(pcm))

            # Распознавание речи
            if recognizer.AcceptWaveform(pcm):
                res = json.loads(recognizer.Result())
                text = res.get("text", "").strip()
                if text:
                    logger.info("Recognized text: %s", text)
                    # Отправка финального текста клиенту
                    await websocket.send_json({"text": text})
                    # Запись в файл
                    with open(TRANSCRIPTION_FILE, "a", encoding="utf-8") as f:
                        f.write(text + "\n")
            else:
                partial = json.loads(recognizer.PartialResult()).get("partial", "").strip()
                if partial:
                    logger.info("Partial text: %s", partial)
                    await websocket.send_json({"partial": partial})

    except Exception as e:
        logger.error(f"WebSocket handler error: {e}")
        try:
            await websocket.send_json({"error": str(e)})
        except:
            pass

    finally:
        logger.info("Shutting down FFmpeg and closing WebSocket")
        process.kill()
        try:
            await websocket.close()
        except:
            pass