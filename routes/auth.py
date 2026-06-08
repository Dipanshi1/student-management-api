from datetime import datetime, timedelta
from fastapi import APIRouter, HTTPException
from schemas import UserCreate, UserLogin
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from database import get_connection
from jose import jwt,JWTError
from passlib.context import CryptContext

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)
import os

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="login"
)
def create_access_token(data: dict):

    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=30)

    to_encode.update(
        {"exp": expire}
    )

    return jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )
def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(
    plain_password: str,
    hashed_password: str
):
    return pwd_context.verify(
        plain_password,
        hashed_password
    )

router = APIRouter()

@router.get("/auth-test")
def auth_test():
    return {
        "message": "Auth router working"
    }

@router.post("/register")
def register(user: UserCreate):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE username = ?",
        (user.username,)
    )

    existing_user = cursor.fetchone()

    if existing_user:
        conn.close()

        raise HTTPException(
            status_code=409,
            detail="Username already exists"
        )

    hashed_password = hash_password(user.password)
    cursor.execute(
        "INSERT INTO users (username, password) VALUES (?, ?)",
        (user.username, hashed_password)
    )

    conn.commit()

    user_id = cursor.lastrowid

    conn.close()

    return {
        "message": "User registered successfully",
        "user_id": user_id
    }

@router.post("/login")
def login(user: UserLogin):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM users WHERE username = ?",
        (user.username,)
    )
    existing_user = cursor.fetchone()

    conn.close()
    if not existing_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )
    if not verify_password(user.password, existing_user[2]):
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )
    token = create_access_token(
    {
        "user_id": existing_user[0],
        "username": existing_user[1]
    }
)

    return {
    "access_token": token,
    "token_type": "bearer"
}
def get_current_user(
    token: str = Depends(oauth2_scheme)
):
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        return payload

    except JWTError:

        raise HTTPException(
            status_code=401,
            detail="Token expired or invalid"
        )
@router.get("/profile")
def profile(
    current_user = Depends(get_current_user)
):
    return {
        "user_id": current_user["user_id"],
        "username": current_user["username"]
    }
