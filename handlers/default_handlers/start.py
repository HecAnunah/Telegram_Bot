from telebot.types import Message

from loader import bot
from config_data.config import DEFAULT_COMMANDS
from api.api_weather import get_weather
from utils.my_logger.logger_decorator import logging_decoratos
from utils.my_logger.logger import logger


@bot.message_handler(commands=["start"])
@logging_decoratos
def bot_start(message: Message):
    """
    Обрабатывает команду /start
    Выводит данные о погоде
    Выводит список команд для бота

    Args:
        message (Message): объект сообщения от пользователя

    Returns:
        None
    """
    try:
        bot.reply_to(
            message, f"Привет, {message.from_user.first_name}.\n{get_weather()}"
        )
    except Exception as e:
        logger.error(f"Ошибка не удалось подключится к API.\n Наименование: {e}")
        bot.reply_to(message, f"Привет, {message.from_user.first_name}.")

    text = [f"/{command} - {desk}" for command, desk in DEFAULT_COMMANDS]
    bot.send_message(message.chat.id, "\n".join(text))
