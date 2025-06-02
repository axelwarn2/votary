import logging
from datetime import datetime, timedelta
import dateparser

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

    def __init__(self):
        logger.info("Initialized TextNormalizer without T5 model")

    def apply_corrections(self, text):
        """Применяет словарь исправлений к тексту."""
        text_lower = text.lower()
        for wrong, correct in self.CORRECTIONS.items():
            text_lower = text_lower.replace(wrong, correct)
        return text_lower

    def normalize_text(self, text):
        """Возвращает текст с применёнными исправлениями из словаря."""
        corrected_text = self.apply_corrections(text)
        logger.info(f"Normalized text: '{text}' -> '{corrected_text}'")
        return corrected_text

    def extract_deadline(self, text, base_date=None):
        """Извлекает дедлайн из текста."""
        if not base_date:
            base_date = datetime.now()

        text_lower = self.apply_corrections(text.lower())
        for expr, days in self.TIME_EXPRESSIONS.items():
            if expr in text_lower:
                if callable(days):
                    days = days(base_date)
                deadline = base_date + timedelta(days=days)
                deadline = deadline.replace(hour=19, minute=0, second=0)
                logger.info(f"Extracted deadline: {deadline} from expression '{expr}' in text: {text}")
                return deadline

        try:
            parsed = dateparser.parse(
                text_lower,
                settings={
                    "PREFER_DATES_FROM": "future",
                    "DATE_ORDER": "DMY",
                    "STRICT_PARSING": False,
                    "PREFERRED_LANGUAGES": ["ru"]
                }
            )
            if parsed:
                deadline = parsed.replace(hour=19, minute=0, second=0)
                logger.info(f"Extracted deadline: {deadline} from text: {text}")
                return deadline
        except Exception as e:
            logger.warning(f"Dateparser failed: {str(e)}, falling back to default")

        default_deadline = base_date + timedelta(days=7)
        logger.warning(f"Deadline not parsed for text: {text}, using default: {default_deadline}")
        return default_deadline.replace(hour=19, minute=0, second=0)
    