from bs4 import BeautifulSoup
import requests
from utils.misc.my_logger.logger import logger


url = r"http://www.vetsimba.ru/price/price.html"


def text_gen():
    for i in range(1, 2):
        urls = url
        logger.info(f"Первый блок: делаю запрос request по {url}")
        response = requests.get(urls)
        if 200 <= response.status_code <= 400:
            logger.info("URL запрос успешен. Форматирую данные...")
            bs4 = BeautifulSoup(response.content, "lxml")
            all_table = bs4.find_all("div", class_="grid")
            logger.info("Все таблицы полученны.")

            logger.info("Получаю данные с первой таблицы.")
            table_works = all_table[0].find_all("tr")
            for row in table_works:
                cols = row.find_all("td")

                if len(cols) >= 4:
                    services = cols[1].decode_contents().split("<br/>")
                    prices = cols[-1].decode_contents().split("<br/>")

                    services = [
                        BeautifulSoup(s, "lxml").text.strip()
                        for s in services
                        if s.strip()
                    ]
                    prices = [
                        BeautifulSoup(p, "lxml").text.strip()
                        for p in prices
                        if p.strip()
                    ]

                    for service, price in zip(services, prices):
                        yield f"{service} {price}"
