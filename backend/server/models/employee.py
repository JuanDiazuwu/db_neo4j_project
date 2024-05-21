from pydantic import BaseModel

class Employee(BaseModel):
    EMPNO: int
    ENAME: str
    JOB: str
    MGR: int = None
    HIREDATE: str
    SAL: float
    COMM: float = None
    DEPTNO: int