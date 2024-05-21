from pydantic import BaseModel

class User(BaseModel):
    name: str
    emp_id: int