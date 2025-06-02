from bs4 import BeautifulSoup
import requests
from utils.misc.my_logger.logger import logger

adress_info = {
    "Sviblovo": " г. Москва ул. Радужная дом 25\nТелефон: 8 (495) 656-67-43",
    "Polarnaya": "г. Москва ул. Полярная дом 54 к. 2\nТелефон: 8 (499) 478-32-91",
}


def info_getter(url):
    response = requests.get(url)
    logger.info(f"\nДелаю запрос по URL {url}")
    if 200 <= response.status_code <= 400:
        logger.info("Запрос успешен. Преобразую файлы в soup")
        soup = BeautifulSoup(response.content, "lxml")
        info = soup.find("div", class_="unit whole")
        info_result = info.find("p", align="justify").get_text(strip=True)
        logger.info("Запрос на Информацию о клинике готов к выдаче.")

        result = (
            "О нас:\n"
            + info_result
            + "\n"
            + "\nАдрес:\n"
            + adress_info["Sviblovo"]
            + "\n"
            + "\n"
            + adress_info["Polarnaya"]
        )
        return result
