from fastapi import APIRouter
from owlready2 import *

onto = get_ontology("data/system_rekomendacji_extra.owl").load()

router = APIRouter()

@router.get("/owl/tags", tags=["tags"])
async def get_categories():
    global onto
    return [ind.name for ind in list(onto.get_instances_of(onto["Tag"]))]
    
@router.get("/owl/tags/movies/{moviename}", tags=["tags"])
async def get_tags_of_movie(moviename : str):
    global onto
    actors = []
    for movie in list(onto.get_instances_of(onto["Film"])):
        if movie.name == moviename:
            actors = [actor.name for actor in list(movie.Film_posiada_Tag)]
            break
    return actors