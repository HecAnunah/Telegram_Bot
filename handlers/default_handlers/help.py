from telebot.types import Message

from config_data.config import DEFAULT_COMMANDS
from loader import bot
from utils.my_logger.logger_decorator import logging_decoratos


@bot.message_handler(commands=["help"])
@logging_decoratos
def bot_help(message: Message):
    """
    Обрабатывает сообщение /help
    Выводит список команд бота

    Args:
        message (Message): объект сообщения от пользователя

    Returns:
        None
    """
    text = [f"/{command} - {desk}" for command, desk in DEFAULT_COMMANDS]
    bot.reply_to(message, "\n".join(text))
