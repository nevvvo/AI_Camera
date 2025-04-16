import json
import os

camera_source = 0

photo_path = "app/static/photos"

if not os.path.exists(photo_path):
    os.makedirs(photo_path)

def load_settings():
    with open("settings.json", "r") as f:
        return json.load(f)

settings = load_settings()
area = settings["area"]