import os
from dotenv import load_dotenv, find_dotenv

if not find_dotenv():
    exit("Переменные окружения не загружены т.к отсутствует файл .env")
else:
    load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
RAPID_API_KEY = os.getenv("RAPID_API_KEY")
DEFAULT_COMMANDS = (
    ("start", "Запустить бота"),
    ("help", "Вывести справку"),
    ("info", "Вывести информацию о нас"),
    ("price", "Вывести Прайс-лист"),
    ("registr_info", "Посмотреть Ваши регистрационные данные"),
    ("registry", "Регистрация"),
)

# Парсинг дата
urls = [
    r"http://www.vetsimba.ru/price/price.html",
    r"http://www.vetsimba.ru/index.html",
]

# Путь к базе данных пользователя

database_file_path = os.path.join(os.getcwd(), "database", "user_data.json")
