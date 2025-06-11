from utils.misc.my_logger.logger import logger
from functools import wraps
import types


def logging_decoratos(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        logger.info(f"Начинаю работу с функцией {func.__name__}")
        try:
            func_ = func(*args, **kwargs)
            if isinstance(func_, types.GeneratorType):

                def generator_wrapped():
                    for item in func_:
                        logger.debug(f"Функция {func.__name__} вернула {item}")
                        yield item
                    logger.info(f"{func.__name__} завершила работу через Генератор.")

                return generator_wrapped()

            else:
                logger.info(
                    f"Функция {func.__name__} возвращает релуьтат своей работы через return"
                )
                return func_
        except Exception as e:
            logger.exception(f"Выявленна ошибка {e}")
            raise

    return wrapper
