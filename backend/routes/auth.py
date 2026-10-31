from fastapi import APIRouter, HTTPException
from backend.repositories.user_repository import user_repository
from backend.models.user import UserCreate
from backend.services.auth import hash_password

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
