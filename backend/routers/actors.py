from fastapi import APIRouter

from .. import onto

router = APIRouter()

@router.get("/owl/actors", tags=["actors"])
async def get_categories():
    global onto
    return [ind.name for ind in onto.get_actors()]
    
@router.get("/owl/actors/movies/{moviename}", tags=["actors"])
async def get_actors_of_movie(moviename : str):
    global onto
    actors = []
    for movie in onto.get_movies():
        if movie.name == moviename:
            actors = [actor.name for actor in list(movie.Film_obsadza_Aktor)]
            break
    return actors

@router.get("/owl/actors/series/{seriesname}", tags=["actors"])
async def get_actors_of_series(seriesname : str):
    global onto
    actors = []
    for series in onto.get_series():
        if series.name == seriesname:
            actors = [actor.name for actor in list(series.Seria_obsadza_Aktor)]
            break
    return actors

@router.get("/owl/actors/liked/{username}", tags=["actors"])
async def get_users_liked_actors(username : str):
    global onto
    for user in onto.get_users():
        if user.name == username:
            break
    return [actor.name for actor in list(user.Uzytkownik_lubi_Aktor)]

@router.get("/owl/actors/watched/{username}", tags=["actors"])
async def get_users_watched_actors(username : str):
    global onto
    for user in onto.get_users():
        if user.name == username:
            break
    actors = []
    for movie in list(user.Uzytkownik_ogladal_Film):
        for actor in list(movie.Film_obsadza_Aktor):
            if actor.name not in actors:
                actors.append(actor.name)
    return actors