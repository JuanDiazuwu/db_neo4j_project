from fastapi import APIRouter, HTTPException
from server.models.department import Department
from server.controllers.departments import (create_department, destroy_department)

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

@department.delete('/departments/{deptno}')
async def delete_department(deptno:int):
    response = await destroy_department(deptno)
    if response:
        return "Successfully deleted department!!!"
    raise HTTPException(400, "Cannot delete department as it has related employees or it does not exist")