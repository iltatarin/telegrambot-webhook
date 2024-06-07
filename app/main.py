import logging
import random
from os import getenv

from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiohttp import web

from const import (
    GUESS_NUMBER_IS_GREATER,
    GUESS_NUMBER_IS_LESS,
    USER_GUESSED_MESSAGE,
    WELCOME_MESSAGE,
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Локальный БД для загаданных чисел
users_data_db: dict[int, int] = {}

# Инициализация телеграм бота
BOT_TOKEN = getenv("BOT_TOKEN")
bot = Bot(token=BOT_TOKEN)

dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(msg: types.Message) -> None:
    """При команде /start создаем число"""

    generate_user_number(msg=msg)
    await msg.answer(text=WELCOME_MESSAGE)


def generate_user_number(msg: types.Message) -> int:
    """Создаем и возвращаем рандомное число"""

    number = random.randint(1, 100)
    logger.info(f"Сгененировано число: {number}")
    users_data_db[msg.chat.id] = number
    logger.info(f"chat_id: {msg.chat.id}")
    return number


def get_guess_number(msg: types.Message) -> int:
    """Возвращаем загаданное число. Если нет - генерим новый."""

    guess_number = users_data_db.get(msg.chat.id, None)
    if guess_number is None:
        return generate_user_number(msg)

    return guess_number


@dp.message()
async def message_handler(msg: types.Message) -> None:
    try:
        number = int(msg.text)
        logger.info(f"Пользователь ввел число: {number}")

        guess_number = get_guess_number(msg=msg)
        if number > guess_number:
            await msg.answer(GUESS_NUMBER_IS_LESS)
        elif number < guess_number:
            await msg.answer(GUESS_NUMBER_IS_GREATER)
        else:
            await msg.answer(USER_GUESSED_MESSAGE)
    except TypeError:
        await msg.answer("Введите целое число!")


async def handle_webhook(request):
    """Обрабатываем webhook и шлем сообщению боту"""

    # Достаем токен
    url = str(request.url)
    index = url.rfind("/")
    token = url[index + 1 :]

    # Проверяем токен
    if token == BOT_TOKEN:
        request_data = await request.json()
        update = types.Update(**request_data)
        await dp._process_update(bot=bot, update=update)

        return web.Response()
    else:
        return web.Response(status=403)


if __name__ == "__main__":
    # Запуск aiohttp сервера

    app = web.Application()
    app.router.add_post(f"/{BOT_TOKEN}", handle_webhook)
    web.run_app(app, host="0.0.0.0", port=8080)
