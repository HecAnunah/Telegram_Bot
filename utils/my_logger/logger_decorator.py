from utils.my_logger.logger import logger
from functools import wraps
from types import GeneratorType

from typing import Callable, Any, Union, Generator


def logging_decoratos(
    func: Callable[..., Any],
) -> Callable[..., Union[Any, Generator[Any, None, None]]]:

    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Union[Any, Generator[Any, None, None]]:
        """
        Декоратор для логирования функций
        Отмечает начало работы функции и завершение ее работы
        Логирует тип возвращаемого результата yield или return

        Returns:
            func: возвращает функцию
        """
        logger.info(f"Начинаю работу с функцией {func.__name__}")
        try:
            func_ = func(*args, **kwargs)
            if isinstance(func_, GeneratorType):

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
