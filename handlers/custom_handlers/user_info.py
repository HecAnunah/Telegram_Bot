from loader import bot
from telebot.types import Message

from utils.my_logger.logger_decorator import logging_decoratos
from database.peewe_model import Client


@bot.message_handler(commands=["user_info"])
@logging_decoratos
def bot_user_info(message: Message) -> None:
    """
    Обрабатывает команду /user_info и выводит информацию о зарегистрированном пользовате
    если пользователь не зарегестрирован отправляется сообщение - "Вы не зарегестрированны. Пройдите регистрацию."

    Args:
        message (Message): объект сообщения от пользователя

    Returns:
        None
    """

    if not (client := Client.get_or_none(Client.user_id == message.from_user.id)):
        bot.send_message(
            message.from_user.id, "Вы не зарегестрированны. Пройдите регистрацию."
        )
    else:
        bot.send_message(message.from_user.id, str(client), parse_mode="HTML")
