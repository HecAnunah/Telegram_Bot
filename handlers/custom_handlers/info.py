from telebot.types import Message
from loader import bot

from api.parser_logic.pars_logic_info import info_getter
from config_data.config import urls
from database.user_data import user_registry


@bot.message_handler(commands=["info"])
def bot_info(message: Message):
    if message.from_user.id not in user_registry:
        bot.reply_to(message, f"Введите команду /start для знакомства с ботом.")
        return
    text = info_getter(urls[1])
    bot.reply_to(message, text)
