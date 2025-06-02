from telebot.types import Message

from loader import bot
from database.user_data import user_registry


@bot.message_handler(commands=["id"])
def id(message: Message):
    if message.from_user.id not in user_registry:
        bot.reply_to(message, f"Введите команду /start для знакомства с ботом.")
        return
    text = f"Ваш ID: {message.from_user.id}\nID чата: {message.chat.id}"
    bot.reply_to(message, text)
