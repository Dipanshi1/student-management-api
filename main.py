from pydantic import BaseModel, Field
from fastapi import FastAPI
from routes.students import router
from routes.students import router as student_router
from routes.auth import router as auth_router

app = FastAPI()

app.include_router(student_router)
app.include_router(auth_router)


app.include_router(router)


@app.get("/")
def home():
    return {"message": "Hello Dipanshi"}

@app.get("/about")
def about():
    return {"course": "FastAPI Backend Training"}

@app.get("/name")
def name():
    return{"name" : "Dipanshi"}

@app.get("/College Name")
def college_name():
    return{"College Name" : "ABESEC"}

@app.get("/Branch")
def branch():
    return{"Branch" : "Computer Science"}

@app.post("/Register")
def register():
    return{"message" : "user registered"}

@app.get("/user/{user_id}")
def get_user(user_id: int):
    return {user_id : "user_id"}

@app.get("/search")
def search(name: str):
    return {"searched_name": name}


