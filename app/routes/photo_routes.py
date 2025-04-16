from fastapi import APIRouter, Query, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.db.database import get_filtered_photos, get_db_connection

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    conn = get_db_connection()
    photos = conn.execute(
        "SELECT filename, created_at FROM photos ORDER BY created_at DESC LIMIT 10"
    ).fetchall()
    conn.close()
    photo_urls = [f"/static/{photo['filename']}" for photo in photos]
    return templates.TemplateResponse("root_page.html", {
        "request": request,
        "photo_urls": photo_urls
    })

@router.get("/humans", response_class=HTMLResponse)
def show_photos_with_filter(
    request: Request,
    start_date: str = Query("", description="Формат: YYYY-MM-DD"),
    end_date: str = Query("", description="Формат: YYYY-MM-DD")
):
    photos = get_filtered_photos(start_date, end_date)
    return templates.TemplateResponse("photos_page.html", {
        "request": request,
        "photos": photos
    })
