from telebot.types import Message

from config_data.config import DEFAULT_COMMANDS
from loader import bot
from database.user_data import user_registry


@bot.message_handler(commands=["help"])
def bot_help(message: Message):
    if message.from_user.id not in user_registry:
        bot.reply_to(message, f"Введите команду /start для знакомства с ботом.")
        return
    text = [f"/{command} - {desk}" for command, desk in DEFAULT_COMMANDS]
    bot.reply_to(message, "\n".join(text))
