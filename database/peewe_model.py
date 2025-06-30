from config_data.config import DB_PATH
from peewee import (
    CharField,
    IntegerField,
    Model,
    SqliteDatabase,
)


db: SqliteDatabase = SqliteDatabase(DB_PATH)


class BaseModel(Model):
    class Meta:
        database = db


class Client(BaseModel):
    """
    Класс модели таблицы пользователя в SQLite.

    Atributs:
        user_id = ID пользователя. Ключевой атрибут по нему идет поиск в базе данных
        name = имя пользователя
        surename = фамилия пользователя
        patronymic = отчество пользователя
        adress = адресс проживания
        phone_number = контактный номер телефона

    """

    user_id = IntegerField(primary_key=True)
    name = CharField()
    surename = CharField()
    patronymic = CharField()
    adress = CharField(max_length=100)
    phone_number = CharField(max_length=20)

    def __str__(self) -> str:
        """
        Возвращает строковое отображение класса Client.

        Returns:
        str: Отформатированная строка с данными пользователя.
        """
        return (
            f"👤 <b>Профиль пользователя</b>\n"
            f"🆔 ID: <code>{self.user_id}</code>\n"
            f"👨‍💼 Имя: {self.name}\n"
            f"👨‍👩‍👧‍👦 Фамилия: {self.surename}\n"
            f"📛 Отчество: {self.patronymic}\n"
            f"🏠 Адрес: {self.adress}\n"
            f"📞 Телефон: {self.phone_number}"
        )


def create_models() -> None:
    """
    Создаёт таблицы в базе данных для всех моделей, наследующих BaseModel.

    Returns:
        None
    """
    db.create_tables(BaseModel.__subclasses__(), safe=True)
