from fastapi import APIRouter, HTTPException
from server.models.employee import Employee, UpdateEmployee
from server.controllers.employees import (index_employee, list_employees, 
                                          create_employee, replace_employee,
                                          destroy_employee, assign_employee_to_department,
                                          delete_employee_department_relation,
                                          assing_manager,
                                          delete_manager_relationship,
                                          delete_subordinate_relationships)

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
        deptno = response.get("DEPTNO")
        empno = response.get("EMPNO")
        await assign_employee_to_department(empno, deptno)

        if employee.MGR:
            await assing_manager(empno, employee.MGR)
        return response
    raise HTTPException(400, "Employee number must be unique")

@employee.put('/employees/{empno}', response_model=Employee)
async def put_employee(empno:int, data:UpdateEmployee):#TODO tipe of data
    update_data = data.model_dump(exclude_unset=True)  # Only include fields that are provided
    response = await replace_employee(empno, update_data)
    if not response:
        raise HTTPException(404, f"There is no employee with the EMPNO {empno}")
    return response

@employee.delete('/employees/{empno}')
async def delete_employee(empno:int):
    employee_data = await index_employee(empno)
    if not employee_data:
        raise HTTPException(404, f"There is no employee with the EMPNO {empno}")
    mgr = employee_data.get("MGR")

    if mgr:
        await delete_manager_relationship(empno)
    await delete_subordinate_relationships(empno)
    await delete_employee_department_relation(empno)
    

    response = await destroy_employee(empno)
    if not response:
        raise HTTPException(404, f"There is no employee with the id {empno}")
    return "Successfully deleted employee"
    