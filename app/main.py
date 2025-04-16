from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.routes import camera_routes, photo_routes
from app.db.database import create_table

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

create_table()

app.include_router(camera_routes.router)
app.include_router(photo_routes.router)
