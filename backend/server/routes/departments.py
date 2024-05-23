from fastapi import APIRouter, HTTPException
from server.models.department import Department, UpdateDepartment
from server.controllers.departments import (index_department, list_departments, 
                                            create_department, replace_department, 
                                            destroy_department)

department = APIRouter()

@department.get('/departments/{deptno}', response_model=Department)
async def get_department(deptno:int):
    response = await index_department(deptno)
    if not response:
        raise HTTPException(404, f"There is no department with the DEPTNO {deptno}")
    return response

@department.get('/departments', response_model=list[Department])
async def get_departments():
    response = await list_departments()
    if not response:
        raise HTTPException(404, "No departments found")
    return response   

@department.post('/departments', response_model=Department)
async def post_department(deptno: Department):
    response = await create_department(deptno)
    if response:
        return response
    raise HTTPException(400, "Department number must be unique")

@department.put('/departments/{deptno}', response_model=Department)
async def put_department(deptno:int, data:UpdateDepartment):
    update_data = data.model_dump(exclude_unset=True)
    response = await replace_department(deptno, update_data)
    if not response:
        raise HTTPException(404, f"There is no department with the DEPTNO {deptno}")
    return response

@department.delete('/departments/{deptno}')
async def delete_department(deptno:int):
    response = await destroy_department(deptno)
    if response:
        return "Successfully deleted department!!!"
    raise HTTPException(400, "Cannot delete department as it has related employees or it does not exist")