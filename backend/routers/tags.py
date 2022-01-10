from fastapi import APIRouter
from .. import onto

router = APIRouter()

@router.get("/owl/tags", tags=["tags"])
async def get_categories():
    global onto
    return [ind.name for ind in onto.get_tags()]
    
@router.get("/owl/tags/movies/{moviename}", tags=["tags"])
async def get_tags_of_movie(moviename : str):
    global onto
    actors = []
    for movie in onto.get_movies():
        if movie.name == moviename:
            actors = [actor.name for actor in list(movie.Film_posiada_Tag)]
            break
    return actors