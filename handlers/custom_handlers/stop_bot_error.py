from telebot.types import Message

from loader import bot
from utils.decorators.logger_decorator import logging_decoratos

@bot.message_handler(commands=["stop"])
@logging_decoratos
def bot_stop(message: Message):
    bot.reply_to(message, "Тест пройден успешно. Бот завершает работу.")
    raise RuntimeError('Остановка бота командой /stop')

