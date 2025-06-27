from telebot.types import Message
from loader import bot

from api.parser_logic.pars_logic_info import info_getter
from config_data.config import urls
from utils.my_logger.logger_decorator import logging_decoratos

url = r"http://www.vetsimba.ru/index.html"


@bot.message_handler(commands=["info"])
@logging_decoratos
def bot_show_info(message: Message):
    text = info_getter(url)
    bot.reply_to(message, text)
