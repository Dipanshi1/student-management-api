from fastapi import FastAPI
from routes.students import router as student_router
from routes.auth import router as auth_router
from database import create_tables

app = FastAPI()

@app.on_event("startup")
def startup():
    create_tables()

app.include_router(student_router)
app.include_router(auth_router)

@app.get("/")
def home():
    return {
        "message": "Student Management API"
    }
