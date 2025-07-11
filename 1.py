import openai
from loader import bot
from telebot.types import Message
from config_data.config import OPEN_AI_KEY


openai.OpenAI = OPEN_AI_KEY

print(OPEN_AI_KEY)


@bot.message_handler(commands="ai_help")
def user_from_ai(message: Message) -> None:
    bot.send_message(message.chat.id, "Задайте ваш вопрос ИИ: ")
    bot.register_next_step_handler(message, process_hendler)


def process_handler(message: Message) -> None:
    user_question = message.text
    bot.send_message(message.chat.id, f"Обрабатываю запрос...")

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Ты ветеринарный помощник."},
                {"role": "user", "content": user_question},
            ],
        )

        answer = response.choices[0].message["content"]
        bot.send_message(message.chat.id, f"{answer}")

    except Exception as exc:
        bot.send_message(message.chat.id, f"Сожалеем произошла ошибка: {exc}")
        print("Open AI Error", exc)
