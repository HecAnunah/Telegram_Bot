from telebot.handler_backends import State, StatesGroup


class UserInfo(StatesGroup):
    name = State()
    surename = State()
    patronymic = State()
    adress = State()
    phone_number = State()
