from pydantic import BaseModel
from typing import Optional

class Employee(BaseModel):
    EMPNO: int                  # employee number
    ENAME: str                  # employee name
    JOB: str                    # job
    MGR: Optional[int] = None    # manager
    HIREDATE: str               # hire_date = fecha de contratacióm
    SAL: float                  # salary
    COMM: Optional[float] = None          # commission
    DEPTNO: int                 # department number

class UpdateEmployee(BaseModel):
    ENAME: Optional[str] = None
    JOB: Optional[str] = None
    MGR: Optional[int] = None
    HIREDATE: Optional[str] = None
    SAL: Optional[float] = None
    COMM: Optional[float] = None
    DEPTNO: Optional[int] = None