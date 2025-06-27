from api.parser_logic.pars_logic_price import price_gen
from config_data.config import urls
from utils.my_logger.logger_decorator import logging_decoratos
from utils.redis_cashe import use_redis


@logging_decoratos
@use_redis(300)
def price_formatter():
    formatted = []

    for line in price_gen():
        line = line.strip()

        if line.startswith("•"):
            formatted.append(f"<i>{line}</i>")
            continue

        parts = line.rsplit(" ", 1)
        if len(parts) == 2 and parts[1].replace(" ", "").replace("от", "").isdigit():
            service, price = parts
            formatted.append(f"<b>{service}</b> — <code>{price}</code>")
        else:
            # Если не удалось — просто добавим как есть
            formatted.append(line)

    return "\n".join(formatted)
