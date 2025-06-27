import redis
import hashlib
from functools import wraps
from utils.my_logger.logger import logger

r = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)


def use_redis(ttl=300):
    def decorat_func(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
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
