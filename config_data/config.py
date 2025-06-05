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
    ("info", "Вывести справку по чату"),
    ("id", "Вывести ID"),
    ("price", "Вывести Прайс-лист"),
    ("update_user", "Создать или Обновить свои данные"),
    ("user_state", "Показать данные"),
)

# Парсинг дата
urls = [
    r"http://www.vetsimba.ru/price/price.html",
    r"http://www.vetsimba.ru/index.html",
]
