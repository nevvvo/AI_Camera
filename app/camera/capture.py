import threading
import time
import cv2
import mediapipe as mp
from datetime import datetime
from app.db.database import save_photo_to_db
from app.camera.settings import camera_source, area
import os

camera_running = False

def save_photo(image):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename_only = f"photos/photo_{timestamp}.jpg"
    full_path = os.path.join("app/static", filename_only)

    print(f"Saving photo: {full_path}")
    cv2.imwrite(full_path, image)
    save_photo_to_db(filename_only) 

def capture_and_save():
    global camera_running
    detection_start_time = None
    person_in_frame = False
    cap = cv2.VideoCapture(camera_source)
    
    if not cap.isOpened():
        print("Failed to open camera")
        return

    x, y, w, h = area["x"], area["y"], area["width"], area["height"]
    with mp.solutions.face_detection.FaceDetection(min_detection_confidence=0.7) as face_detection:
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
                    print("Человек в кадре 5 секунд — делаем фото")
                    save_photo(frame_resized)
                    detection_start_time = time.time()
            else:
                if person_in_frame:
                    print("Человек ушел из кадра")
                    person_in_frame = False
                detection_start_time = None

            time.sleep(0.5)

    cap.release()

def start_camera_thread():
    global camera_running
    if camera_running:
        return {"message": "Camera already running"}
    camera_running = True
    threading.Thread(target=capture_and_save, daemon=True).start()
    return {"message": "Camera started"}

def stop_camera():
    global camera_running
    if not camera_running:
        return {"message": "Camera was not launched"}
    camera_running = False
    return {"message": "Camera stopped"}
