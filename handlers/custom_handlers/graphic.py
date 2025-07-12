from loader import bot
from telebot.types import Message
import pandas
from utils.my_logger.logger import logging


@bot.message_handler(commands=["works"])
def works_date(message: Message) -> None:
    try:
        file_zp = pandas.read_excel("solary.xlsx", header=None)
    except Exception as exc:
        logging.info(f"Ошибка не найден график работы персонала. Подробнее: {exc}")

    graphics = []
    for index, row in file_zp.iterrows():
        if pandas.notna(row[0]):
            name = str(row[0]).strip()
            works_date = []

            for i, values in enumerate(row[1:], start=1):
                if str(values) == "+":
                    works_date.append(str(i))

            line = f"<b>{name}</b>: {', '.join(works_date)}"
            graphics.append(line)

    month = "<b>График работы вет. клиники Симба на Июль</b>\n"
    result = month + "\n".join(graphics)
    bot.send_message(message.chat.id, result, parse_mode="HTML")
