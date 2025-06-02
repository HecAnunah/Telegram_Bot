from api.parser_logic.pars_logic_price import text_gen
from config_data.config import urls


def price_formatter():
    formatted = []

    for line in text_gen(urls[0]):
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
