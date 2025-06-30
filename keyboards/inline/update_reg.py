from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def update_or_not() -> InlineKeyboardMarkup:
    """
    Создает объет Inline клавиатуры с двумя кнопками да-нет, который используется для прохождения
    регистрации новым пользователем или обновлением данных уже существующего пользователя

    Returns:
        InlineKeyboardMarkup: объект клавиатуры с двумя кнопками
    """
    keyboard = InlineKeyboardMarkup()

    button_yes = InlineKeyboardButton(
        text="Обновить данные регистрации.", callback_data="yes"
    )
    button_not = InlineKeyboardButton(text="Вернутся в меню.", callback_data="no")

    keyboard.add(button_yes, button_not)
    return keyboard
