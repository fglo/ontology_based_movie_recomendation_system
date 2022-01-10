from fastapi import APIRouter
from owlready2 import *

onto = get_ontology("data/system_rekomendacji_extra.owl").load()

router = APIRouter()

@router.get("/owl/actors", tags=["actors"])
async def get_categories():
    global onto
    return [ind.name for ind in list(onto.get_instances_of(onto["Aktor"]))]
    
@router.get("/owl/actors/movies/{moviename}", tags=["actors"])
async def get_actors_of_movie(moviename : str):
    global onto
    actors = []
    for movie in list(onto.get_instances_of(onto["Film"])):
        if movie.name == moviename:
            actors = [actor.name for actor in list(movie.Film_obsadza_Aktor)]
            break
    return actors

@router.get("/owl/actors/series/{seriesname}", tags=["actors"])
async def get_actors_of_series(seriesname : str):
    global onto
    actors = []
    for series in list(onto.get_instances_of(onto["Seria"])):
        if series.name == seriesname:
            actors = [actor.name for actor in list(series.Seria_obsadza_Aktor)]
            break
    return actors

# @router.get("/owl/actors/category/{categoryname}")
# async def get_actors_of_category(categoryname : str):
#     global onto
#     movies = []
#     for series in list(onto.get_instances_of(onto["Seria"])):
#         if series.name == categoryname:
#             movies = [movie for movie in list(series.Seria_zawiera_Film)]
#             break
#     categories = []
#     for movie in movies:
#         for category in list(movie.Film_jest_Kategoria):
#             if category.name not in categories:
#                 categories.append(category.name)
#     return categories

@router.get("/owl/actors/liked/{username}", tags=["actors"])
async def get_users_liked_actors(username : str):
    global onto
    for user in list(onto.get_instances_of(onto["Uzytkownik"])):
        if user.name == username:
            break
    return [actor.name for actor in list(user.Uzytkownik_lubi_Aktor)]

@router.get("/owl/actors/watched/{username}", tags=["actors"])
async def get_users_watched_actors(username : str):
    global onto
    for user in list(onto.get_instances_of(onto["Uzytkownik"])):
        if user.name == username:
            break
    actors = []
    for movie in list(user.Uzytkownik_ogladal_Film):
        for actor in list(movie.Film_obsadza_Aktor):
            if actor.name not in actors:
                actors.append(actor.name)
    return actors