from config_data.config import DB_PATH
from peewee import (
    CharField,
    IntegerField,
    Model,
    SqliteDatabase,
)


db = SqliteDatabase(DB_PATH)


class BaseModel(Model):
    class Meta:
        database = db


class Client(BaseModel):
    user_id = IntegerField(primary_key=True)
    name = CharField()
    surename = CharField()
    patronymic = CharField()
    adress = CharField(max_length=100)
    phone_number = CharField(max_length=20)

    def __str__(self):
        return (
            f"👤 <b>Профиль пользователя</b>\n"
            f"🆔 ID: <code>{self.user_id}</code>\n"
            f"👨‍💼 Имя: {self.name}\n"
            f"👨‍👩‍👧‍👦 Фамилия: {self.surename}\n"
            f"📛 Отчество: {self.patronymic}\n"
            f"🏠 Адрес: {self.adress}\n"
            f"📞 Телефон: {self.phone_number}"
        )


def create_models():
    db.create_tables(BaseModel.__subclasses__(), safe=True)
