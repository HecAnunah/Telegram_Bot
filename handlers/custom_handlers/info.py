from telebot.types import Message
from loader import bot

from api.parser_logic.pars_logic_info import info_getter
from utils.my_logger.logger_decorator import logging_decoratos


@bot.message_handler(commands=["info"])
@logging_decoratos
def bot_show_info(message: Message):
    """
    Обрабатывает команду /info
    Выводит информацию с главной страницы сайта vetsimba.ru о Нас, адрес и телефоны

    Args:
        message (Message): объект сообщения от пользователя

    Returns:
        None
    """
    text = info_getter()
    bot.reply_to(message, text)
