from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .users import *

router = APIRouter()

templates = Jinja2Templates(directory="frontend/html")

current_user = "user_Filip"

@router.get("/views/users", response_class=HTMLResponse, tags=["views"]) 
async def view_all_users(request: Request):
    global current_user
    return templates.TemplateResponse("users.html", {"request": request, "username": current_user})

@router.get("/views/users/{username}", response_class=HTMLResponse, tags=["views"]) 
async def change_user(request: Request, username : str):
    global current_user
    users = await get_all_users()
    if username in users:
        current_user = username
    return templates.TemplateResponse("users.html", {"request": request, "username": current_user})

@router.get("/views/movies", response_class=HTMLResponse, tags=["views"]) 
async def view_movies_view(request: Request):
    global current_user
    return templates.TemplateResponse("movies.html", {"request": request, "username": current_user})

@router.get("/views/recommended", response_class=HTMLResponse, tags=["views"]) 
async def view_recommended_movies_view(request: Request):
    global current_user
    return templates.TemplateResponse("recommended.html", {"request": request, "username": current_user})

@router.get("/views/movie/{moviename}", response_class=HTMLResponse, tags=["views"]) 
async def view_movie_details(request: Request, moviename : str):
    return templates.TemplateResponse("movie_details.html", {"request": request, "moviename": moviename, "username": current_user})

@router.get("/views/watched", response_class=HTMLResponse, tags=["views"]) 
async def view_watched_movies(request: Request):
    global current_user
    return templates.TemplateResponse("watched.html", {"request": request, "username": current_user})