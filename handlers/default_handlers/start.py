from telebot.types import Message

from loader import bot
from config_data.config import DEFAULT_COMMANDS
from utils.misc.is_new import is_new
from api.api_weather import get_weather
from utils.my_logger.logger_decorator import logging_decoratos
from utils.my_logger.logger import logger


@bot.message_handler(commands=["start"])
@logging_decoratos
def bot_start(message: Message):
    try:
        bot.reply_to(
            message, f"Привет, {message.from_user.first_name}.\n{get_weather()}"
        )
    except Exception as e:
        logger.error(f"Ошибка не удалось подключится к API.\n Наименование: {e}")
        bot.reply_to(message, f"Привет, {message.from_user.first_name}.")

    text = [f"/{command} - {desk}" for command, desk in DEFAULT_COMMANDS]
    bot.send_message(message.chat.id, "\n".join(text))

    is_new_user = is_new(message.from_user.id)
    if is_new_user:
        bot.send_message(
            message.chat.id, f"Пройдите регистрацию для знакомства с Вами."
        )
