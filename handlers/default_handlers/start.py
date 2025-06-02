from telebot.types import Message

from loader import bot
from database.user_data import user_registry
from config_data.config import DEFAULT_COMMANDS


@bot.message_handler(commands=["start"])
def bot_start(message: Message):
    user_registry.add(message.from_user.id)
    bot.reply_to(message, f"Привет, {message.from_user.full_name}!")
    text = [f"/{command} - {desk}" for command, desk in DEFAULT_COMMANDS]
    bot.send_message(message.chat.id, "\n".join(text))
