from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi import FastAPI, Request, Query
from datetime import datetime
import mediapipe as mp
import threading
import sqlite3
import uvicorn
import json
import time
import cv2
import os


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

camera_source = 0  
photo_path = "static/photos"  
camera_running = False
last_camera_start_time = 0
mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils

if not os.path.exists(photo_path):
    os.makedirs(photo_path)

def load_settings():
    with open("settings.json", "r") as f:
        return json.load(f)
    
settings = load_settings()
area = settings["area"]
x, y, w, h = area["x"], area["y"], area["width"], area["height"]


def get_db_connection():
    conn = sqlite3.connect('db/photos.db') 
    conn.row_factory = sqlite3.Row
    return conn

def create_table():
    conn = get_db_connection()
    conn.execute("""
    CREATE TABLE IF NOT EXISTS photos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        filename TEXT NOT NULL,
        created_at TEXT NOT NULL
    )
    """)
    conn.commit()
    conn.close()

def clear_db():
    conn = sqlite3.connect('db/photos.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM photos")
    conn.commit()
    conn.close()

def save_photo_to_db(filename):
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn = get_db_connection()
    conn.execute("INSERT INTO photos (filename, created_at) VALUES (?, ?)", (filename, created_at))
    conn.commit()
    conn.close()

create_table() 

def save_photo(image):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{photo_path}/photo_{timestamp}.jpg"
    print(f"Saving photo: {filename}")
    cv2.imwrite(filename, image)
    save_photo_to_db(filename)


def capture_and_save():
    global camera_running
    detection_start_time = None
    person_in_frame = False
    cap = cv2.VideoCapture(camera_source)
    if not cap.isOpened():
        print("Failed to open camera")
        return

    with mp_face_detection.FaceDetection(min_detection_confidence=0.7) as face_detection:
        while camera_running:
            ret, frame = cap.read()
            if not ret:
                print("Failed to capture frame")
                break

            frame_resized = cv2.resize(frame, (1280, 960))
            area_frame = frame_resized[y:y+h, x:x+w]
            rgb_frame = cv2.cvtColor(area_frame, cv2.COLOR_BGR2RGB)
            results = face_detection.process(rgb_frame)

            if results.detections:
                if not person_in_frame:
                    print("Человек обнаружен в кадре")
                    person_in_frame = True

                if detection_start_time is None:
                    detection_start_time = time.time()

                elif time.time() - detection_start_time >= 5:
                        print("Человек находится в кадре 5 секунд - делаем фото")
                        save_photo(frame_resized)
                        detection_start_time = time.time()

            else:
                if person_in_frame:
                    print("Человек ушел из кадра")
                    person_in_frame = False
                detection_start_time = None
            time.sleep(0.5) 

    cap.release()


def get_filtered_photos(start_date: str = "", end_date: str = ""):
    conn = get_db_connection()
    if start_date and end_date:
        try:
            start_date_obj = datetime.strptime(start_date, '%Y-%m-%d')
            end_date_obj = datetime.strptime(end_date, '%Y-%m-%d')
            photos = conn.execute(
                "SELECT filename, created_at FROM photos WHERE created_at BETWEEN ? AND ? ORDER BY created_at DESC",
                (start_date_obj, end_date_obj)
            ).fetchall()
        except ValueError:
            photos = []

    else:
        photos = conn.execute("SELECT filename, created_at FROM photos ORDER BY created_at DESC LIMIT 10").fetchall()

    conn.close()
    return photos

@app.get("/start", response_class=HTMLResponse)
def show_start_page():
    return templates.TemplateResponse("start_page.html", {"request": {}, "button_text": "Start camera", "action_url": "/start"})

@app.post("/start", summary="Launch the camera", response_description="Camera launch status")
def start_camera():
    global camera_running
    if camera_running:
        return {"message": "Camera already running"}

    camera_running = True
    threading.Thread(target=capture_and_save, daemon=True).start()
    return {"message": "Camera started"}

@app.get("/stop", response_class=HTMLResponse)
def show_stop_page():
    return templates.TemplateResponse("stop_page.html", {"request": {}, "button_text": "Stop camera", "action_url": "/stop"})

@app.post("/stop", summary="Stop the camera", response_description="Camera stop status")
def stop_camera():
    global camera_running
    if not camera_running:
        return {"message": "Camera was not launched"}

    camera_running = False
    return {"message": "Camera stopped"}

@app.get("/humans", response_class=HTMLResponse)
async def show_photos_with_filter(request: Request, start_date: str = Query("", description="Дата начала в формате YYYY-MM-DD"), end_date: str = Query("", description="Дата конца в формате YYYY-MM-DD")):
    photos = get_filtered_photos(start_date, end_date)
    return templates.TemplateResponse("photos_page.html", {"request": request, "photos": photos})

@app.get("/", response_class=HTMLResponse)
def read_root():
    conn = get_db_connection()
    photos = conn.execute("SELECT filename, created_at FROM photos ORDER BY created_at DESC LIMIT 10").fetchall()
    conn.close()
    photo_urls = [f"/{photo['filename']}" for photo in photos]
    return templates.TemplateResponse("root_page.html", {"request": {}, "photo_urls": photo_urls})

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
