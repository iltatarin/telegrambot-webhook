import logging
import random

logger = logging.getLogger(__name__)

# БД загаданных чисел
GUSS_NUMBER_DB: dict[int, int] = {}


def create_guess_number(chat_id: int) -> int:
    """Создаем угадываемое число"""

    number = random.randint(1, 100)
    logger.info(f"Угадываемое число: {number}")

    GUSS_NUMBER_DB[chat_id] = number
    logger.info(f"chat_id: {chat_id}")
    return number


def get_guess_number(chat_id: int) -> int:
    """Возвращаем угадываемое число.

    Если число отсутсвует в БД - создаем новый."""

    guess_number = GUSS_NUMBER_DB.get(chat_id, None)
    if guess_number is None:
        return create_guess_number(chat_id)

    return guess_number
