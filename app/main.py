import logging
import random
from os import getenv

from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiohttp import web
from const import (GUESS_NUMBER_IS_GREATER_MESSAGE,
                   GUESS_NUMBER_IS_LESS_MESSAGE, USER_GUESSED_MESSAGE,
                   WELCOME_MESSAGE)

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

# API routess
routes = web.RouteTableDef()


@dp.message(CommandStart())
async def command_start_handler(msg: types.Message) -> None:
    """Обработчик команды /start"""

    generate_user_number(msg=msg)
    await msg.answer(text=WELCOME_MESSAGE)


def generate_user_number(msg: types.Message) -> int:
    """Возвразаем рандомное число"""

    number = random.randint(1, 100)
    logger.info(f"Сгененировано число: {number}")
    users_data_db[msg.chat.id] = number
    logger.info(f"chat_id: {msg.chat.id}")
    return number


def get_guess_number(msg: types.Message) -> int:
    """Возвращаем загаданное число. Если нет - создаем новый"""

    guess_number = users_data_db.get(msg.chat.id, None)
    if guess_number is None:
        return generate_user_number(msg)

    return guess_number


@dp.message()
async def message_handler(msg: types.Message) -> None:
    """Обработчик сообщений"""
    try:
        number = int(msg.text)
        logger.info(f"Пользователь ввел число: {number}")

        guess_number = get_guess_number(msg=msg)
        if number > guess_number:
            await msg.answer(GUESS_NUMBER_IS_LESS_MESSAGE)
        elif number < guess_number:
            await msg.answer(GUESS_NUMBER_IS_GREATER_MESSAGE)
        else:
            await msg.answer(USER_GUESSED_MESSAGE)
    except TypeError:
        await msg.answer("Введите целое число!")


# ----------------
# API
# ----------------


@routes.get("/")
async def health(request):
    """Используется для readiness_probe"""
    return web.Response(text="OK")


@routes.post(f"/{BOT_TOKEN}")
async def handle_webhook_request(request):
    """Используется для обработки webhook из telegram"""

    # Достаем токен
    url = str(request.url)
    index = url.rfind("/")
    token = url[index + 1 :]

    # Проверяем токен
    if token == BOT_TOKEN:
        request_data = await request.json()
        update = types.Update(**request_data)
        await dp._process_update(bot=bot, update=update)

        return web.Response(text="OK")
    else:
        return web.Response(status=403)


if __name__ == "__main__":
    # Запуск aiohttp сервера

    app = web.Application()
    app.add_routes(routes)
    web.run_app(app, host="0.0.0.0", port=8080)
