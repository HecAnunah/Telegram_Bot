import redis
import hashlib
from functools import wraps
from utils.my_logger.logger import logger

from typing import Callable, Any

r = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)


def use_redis(ttl: int = 300) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """
    Декоратор для кеширования результата выполнения функции с использованием Redis.

    Ключ кеша строится на основе имени функции и её аргументов.
    Если результат уже есть в кеше, он возвращается без повторного вызова функции.

    Args:
        ttl (int): Время жизни кеша в секундах. По умолчанию 300 секунд.

    Returns:
        Callable: Декоратор, оборачивающий функцию в механизм кеширования.
    """

    def decorat_func(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            key_ = f"{func.__name__}: {args}:{kwargs}"
            cache_key = "cache:" + hashlib.md5(key_.encode()).hexdigest()
            cached = r.get(cache_key)

            if cached:
                logger.info("Возвращаю данные из КЭША")
                return cached

            logger.info("В КЭШе пусто. Возвращаю результат работы функции")
            new_cesh_data = func(*args, **kwargs)
            r.setex(cache_key, ttl, new_cesh_data)

            return new_cesh_data

        return wrapper

    return decorat_func
