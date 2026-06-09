# Student Management API

A FastAPI backend project with:

- User Registration
- JWT Authentication
- Student CRUD Operations
- User-specific Student Records
- Search Students
- Pagination
- SQLite Database

## Tech Stack

- FastAPI
- SQLite
- JWT
- Passlib (bcrypt)
- Uvicorn

## Run Locally

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

## Authentication

- POST /register
- POST /login
- GET /profile

## Students

- POST /student
- GET /student/{id}
- PUT /student/{id}
- DELETE /student/{id}
- GET /students

## Search

GET /students?name=abc

Returns students whose name contains "abc".

## Pagination

GET /students?skip=0&limit=5

Returns first 5 students.

GET /students?skip=5&limit=5

Returns next 5 students.