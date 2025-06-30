from telebot.types import KeyboardButton, ReplyKeyboardMarkup


def request_contact() -> ReplyKeyboardMarkup:
    """
    Создает объект Reply клавиатуры для подтверждения отправки пользователем своего контактного номера

    Returns:
        ReplyKeyboardMarkup: объект клавиатуры с кнопкой запроса контакта
    """
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(
        KeyboardButton("Подтвердите отправку номера телефона", request_contact=True)
    )
    return keyboard
