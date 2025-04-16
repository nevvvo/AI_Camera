from fastapi import APIRouter
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request

from app.camera.capture import start_camera_thread, stop_camera

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/start", response_class=HTMLResponse)
def show_start_page(request: Request):
    return templates.TemplateResponse("start_page.html", {
        "request": request,
        "button_text": "Start camera",
        "action_url": "/start"
    })

@router.post("/start")
def start_camera():
    start_camera_thread()
    return RedirectResponse(url="/stop", status_code=303)

@router.get("/stop", response_class=HTMLResponse)
def show_stop_page(request: Request):
    return templates.TemplateResponse("stop_page.html", {
        "request": request,
        "button_text": "Stop camera",
        "action_url": "/stop"
    })

@router.post("/stop")
def stop():
    stop_camera()
    return RedirectResponse(url="/", status_code=303)

