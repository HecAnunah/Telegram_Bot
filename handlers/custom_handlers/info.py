from telebot.types import Message

from loader import bot


@bot.message_handler(commands=["info"])
def bot_info(message: Message):
    text = [f"Chat ID {message.chat.id}"]
    bot.reply_to(message, "\n".join(text))
