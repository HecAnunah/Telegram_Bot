from loader import bot
from telebot.types import Message
import pandas
from utils.my_logger.logger import logging


@bot.message_handler(commands="/graphic")
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

            line = f"{name} {' '.join(works_date)}"
            graphics.append(line)
    result = "\n".join(graphics)
    return result
