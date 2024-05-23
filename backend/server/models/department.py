from pydantic import BaseModel
from typing import Optional

class Department(BaseModel):
    DEPTNO: int
    DNAME: str
    LOC: str

class UpdateDepartment(BaseModel):
    DNAME: Optional[str] = None
    LOC: Optional[str] = None