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


@bot.message_handler(commands=["registry"])
def starts_state(message: Message) -> None:
    bot.set_state(message.from_user.id, UserInfo.name)
    bot.send_message(
        message.chat.id,
        f"Здравствуйте, {message.from_user.first_name} введите ваше имя.",
    )


@bot.message_handler(state=UserInfo.name)
def get_name(message: Message) -> None:
    if message.text.isalpha():
        bot.send_message(message.chat.id, f"Ваше имя записанно. Введите ваш возраст.")
        bot.set_state(message.from_user.id, UserInfo.age)

        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data["name"] = message.text
    else:
        bot.send_message(message.chat.id, f"Имя должно состоять из букв.")


@bot.message_handler(state=UserInfo.age)
def get_age(message: Message) -> None:
    if message.text.isdigit():
        bot.send_message(
            message.chat.id, f"Ваш возраст записанн. Введите вашу страну проживания."
        )
        bot.set_state(message.from_user.id, UserInfo.country)

        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data["age"] = message.text
    else:
        bot.send_message(message.chat.id, f"Возраст - только цифры.")


@bot.message_handler(state=UserInfo.country)
def get_country(message: Message) -> None:
    bot.send_message(message.chat.id, f"Страну проживания записали. Введите город.")
    bot.set_state(message.from_user.id, UserInfo.city)

    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data["country"] = message.text


@bot.message_handler(state=UserInfo.city)
def get_city(message: Message) -> None:
    bot.send_message(
        message.chat.id,
        f"Город проживания добавлен. Дайте разрешение на ваш номер телефона нажав на кнопку под строкой ввода.",
        reply_markup=request_contact(),
    )
    bot.set_state(message.from_user.id, UserInfo.phone_number)

    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data["city"] = message.text


@bot.message_handler(content_types=["contact"], state=UserInfo.phone_number)
def get_phone(message: Message) -> None:
    if message.content_type == "contact":
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data["phone_number"] = message.contact.phone_number

            user_id = message.from_user.id

            logger.info("Запуск записи фалйа в БД...")

            # Читаем уже существующий файл БД
            try:
                if os.path.exists(database_file_path):
                    with open(database_file_path, "r", encoding="utf-8") as file:
                        users_data = json.load(file)
                        logger.info(f" JSON данные ДО обновления {users_data}")
                else:
                    users_data = {}
            except Exception as e:
                logger.warning(f"Ошибка чтения предыдущих записей BD: {e}")
                users_data = {}

            is_new_user = is_new(message.from_user.id)
            # Данные нового пользователя или обновление данных уже существующего
            users_data[str(user_id)] = data
            logger.info(f" JSON данные ПОСЛЕ обновления {users_data}")

            if is_new_user:
                msg = "Поздравляем с регистрацией"
            else:
                msg = "Вы успешно обновили данные"

            try:
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
