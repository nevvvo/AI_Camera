import json
import os

# Камера (0 = встроенная)
camera_source = 0

# Путь к папке с фотографиями
photo_path = "app/static/photos"

# Убедимся, что папка для фото существует
if not os.path.exists(photo_path):
    os.makedirs(photo_path)

# Загрузка настроек области из JSON
def load_settings():
    with open("settings.json", "r") as f:
        return json.load(f)

settings = load_settings()
area = settings["area"]  # Пример: {"x": 100, "y": 200, "width": 300, "height": 400}
