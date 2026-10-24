from fastapi import APIRouter
from backend.models.personal_best import PersonalBest
from backend.repositories.personal_best_repository import personal_best_repository

router = APIRouter()

@router.get("/personal-bests")
def get_all_personal_bests():
    personal_bests = personal_best_repository.get_all_personal_bests()

    return personal_bests

@router.put("/personal-bests")
def upsert_personal_best(personal_best: PersonalBest):
    personal_best_repository.upsert_personal_best(personal_best)

    return {"updated": personal_best}