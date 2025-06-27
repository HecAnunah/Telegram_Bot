import os
from dotenv import load_dotenv, find_dotenv

if not find_dotenv():
    exit("Переменные окружения не загружены т.к отсутствует файл .env")
else:
    load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
DB_PATH = "database/clients.db"
DEFAULT_COMMANDS = (
    ("start", "Запустить бота"),
    ("stop", "Остановть бота"),
    ("help", "Вывести справку"),
    ("info", "Вывести информацию о нас"),
    ("price", "Вывести Прайс-лист"),
    ("user_info", "Посмотреть Ваши регистрационные данные"),
    ("registry", "Регистрация"),
)

# Парсинг дата - перенес в api -> pars_logic
