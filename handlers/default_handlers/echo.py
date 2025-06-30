from telebot.types import Message

from loader import bot


# Эхо хендлер, куда летят текстовые сообщения без указанного состояния
@bot.message_handler(state=None)
def bot_echo(message: Message):
    """
    Обрабатывает не задокументированные команды /...

    Args:
        message (Message): объект сообщения от пользователя

    Returns:
        None
    """
    bot.reply_to(
        message, "Эхо без состояния или фильтра.\n" f"Сообщение: {message.text}"
    )
