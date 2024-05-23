from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

#from server.routes.users import user
from server.routes.employees import employee
from server.routes.departments import department

app = FastAPI()

@app.get('/')
def hello_world():
    return 'Server is running!!!'

origins = ["http://localhost:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#app.include_router(user)
app.include_router(employee)
app.include_router(department)