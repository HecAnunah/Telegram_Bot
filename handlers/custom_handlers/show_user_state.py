from loader import bot
from telebot.types import Message


@bot.message_handler(commands=["user_state"])
def show_state(message: Message) -> None:
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        if not data:
            bot.send_message(message.chat.id, f"Ваших данных нет в базе.")
            return

        name = data.get("name", "Не указанно")
        age = data.get("age", "Не указанно")
        country = data.get("country", "Не указанно")
        city = data.get("city", "Не указанно")
        phone = data.get("phone_number", "Не указанно")

        result = f"Имя {name}\nВозраст {age}\nСтрана проживания {country}\nГород {city}\nТелефон {phone}"
        bot.send_message(message.chat.id, result)
