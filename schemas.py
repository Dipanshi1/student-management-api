from pydantic import BaseModel
class StudentCreate(BaseModel):
    name: str
    age: int
    email: str
class StudentUpdate(BaseModel):
    name: str
    age: int
    email: str
class UserCreate(BaseModel):
    username: str
    password: str


class UserLogin(BaseModel):
    username: str
    password: str
    