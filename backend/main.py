from fastapi import Depends, FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import uuid

from shutil import copyfile
from owlready2 import *

from .routers import users, movies, categories, series, actors, tags, views

from . import onto
from . import config

onto.init_onto()

app = FastAPI(title="System rekomendacji filmów",
    version="0.9.2")
app.mount("/css", StaticFiles(directory="frontend/css"), name="css")
app.mount("/js", StaticFiles(directory="frontend/js"), name="js")
app.include_router(users.router)
app.include_router(movies.router)
app.include_router(categories.router)
app.include_router(series.router)
app.include_router(actors.router)
app.include_router(tags.router)
app.include_router(views.router)