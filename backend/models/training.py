from datetime import date
from pydantic import BaseModel
from typing import Optional

class TaskSegmentsCreate(BaseModel):
    position: int
    description: str
    distance: float
    target_time: Optional[float] = None
    average_time: Optional[float] = None
    times: Optional[list[float]] = None

class TrainingSegments(TaskSegmentsCreate):
    id: int
    task_id: int

class TrainingTaskCreate(BaseModel):
    description: str
    task_reps: int
    task_break: int
    segments: list[TaskSegmentsCreate]

class TrainingTask(TrainingTaskCreate):
    segments: list[TrainingSegments]
    id: int

class TrainingCreate(BaseModel):
    date: date
    time: int
    distance: int
    RPE: int
    tasks: list[TrainingTaskCreate]

# Dodajemy klasę dziedziczącą, aby uniknąć potrzeby wysyłania id przez backend
class Training(TrainingCreate):
    tasks: list[TrainingTask]
    id: int
