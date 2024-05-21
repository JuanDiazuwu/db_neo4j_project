from fastapi import APIRouter, HTTPException
from server.models.department import Department
from server.controllers.departments import (create_department)

department = APIRouter()

#@department.get('/departments/', response_model=Department)
#async def get_department(deptno:int):

#@department.get('/departments', response_model=list[Department])
#async def get_departments():

@department.post('/departments', response_model=Department)
async def post_department(deptno: Department):
    response = await create_department(deptno)
    if response:
        return response
    raise HTTPException(400, "Something went wrong")

#@department.put('/departments/{deptno}')
#async def put_department(deptno:int, data):#TODO type of data

#@department.delete('/departments/{deptno}')
#async def get_department(deptno:int):