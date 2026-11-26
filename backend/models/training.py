from datetime import date
from pydantic import BaseModel, Field, confloat, root_validator
from typing import Optional

class TaskSegmentsCreate(BaseModel):
    position: int = Field(ge=1)
    description: str
    distance: float = Field(gt=0)
    target_time: Optional[float] = Field(None, gt=0)
    average_time: Optional[float] = Field(None, gt=0)
    times: Optional[list[confloat(gt=0)]] = None
    rest_after: Optional[float] = Field(None, ge=0)
    send_off: Optional[float] = Field(None, gt=0)

    @root_validator
    def check_rest_after_and_send_off(cls, values):
        rest_after = values.get("rest_after")
        send_off = values.get("send_off")

        if rest_after is not None and send_off is not None:
            raise ValueError("Provide either rest_after or send_off, not both")
        return values

class TrainingSegments(TaskSegmentsCreate):
    id: int
    task_id: int

class TrainingTaskCreate(BaseModel):
    description: str
    task_reps: int = Field(ge=1)
    task_break: int = Field(ge=0)
    segments: list[TaskSegmentsCreate] = Field(min_items=1)

class TrainingTask(TrainingTaskCreate):
    segments: list[TrainingSegments]
    id: int

class TrainingCreate(BaseModel):
    date: date
    # Dodajemy sprawdzenie czy time to liczba całkowita, poza zero
    time: int = Field(gt=0)
    distance: int = Field(ge=0)
    RPE: int = Field(ge=1, le=10)
    tasks: list[TrainingTaskCreate]

# Dodajemy klasę dziedziczącą, aby uniknąć potrzeby wysyłania id przez backend
class Training(TrainingCreate):
    tasks: list[TrainingTask]
    id: int
