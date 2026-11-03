from fastapi import APIRouter, Depends
from backend.models.personal_best import PersonalBest
from backend.repositories.personal_best_repository import personal_best_repository
from backend.services.auth import get_current_user

router = APIRouter()

@router.get("/personal-bests")
def get_all_personal_bests(user_id: int = Depends(get_current_user)):
    personal_bests = personal_best_repository.get_all_personal_bests(user_id)

    return personal_bests

@router.put("/personal-bests")
def upsert_personal_best(personal_best: PersonalBest, user_id: int = Depends(get_current_user)):
    personal_best_repository.upsert_personal_best(personal_best, user_id)

    return {"updated": personal_best}