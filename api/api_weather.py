import requests
from utils.redis_cashe import use_redis
from utils.my_logger.logger import logger


@use_redis(300)
def get_weather():
    params = {
        "latitude": 55.7558,
        "longitude": 37.6176,
        "hourly": "temperature_2m",
        "current_weather": True,
        "timezone": "Europe/Moscow",
    }

    logger.info(f"Подаю request запрос к open-meteo...")

    response = requests.get(
        "https://api.open-meteo.com/v1/forecast", params=params, timeout=2
    )
    if not 200 <= response.status_code <= 400:
        logger.info(f"response.statuc_code не пройден. Возврат None")
        return None
    else:
        data = response.json()
        temperature = data["current_weather"]["temperature"]
        time = data["current_weather"]["time"].replace("T", " ")
        result = f"Температура на улице {temperature}C°\nВремя {time}"
        logger.info(f"Получен результат работы функции: {result}")
        return result
