from fastapi import APIRouter
from .. import onto

router = APIRouter()

@router.get("/owl/users", tags=["users"])
async def get_all_users():
    global onto
    return [ind.name for ind in onto.get_users()]

@router.post("/owl/users/{username}", tags=["users"]) 
async def create_individual(username : str):
    global onto
    onto.add_user(username)
    onto.sync()