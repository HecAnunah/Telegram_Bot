from bs4 import BeautifulSoup
import requests
from utils.my_logger.logger import logger
from utils.my_logger.logger_decorator import logging_decoratos
from utils.redis_cashe import use_redis


adress_info = {
    "Sviblovo": " г. Москва ул. Радужная дом 25\nТелефон: 8 (495) 656-67-43",
    "Polarnaya": "г. Москва ул. Полярная дом 54 к. 2\nТелефон: 8 (499) 478-32-91",
}


@logging_decoratos
@use_redis(300)
def info_getter() -> str:
    """
    Получает с сайта информацию о клинике, включая описание, адреса и телефоны.

    Делает запрос к главной странице сайта, извлекает описание из блока <div class="unit whole">,
    а также добавляет заранее известные адреса двух филиалов.

    Returns:
        str: Информация о клинике в виде форматированной строки.

    """
    url = r"http://www.vetsimba.ru/index.html"
    response = requests.get(url)
    logger.info(f"Делаю запрос по URL {url}")
    try:
        if 200 <= response.status_code <= 400:
            logger.info("Создаю объект BeautifulSoup")
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
            logger.info("Вывожу информацию о клинике")
            return result
    except Exception as exc:
        logger.info(
            f"Во время парсинга страницы: http://www.vetsimba.ru/index.html появилась ошибка: {exc} "
        )
        return "Произошла ошибка в функции info_getter() при получении информации о клинике."
