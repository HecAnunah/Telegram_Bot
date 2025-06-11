from loader import bot
from telebot.types import Message
import os
import json

from config_data.config import database_file_path
from utils.decorators.logger_decorator import logging_decoratos


@bot.message_handler(commands=["registr_info"])
@logging_decoratos
def bot_show_state(message: Message) -> None:

    user_id = str(message.from_user.id)

    if not os.path.exists(database_file_path):
        bot.send_message(
            message.chat.id,
            f"Данных не существует. Техническая ошибка, нет пути {database_file_path}",
        )
        return
    else:
        with open(database_file_path, "r", encoding="utf-8") as file:
            all_user_data = json.load(file)

        user_data = all_user_data.get(user_id)
        if not user_data:
            bot.send_message(
                message.chat.id,
                f"Нет сохраненных данных. Пройдите регистрацию.",
            )
        else:
            text = (
                f"📝 Сохранённые данные:\n"
                f"👤 Имя: {user_data.get('name', 'не указано')}\n"
                f"🎂 Возраст: {user_data.get('surename', 'не указано')}\n"
                f"🌍 Страна: {user_data.get('patronymic', 'не указано')}\n"
                f"🏙 Город: {user_data.get('adress', 'не указано')}\n"
                f"📞 Телефон: {user_data.get('phone_number', 'не указано')}"
            )
            bot.send_message(message.chat.id, text)
