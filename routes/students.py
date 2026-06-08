from fastapi import APIRouter, HTTPException
from schemas import StudentCreate, StudentUpdate
from database import get_connection
router = APIRouter()

@router.get("/test")
def test_route():
    return {
        "message": "Students route working"
    }

@router.get("/student/{student_id}") 
def get_student(student_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM students WHERE id = ?",
        (student_id,)
    )

    student = cursor.fetchone()

    conn.close()
    if student is None:
        raise HTTPException(
            status_code = 404,
            detail="Student not found"
        )

    id, name, age, email = student

    return {
    "id": id,
    "name": name,
    "age": age,
    "email": email
   }

@router.post("/student")
def create_student(student : StudentCreate):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO students (name, age, email) VALUES (?, ?, ?)",
        (student.name, student.age, student.email)
    )
    conn.commit()
    student_id = cursor.lastrowid
    conn.close()
    return {
        "message" : "Student created successfully",
        "student_id": student_id
    }

@router.put("/student/{student_id}")
def update_student(student_id: int, student: StudentUpdate):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE students
        SET name = ?,
            age = ?,
            email = ?
        WHERE id = ?
        """,
        (
            student.name,
            student.age,
            student.email,
            student_id
        )
    )

    conn.commit()
    conn.close()

    return {
        "message": "Student updated successfully"
    }

@router.delete("/student/{student_id}")
def delete_student(student_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM students WHERE id = ?",
        (student_id,)
    )

    conn.commit()
    conn.close()

    return {
        "message": "Student deleted successfully"
    }