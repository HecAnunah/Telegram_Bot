import openai
from loader import bot
from telebot.types import Message

# ключ скорее всего ограницен кол-вом запросов
from config_data.config import OPEN_AI_KEY

from utils.my_logger.logger import logging
from states.user_state import ChatAI

client = openai.OpenAI(api_key=OPEN_AI_KEY, base_url="https://openrouter.ai/api/v1")


@bot.message_handler(commands=["ai_help"])
def user_from_ai(message: Message) -> None:
    bot.set_state(message.from_user.id, ChatAI.ai_state, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data["history"] = [
            {
                "role": "system",
                "content": "Ты вежливый помощник.",
            }
        ]
    bot.send_message(message.chat.id, "Задайте ваш вопрос ИИ: ")


@bot.message_handler(state=ChatAI.ai_state)
def process_handler(message: Message) -> None:
    if message.text == "/exit_ai":
        bot.delete_state(message.from_user.id, message.chat.id)
        bot.send_message(message.chat.id, f"Вы вышли из диалога с ИИ.")
        return

    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        messages = data.get("history", [])
        messages.append({"role": "user", "content": message.text})
        logging.info(f"Вопрос пользователя: {message.text}")

    try:
        response = client.chat.completions.create(
            model="openai/gpt-3.5-turbo-0613",  # или gpt-4, если у тебя есть доступ
            messages=messages,
        )

        answer = response.choices[0].message.content
        logging.info(f"Ответ бота: {answer}")
        bot.send_message(message.chat.id, f"{answer}")

    except Exception as exc:
        bot.send_message(message.chat.id, f"Сожалеем произошла ошибка: {exc}")
        logging.info(f"Ошибка: {exc}")
