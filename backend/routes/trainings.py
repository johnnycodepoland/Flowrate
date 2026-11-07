import json
from fastapi import APIRouter, HTTPException, Depends
from backend.repositories.training_repository import training_repository
from backend.repositories.personal_best_repository import personal_best_repository
from backend.models.training import TrainingCreate
from backend.services.training_load import calculate_percentage_fatigue
from backend.services.auth import get_current_user

router = APIRouter()

@router.post("/trainings")
def create_training(training: TrainingCreate, user_id: int = Depends(get_current_user)):
    try:
        new_id = training_repository.create_training(training, user_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {"added": training, "id": new_id}

@router.get("/trainings")
def get_all_trainings(user_id: int = Depends(get_current_user)):
    trainings = []

    for training in training_repository.get_all_trainings(user_id):
        training = dict(training)

        trainings.append(training)

    return trainings

@router.get("/trainings/{training_id}")
def get_training_by_id(training_id: int, user_id: int = Depends(get_current_user)):
    training, tasks, segments = training_repository.get_training_by_id(training_id, user_id)

    if training is None:
        raise HTTPException(status_code=404, detail="Training not found")

    training = dict(training)

    training["tasks"] = []

    for i, task in enumerate(tasks):
        task = dict(task)

        task["segments"] = []

        for segment in segments[i]:
            segment = dict(segment)

            if segment["times"]:
                segment["times"] = json.loads(segment["times"])

            task["segments"].append(segment)

        training["tasks"].append(task)

    return training

@router.delete("/trainings/{training_id}")
def delete_training(training_id: int, user_id: int = Depends(get_current_user)):
    training, tasks, segments = training_repository.get_training_by_id(training_id, user_id)

    if training is None:
        raise HTTPException(status_code=404, detail="Training not found")

    training_repository.delete_training(training_id)

    return {"deleted": dict(training)}

@router.put("/trainings/{training_id}")
def update_training(training_id: int, training: TrainingCreate, user_id: int = Depends(get_current_user)):
    # Zapisujemy training pod inną nazwą zmiennej, aby nie nadpisywać już istniejącej zmiennej training
    existing_training, tasks, segments  = training_repository.get_training_by_id(training_id, user_id)

    if existing_training is None:
        raise HTTPException(status_code=404, detail="Training not found")

    training_repository.update_training(training_id, training)

    return {"updated": training}

@router.get("/fatigue")
def get_percentage_fatigue(user_id: int = Depends(get_current_user)):
    personal_bests = personal_best_repository.get_all_personal_bests(user_id)

    trainings_with_tasks = training_repository.get_all_trainings_with_tasks(user_id)

    average_percentage_fatigue, external_percentage_fatigue, internal_percentage_fatigue = calculate_percentage_fatigue(trainings_with_tasks, personal_bests)

    return {"percentage_fatigue": average_percentage_fatigue, "external_percentage_fatigue": external_percentage_fatigue, "internal_percentage_fatigue": internal_percentage_fatigue}