from telebot.types import Message
from loader import bot
from api.parser_logic.price_formatter import price_formatter
from database.user_data import user_registry


@bot.message_handler(commands=["price"])
def bot_info(message: Message):
    if message.from_user.id not in user_registry:
        bot.reply_to(message, f"Введите команду /start для знакомства с ботом.")
        return
    text = price_formatter()

    if len(text) > 4000:
        chunks = text.split("\n")
        temp = ""
        for chunk in chunks:
            if len(temp) + len(chunk) + 1 < 4000:
                temp += chunk + "\n"
            else:
                bot.send_message(message.chat.id, temp, parse_mode="HTML")
                temp = chunk + "\n"
        if temp:
            bot.send_message(message.chat.id, temp, parse_mode="HTML")

    else:
        bot.reply_to(message, text, parse_mode="HTML")
