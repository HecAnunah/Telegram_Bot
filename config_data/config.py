import os
from typing import Tuple
from dotenv import load_dotenv, find_dotenv

if not find_dotenv():
    exit("Переменные окружения не загружены т.к отсутствует файл .env")
else:
    load_dotenv()

BOT_TOKEN: str = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    exit(f"Ошибка: переменная окружения BOT_TOKEN не обнаруженна.")
OPEN_AI_KEY: str = os.getenv("OPEN_AI_KEY")

DB_PATH: str = "database/clients.db"
DEFAULT_COMMANDS: Tuple[Tuple[str, str], ...] = (
    ("start", "Запустить бота"),
    ("works", "Даты работы врачей"),
    ("help", "Вывести справку"),
    ("info", "Вывести информацию о нас"),
    ("price", "Вывести Прайс-лист"),
    ("user_info", "Посмотреть Ваши регистрационные данные"),
    ("registry", "Регистрация"),
    ("ai_help", "Задать вопрос ИИ"),
    ("exit_ai", "Выйти из диалога с ботом"),
)
