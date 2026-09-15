from datetime import date
from pydantic import BaseModel

class TrainingTask(BaseModel):
    description: str
    task_distance: int
    task_reps: int
    task_target_time: int
    task_break: int
    average_segment_time: int

class TrainingCreate(BaseModel):
    date: date
    time: int
    distance: int
    RPE: int
    tasks: list[TrainingTask]

# Dodajemy klasę dziedziczącą, aby uniknąć potrzeby wysyłania id przez backend
class Training(TrainingCreate):
    id: int
