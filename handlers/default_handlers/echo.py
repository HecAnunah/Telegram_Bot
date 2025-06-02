from telebot.types import Message

from loader import bot
from database.user_data import user_registry


# Эхо хендлер, куда летят текстовые сообщения без указанного состояния
@bot.message_handler(state=None)
def bot_echo(message: Message):
    if message.from_user.id not in user_registry:
        bot.reply_to(message, f"Введите команду /start для знакомства с ботом.")
        return
    bot.reply_to(
        message, "Эхо без состояния или фильтра.\n" f"Сообщение: {message.text}"
    )
