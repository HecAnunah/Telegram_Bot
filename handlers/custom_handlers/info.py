from telebot.types import Message
from loader import bot

from api.parser_logic.pars_logic_info import info_getter
from config_data.config import urls


@bot.message_handler(commands=["info"])
def bot_info(message: Message):
    text = info_getter(urls[1])
    bot.reply_to(message, text)
