from fastapi import APIRouter, HTTPException, Depends
from backend.repositories.user_repository import user_repository
from backend.models.user import UserCreate, UserLogin
from backend.services.auth import hash_password, verify_password, create_access_token, get_current_user

router = APIRouter()

@router.post("/auth/register")
def register(user_create: UserCreate):
    email = user_create.email.lower().strip()

    user_in_database = user_repository.get_user_by_email(email)

    if user_in_database is not None:
        raise HTTPException(status_code=409, detail="User with this email already exists")

    password_hash = hash_password(user_create.password)

    user_id = user_repository.create_user(email, password_hash)

    return {"id": user_id, "email": email}

@router.post("/auth/login")
def login(user_login: UserLogin):
    email = user_login.email.lower().strip()

    user_in_database = user_repository.get_user_by_email(email)

    if user_in_database is None or not verify_password(user_login.password, user_in_database["password_hash"]):
        raise HTTPException(status_code=401, detail="Incorrect email or password")

    return {"access_token": create_access_token(user_in_database["id"]), "token_type": "bearer"}

@router.get("/auth/me")
def auth_me(user_id: int=Depends(get_current_user)):
    user = user_repository.get_user_by_id(user_id)

    if user is None:
        raise HTTPException(status_code=401, detail="User not found")

    return {"id": user["id"], "email": user["email"]}



    
