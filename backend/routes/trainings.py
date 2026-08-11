from fastapi import APIRouter, HTTPException
from backend.repositories.training_repository import training_repository
from backend.models.training import Training
from backend.services.training_load import calculate_percentage_fatigue

router = APIRouter()

@router.post("/trainings")
def create_training(training: Training):
    try:
        training_repository.create_training(training)
    # Wyłapujemy błąd który zwróciło nam training_service.create_training(training)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {"added": training}

@router.get("/trainings")
def get_all_trainings():
    trainings = []

    for training in training_repository.get_all_trainings():
        training = dict(training)

        trainings.append(training)

    return trainings

@router.get("/trainings/{training_id}")
def get_training_by_id(training_id: int):
    training, tasks = training_repository.get_training_by_id(training_id)

    if training is None:
        raise HTTPException(status_code=404, detail="Training not found")

    training = dict(training)

    training["tasks"] = []

    for task in tasks:
        training["tasks"].append(dict(task))

    return training

@router.delete("/trainings/{training_id}")
def delete_training(training_id: int):
    training, tasks = training_repository.get_training_by_id(training_id)

    if training is None:
        raise HTTPException(status_code=404, detail="Training not found")

    training_repository.delete_training(training_id)

    return {"deleted": dict(training)}

@router.put("/trainings/{training_id}")
def update_training(training_id: int, training: Training):
    # Zapisujemy training pod inną nazwą zmiennej, aby nie nadpisywać już istniejącej zmiennej training
    existing_training, tasks  = training_repository.get_training_by_id(training_id)

    if existing_training is None:
        raise HTTPException(status_code=404, detail="Training not found")

    if training_id != training.id:
        raise HTTPException(status_code=409, detail="Conflict")

    training_repository.update_training(training)

    return {"updated": training}

@router.get("/fatigue")
def get_percentage_fatigue():
    trainings_with_tasks = training_repository.get_all_trainings_with_tasks()

    percentage_fatigue = calculate_percentage_fatigue(trainings_with_tasks)

    return {"percentage_fatigue": percentage_fatigue}