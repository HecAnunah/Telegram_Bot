from telebot.handler_backends import State, StatesGroup


class ChatAI(StatesGroup):
    """
    Класс состояния для поддержки АИ.

    Атрибуты:
        ai_state (State): состояние нахождения в диалоге с АИ.
    """

    ai_state = State()


class UserInfo(StatesGroup):
    """
    Класс состояний пользователя для процесса регистрации.

    Атрибуты:
        name (State): Состояние ввода имени.
        surename (State): Состояние ввода фамилии.
        patronymic (State): Состояние ввода отчества.
        adress (State): Состояние ввода адреса.
        phone_number (State): Состояние ввода номера телефона.
    """

    name: State = State()
    surename: State = State()
    patronymic: State = State()
    adress: State = State()
    phone_number: State = State()
