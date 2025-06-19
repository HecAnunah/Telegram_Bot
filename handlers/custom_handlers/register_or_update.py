from telebot.types import Message
from loader import bot
import os
import json

# Для состояний берем наш класс
from states.user_state import UserInfo
from keyboards.reply.my_keyboard import request_contact
from utils.misc.my_logger.logger import logger
from utils.is_new import is_new
from config_data.config import database_file_path
from utils.decorators.logger_decorator import logging_decoratos


@bot.message_handler(commands=["registry"])
@logging_decoratos
def bot_starts_state(message: Message) -> None:
    bot.set_state(message.from_user.id, UserInfo.name)
    bot.send_message(
        message.chat.id,
        f"Здравствуйте, введите ваше имя:",
    )


@bot.message_handler(state=UserInfo.name)
@logging_decoratos
def bot_get_name(message: Message) -> None:
    if message.text.isalpha():
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data["name"] = message.text

        bot.send_message(message.chat.id, f"Введите вашу фамилию:")
        bot.set_state(message.from_user.id, UserInfo.surename)
    else:
        bot.send_message(message.chat.id, f"Имя должно состоять из букв.")


@bot.message_handler(state=UserInfo.surename)
@logging_decoratos
def bot_get_age(message: Message) -> None:
    if message.text.isalpha():
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data["surename"] = message.text

        bot.send_message(message.chat.id, f"Введите ваше отчество:")
        bot.set_state(message.from_user.id, UserInfo.patronymic)
    else:
        bot.send_message(message.chat.id, f"Фамилия должна состоять из букв.")


@bot.message_handler(state=UserInfo.patronymic)
@logging_decoratos
def bot_get_country(message: Message) -> None:
    if message.text.isalpha():
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data["patronymic"] = message.text

        bot.send_message(
            message.chat.id,
            f"Введите ваш адрес проживания:",
        )
        bot.set_state(message.from_user.id, UserInfo.adress)
    else:
        bot.send_message(message.chat.id, f"Отчество должно состоять из букв.")


@bot.message_handler(state=UserInfo.adress)
@logging_decoratos
def bot_get_city(message: Message) -> None:
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data["adress"] = message.text

    bot.send_message(
        message.chat.id,
        f"Для завершения регистрации необходимо подтвердить номер телефона кнопкой ниже.",
        reply_markup=request_contact(),
    )
    bot.set_state(message.from_user.id, UserInfo.phone_number)


@bot.message_handler(content_types=["contact"], state=UserInfo.phone_number)
@logging_decoratos
def bot_get_phone(message: Message) -> None:
    if message.content_type == "contact":
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data["phone_number"] = message.contact.phone_number

            user_id = message.from_user.id
            logger.info("Запуск записи файла в БД...")

            # Читаем уже существующий файл БД
            try:
                if os.path.exists(database_file_path):
                    with open(database_file_path, "r", encoding="utf-8") as file:
                        users_data = json.load(file)
                        logger.info(
                            f" JSON данные ДО обновления {users_data.get(str(user_id))}"
                        )
                else:
                    users_data = {}
            except Exception as e:
                logger.warning(f"Ошибка чтения предыдущих записей BD: {e}")
                users_data = {}

            is_new_user = is_new(user_id)
            # Данные нового пользователя или обновление данных уже существующего
            users_data[str(user_id)] = data
            logger.info(f" JSON данные ПОСЛЕ обновления {users_data.get(str(user_id))}")

            if is_new_user:
                msg = "Поздравляем с регистрацией"
            else:
                msg = "Вы успешно обновили данные"

            try:
                logger.info("Начинаем обновление нашей БД...")
                with open(database_file_path, "w", encoding="utf-8") as file:
                    json.dump(users_data, file, indent=4, ensure_ascii=False)
                    logger.info("Запись файла в БД успешна.")
            except Exception as e:
                logger.warning(f"Ошибка при записи файла в JSON  {e}")

        bot.send_message(
            message.chat.id,
            f"Ваш номер {data['phone_number']} записан. {msg}.",
        )
        bot.delete_state(message.from_user.id, message.chat.id)
    else:
        bot.send_message(message.from_user.id, f"Нужно подтвердит отправку номера.")
