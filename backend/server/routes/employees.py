from fastapi import APIRouter, HTTPException
from server.models.employee import Employee
from server.controllers.employees import (index_employee, list_employees, 
                                          create_employee, replace_employee,
                                          destroy_employee)

employee = APIRouter()

@employee.get('/employees/{empno}', response_model=Employee)
async def get_employee(empno:int):
    response = await index_employee(empno)
    if response:
        return response
    raise HTTPException(404, f"There is no user with the id {empno}")

@employee.get('/employees', response_model=list[Employee])
async def get_employees():
    response = await list_employees()
    if response is not None:
        return response
    raise HTTPException(404, "No employees found")

@employee.post('/employees')
async def post_employee(employee: Employee):
    response = await create_employee(employee)
    if response:
        return response
    raise HTTPException(400, "Something went wrong")

@employee.put('/employees/{empno}', response_model=Employee)
async def put_employee(empno:int, data):#TODO tipe of data
    pass

@employee.delete('/employees/{empno}')
async def get_employee(empno:int):
    response = await destroy_employee(empno)
    if response:
        return "Successfully deleted employee"
    raise HTTPException(404, f"There is no employee with the id {empno}")