from telebot.types import Message

from loader import bot
from config_data.config import DEFAULT_COMMANDS
from utils.is_new import is_new


@bot.message_handler(commands=["start"])
def bot_start(message: Message):
    bot.reply_to(message, f"Привет, {message.from_user.full_name}!")
    text = [f"/{command} - {desk}" for command, desk in DEFAULT_COMMANDS]
    bot.send_message(message.chat.id, "\n".join(text))

    is_new_user = is_new(message.from_user.id)
    if is_new_user:
        bot.send_message(
            message.chat.id, f"Пройдите регистрацию для знакомства с Вами."
        )
