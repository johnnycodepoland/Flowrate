from datetime import date
from pydantic import BaseModel

class TrainingTask(BaseModel):
    description: str
    task_distance: int
    task_reps: int
    task_target_time: int
    task_break: int
    average_segment_time: int

class Training(BaseModel):
    id: int
    date: date
    time: int
    distance: int
    RPE: int
    tasks: list[TrainingTask]
