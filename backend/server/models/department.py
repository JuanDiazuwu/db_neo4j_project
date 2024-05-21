from pydantic import BaseModel

class Department(BaseModel):
    deptno: int
    dname: str
    loc: str