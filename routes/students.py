from fastapi import APIRouter, HTTPException
from database import get_connection
from fastapi import Depends
from routes.auth import get_current_user
from schemas import (
    StudentCreate,
    StudentUpdate,
    StudentResponse,
    StudentListResponse
)
router = APIRouter()

@router.get(
    "/student/{student_id}",
    response_model=StudentResponse
)
def get_student(
    student_id: int,
    current_user = Depends(get_current_user)
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT * FROM students
        WHERE id = ?
        AND user_id = ?
        """,
        (student_id, current_user["user_id"])
    )

    student = cursor.fetchone()

    conn.close()
    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    return {
    "id": student[0],
    "name": student[1],
    "age": student[2],
    "email": student[3]
}
@router.get(
    "/students",
    response_model=StudentListResponse
)
def get_students(
    current_user = Depends(get_current_user)
):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM students WHERE user_id = ?",
        (current_user["user_id"],)
    )

    students = cursor.fetchall()

    students_list = []

    for student in students:
        students_list.append({
            "id": student[0],
            "name": student[1],
            "age": student[2],
            "email": student[3]
        })

    conn.close()

    return {
        "students": students_list
    }


@router.post("/student")
def create_student(
    student: StudentCreate,
    current_user = Depends(get_current_user)
):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
    """
    INSERT INTO students(name, age, email, user_id)
    VALUES (?, ?, ?, ?)
    """,
    (
        student.name,
        student.age,
        student.email,
        current_user["user_id"]
    )
)

    conn.commit()
    conn.close()

    return {
        "message": "Student created successfully"
    }
    
@router.put("/student/{student_id}")
def update_student(
    student_id: int,
    student: StudentUpdate,
    current_user = Depends(get_current_user)
):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
    """
    UPDATE students
    SET name = ?,
        age = ?,
        email = ?
    WHERE id = ?
    AND user_id = ?
    """,
    (
        student.name,
        student.age,
        student.email,
        student_id,
        current_user["user_id"]
    )
)

    conn.commit()

    affected_rows = cursor.rowcount

    conn.close()

    if affected_rows == 0:
     raise HTTPException(
        status_code=404,
        detail="Student not found"
    )

    return {
    "message": "Student updated successfully"
    }

@router.delete("/student/{student_id}")
def delete_student(
    student_id: int,
    current_user = Depends(get_current_user)
):
    
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
    """
    DELETE FROM students
    WHERE id = ?
    AND user_id = ?
    """,
    (
        student_id,
        current_user["user_id"]
    )
)

    conn.commit()

    affected_rows = cursor.rowcount

    conn.close()

    if affected_rows == 0:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )
    return {
        "message": "Student deleted successfully"
    }


@router.get("/students")
def get_students(
    current_user = Depends(get_current_user)
):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
    "SELECT * FROM students WHERE user_id = ?",
    (current_user["user_id"],)
)
    students = cursor.fetchall()

    students_list = []

    for student in students:
     students_list.append({
        "id": student[0],
        "name": student[1],
        "age": student[2],
        "email": student[3]
    })
    conn.close()

    return {
    "students": students_list
    }

