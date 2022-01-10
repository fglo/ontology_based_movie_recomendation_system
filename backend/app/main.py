from fastapi import Depends, FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import uuid
from routers import users, movies, categories, series, actors, tags, views
from shutil import copyfile
from owlready2 import *

owlready2.JAVA_EXE = "C:\\Program Files\\java\\bin\\java.exe"

onto = get_ontology("data/system_rekomendacji_extra.owl").load()
sync_reasoner(onto, infer_property_values = True)

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

@app.get("/owl/classes", tags=["owl"])
async def get_classes():
    global onto

    response = []

    classes = list(onto.classes())
    for c in classes:
        response.append({
            'name': c.name, 
            'parents': [a.name for a in list(c.is_a)], 
            'ancestors': [a.name for a in list(c.ancestors()) if a.name != c.name], 
            'subclasses': [s.name for s in list(c.subclasses())]
        })
    return response

@app.get("/owl/relations", tags=["owl"])
async def get_relations():
    global onto
    response = []

    properties = list(onto.object_properties())
    for p in properties:
        response.append({
            'name': p.name, 
            'domain': [d.name for d in list(p.domain)], 
            'range': [r.name for r in list(p.range)]
        })
    return response

@app.get("/owl/properties", tags=["owl"])
async def get_properties():
    global onto
    response = []

    properties = list(onto.data_properties())
    for p in properties:
        response.append({
            'name': p.name, 
            'domain': [d.name for d in list(p.domain)], 
            # 'range': [r.name for r in list(p.range)] 
        })
    return response

    
@app.get("/owl/individuals", tags=["owl"])
async def get_individuals():
    global onto
    return list(onto.individuals())

@app.get("/owl/individuals/{class_name}", tags=["owl"]) 
async def get_individuals_of_class(class_name : str, individual_name : str):
    global onto, individuals
    classes = list(onto.classes())
    for c in classes:
        if c.name.lowe() == class_name.lower():
            return list(c.instances())
    return []

individuals = {}

@app.post("/owl/individual/{class_name}", tags=["owl"]) 
async def create_individual(class_name : str, individual_name : str):
    global onto, individuals
    classes = list(onto.classes())
    for c in classes:
        if c.name.lower() == class_name.lower():
            id = str(uuid.uuid4())
            individuals[id] = c(individual_name)
            return individuals[id]
    return None