from api.price_parser.pars_logic import text_gen


def price_formatter():
    formatted = []

    for line in text_gen():
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
