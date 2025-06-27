from loader import bot
import handlers  # noqa
from utils.set_bot_commands import set_default_commands
from utils.my_logger.logger import logger

# Подгружаем поддержку состояний
from telebot.custom_filters import StateFilter
from database.peewe_model import create_models, db


if __name__ == "__main__":
    db.connect()
    create_models()
    bot.add_custom_filter(StateFilter(bot))  # отвечает за поддержку состояний
    set_default_commands(bot)
    logger.info("Бот запускается...")
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        logger.error(f"Ошибка в боте: {e}")
    finally:
        logger.info("Бот завершил работу.")
