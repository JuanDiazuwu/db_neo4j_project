from fastapi import APIRouter, HTTPException

from server.models.user import User
from server.controllers.users import create_user

user = APIRouter()
    
@user.post('/users', response_model=User)
async def post_user(user: User):
    response = await create_user(user)
    if response:
        return response
    raise HTTPException(400, "Something went wrong")
