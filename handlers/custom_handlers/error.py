from telebot.types import Message

from loader import bot


@bot.message_handler(commands=["error"])
def test_error(message: Message):
    bot.reply_to(message, "Тест пройден успешно. Бот завершает работу.")
    raise ValueError("Ошибка для проверки блока Exxept блока main")
