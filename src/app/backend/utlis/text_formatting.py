import logging
from datetime import datetime, timedelta
import dateparser
from transformers import T5ForConditionalGeneration, T5Tokenizer
from functools import lru_cache

logger = logging.getLogger(__name__)

class TextNormalizer:
    CORRECTIONS = {
        "птныца": "пятница",
        "птныцы": "пятницы",
        "четверк": "четверг",
        "четверга": "четверга",
        "среду": "среда",
        "среды": "среды",
        "понедельник": "понедельник",
        "вторник": "вторник",
        "суббота": "суббота",
        "воскресенье": "воскресенье",
        "клавтура": "клавиатура",
        "задачу": "задачу",
        "задачи": "задачи",
        "после завтра": "послезавтра",
        "после завтрака": "послезавтра",
        "следующий четверг": "в четверг",
        "следующую пятницу": "в пятницу"
    }

    TIME_EXPRESSIONS = {
        "сегодня": 0,
        "завтра": 1,
        "послезавтра": 2,
        "после завтра": 2,
        "в понедельник": lambda base: (0 - base.weekday() + 7) % 7 or 7,
        "во вторник": lambda base: (1 - base.weekday() + 7) % 7 or 7,
        "в среду": lambda base: (2 - base.weekday() + 7) % 7 or 7,
        "в четверг": lambda base: (3 - base.weekday() + 7) % 7 or 7,
        "в пятницу": lambda base: (4 - base.weekday() + 7) % 7 or 7,
        "в субботу": lambda base: (5 - base.weekday() + 7) % 7 or 7,
        "в воскресенье": lambda base: (6 - base.weekday() + 7) % 7 or 7
    }

    def __init__(self, model_name="t5-small"):
        self.model = T5ForConditionalGeneration.from_pretrained(model_name)
        self.tokenizer = T5Tokenizer.from_pretrained(model_name)
        logger.info(f"Loaded T5 model: {model_name}")

    def apply_corrections(self, text):
        """Применяет словарь исправлений к тексту."""
        text_lower = text.lower()
        for wrong, correct in self.CORRECTIONS.items():
            text_lower = text_lower.replace(wrong, correct)
        return text_lower

    @lru_cache(maxsize=1000)
    def normalize_text(self, text):
        """Исправляет ошибки в тексте с помощью T5."""
        text = self.apply_corrections(text)
        try:
            input_text = f"correct: {text}"
            inputs = self.tokenizer(input_text, return_tensors="pt", max_length=512, truncation=True)
            outputs = self.model.generate(
                inputs["input_ids"],
                max_length=512,
                num_beams=4,
                early_stopping=True
            )
            corrected_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            logger.info(f"Normalized text: '{text}' -> '{corrected_text}'")
            return corrected_text
        except Exception as e:
            logger.warning(f"T5 normalization failed: {str(e)}, returning original text")
            return text

    def extract_deadline(self, text, base_date=None):
        """Извлекает дедлайн из текста, нормализуя его."""
        if not base_date:
            base_date = datetime.now()

        text_lower = self.apply_corrections(text.lower())
        for expr, days in self.TIME_EXPRESSIONS.items():
            if expr in text_lower:
                if callable(days):
                    days = days(base_date)
                deadline = base_date + timedelta(days=days)
                deadline = deadline.replace(hour=23, minute=59, second=59)
                logger.info(f"Extracted deadline: {deadline} from expression '{expr}' in text: {text}")
                return deadline

        try:
            normalized = self.normalize_text(text_lower)
        except Exception as e:
            logger.warning(f"Normalization failed: {str(e)}, using original text")
            normalized = text_lower

        try:
            parsed = dateparser.parse(
                normalized,
                settings={
                    "PREFER_DATES_FROM": "future",
                    "DATE_ORDER": "DMY",
                    "STRICT_PARSING": False,
                    "PREFERRED_LANGUAGES": ["ru"]
                }
            )
            if parsed:
                deadline = parsed.replace(hour=23, minute=59, second=59)
                logger.info(f"Extracted deadline: {deadline} from text: {text}")
                return deadline
        except Exception as e:
            logger.warning(f"Dateparser failed: {str(e)}, falling back to default")

        default_deadline = base_date + timedelta(days=7)
        logger.warning(f"Deadline not parsed for text: {text}, using default: {default_deadline}")
        return default_deadline.replace(hour=23, minute=59, second=59)
    