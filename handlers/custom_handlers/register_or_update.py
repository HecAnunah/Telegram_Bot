from telebot.types import Message, ReplyKeyboardRemove
from loader import bot


# Для состояний берем наш класс
from states.user_state import UserInfo
from keyboards.reply.my_keyboard import request_contact
from keyboards.inline.update_reg import update_or_not
from utils.my_logger.logger import logger
from utils.my_logger.logger_decorator import logging_decoratos
from database.peewe_model import Client
from config_data.config import DEFAULT_COMMANDS


@bot.message_handler(commands=["registry"])
@logging_decoratos
def bot_starts_state(message: Message) -> None:
    if not Client.select().where(Client.user_id == message.from_user.id).exists():
        bot.set_state(message.from_user.id, UserInfo.name)
        bot.send_message(
            message.chat.id,
            f"Здравствуйте, введите ваше имя:",
        )
    else:
        logger.info(
            f"Пользователь с user_id={message.from_user.id} уже есть в базе данных. Отправляем клавиатуру Inline и предлагаем выбор"
        )
        bot.send_message(
            message.from_user.id,
            "Вы уже зарегестрированны. Обновить данные?",
            reply_markup=update_or_not(),
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
def bot_get_surename(message: Message) -> None:
    if message.text.replace("-", "").replace(" ", "").isalpha():
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

            # Удаляем клавиатуру
            bot.send_message(
                message.from_user.id,
                "Спасибо. Телефон внесен в базу данных.",
                reply_markup=ReplyKeyboardRemove(),
            )
            logger.info("Запуск записи файла в БД...")

            # Выбираем что делать или обновить данные пользователя или создать нового.
            if Client.select().where(Client.user_id == message.from_user.id).exists():
                Client.update(
                    name=data["name"],
                    surename=data["surename"],
                    patronymic=data["patronymic"],
                    adress=data["adress"],
                    phone_number=data["phone_number"],
                ).where(Client.user_id == message.from_user.id).execute()

                logger.info(
                    f"Пользователь {message.from_user.id} успешно обновил данные."
                )
                bot.send_message(message.from_user.id, "Вы успешно обновили данные!")
            else:
                Client.create(
                    user_id=message.from_user.id,
                    name=data["name"],
                    surename=data["surename"],
                    patronymic=data["patronymic"],
                    adress=data["adress"],
                    phone_number=data["phone_number"],
                )
                logger.info(f"Пользователь {message.from_user.id} прошел регистрацию.")
                bot.send_message(message.from_user.id, "Регистрация завершена!")

        bot.delete_state(message.from_user.id, message.chat.id)
    else:
        bot.send_message(message.from_user.id, f"Нужно подтвердит отправку номера.")
        bot.delete_state(message.from_user.id, message.chat.id)


# Обрабатываем ответ ДА Inline клавиатуры
@bot.callback_query_handler(func=lambda callback_query: callback_query.data == "yes")
def yes_answer(callback_query):
    # Удаляем клавиату
    bot.edit_message_reply_markup(
        callback_query.from_user.id, callback_query.message.message_id
    )
    bot.set_state(callback_query.from_user.id, UserInfo.name)
    bot.send_message(callback_query.message.chat.id, "Введите свое имя.")


# Обрабатываем ответ НЕТ Inline клавиатуры
@bot.callback_query_handler(func=lambda callback_query: callback_query.data == "no")
def no_answer(callback_query):
    bot.delete_state(callback_query.from_user.id, callback_query.message.chat.id)
    menu = [f"/{command} - {commit}" for command, commit in DEFAULT_COMMANDS]
    bot.send_message(callback_query.from_user.id, "\n".join(menu))
