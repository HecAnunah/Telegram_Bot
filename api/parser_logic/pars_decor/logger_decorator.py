from utils.misc.my_logger.logger import logger


def func_logger(func):
    def wrapper(*args, **kwargs):
        logger.info(f"Функция {func.__name__} начала работу...")
        result = func(*args, **kwargs)
        return result

    return wrapper
