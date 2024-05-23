from pydantic import BaseModel

class Employee(BaseModel):
    EMPNO: int          # employee number
    ENAME: str          # employee name
    JOB: str            # job
    MGR: int = None     # manager
    HIREDATE: str       # hire_date = fecha de contratacióm
    SAL: float          # salary
    COMM: float = None  # commission
    DEPTNO: int         # department number

class UpdateEmployee(BaseModel):
    ENAME: str
    JOB: str
    MGR: int = None
    HIREDATE: str
    SAL: float
    COMM: float = None
    DEPTNO: int