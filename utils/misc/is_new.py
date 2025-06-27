import os
import json
from config_data.config import database_file_path


def is_new(user_id):
    id = str(user_id)

    if not os.path.exists(database_file_path):
        return True
    try:
        with open(database_file_path, "r", encoding="utf-8") as f:
            users_data = json.load(f)

        return id not in users_data

    except json.JSONDecodeError:
        # Файл существует, но невалидный JSON
        print("Ошибка: повреждённый файл базы данных.")
        return None
    except Exception as e:
        print(f"Непредвиденная ошибка: {e}")
        return None
