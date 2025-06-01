from telebot.types import Message

from loader import bot


@bot.message_handler(commands=["id"])
def id(message: Message):
    text = f"Ваш ID: {message.from_user.id}\nID чата: {message.chat.id}"
    bot.reply_to(message, text)
