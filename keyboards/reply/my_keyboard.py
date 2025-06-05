from telebot.types import KeyboardButton, ReplyKeyboardMarkup


def request_contact() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(True, True)
    keyboard.add(
        KeyboardButton("Подтвердите отправку номера телефона", request_contact=True)
    )
    return keyboard
