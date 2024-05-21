from fastapi import FastAPI

#from server.routes.users import user
from server.routes.employees import employee
from server.routes.departments import department

app = FastAPI()

@app.get('/')
def hello_world():
    return 'Server is running!!!'

#app.include_router(user)
app.include_router(employee)
app.include_router(department)