from telebot.types import Message
from loader import bot

# Для состояний берем наш класс
from states.user_state import UserInfo
from keyboards.reply.my_keyboard import request_contact


@bot.message_handler(commands=["update_user"])
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

            bot.send_message(
                message.chat.id,
                f"Ваш номер {data['phone_number']} записан. Поздравляю с регистрацией.",
            )
    else:
        bot.send_message(message.from_user.id, f"Нужно подтвердит отправку номера.")
