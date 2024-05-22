from pydantic import BaseModel

class Department(BaseModel):
    DEPTNO: int
    DNAME: str
    LOC: str