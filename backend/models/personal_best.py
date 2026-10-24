from pydantic import BaseModel, Field

class PersonalBest(BaseModel):
    distance: int = Field(gt=0)
    time: float