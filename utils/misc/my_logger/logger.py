import logging
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("bot.log", encoding="utf-8"),  # Выводит логи в файл
        logging.StreamHandler(),  # Выдает логирование в поток (в терминал)
    ],
    force=True,
)

logger = logging.getLogger("my_logger")
print(logger)
