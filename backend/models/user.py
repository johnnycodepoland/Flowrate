from pydantic import BaseModel, Field

MIN_PASSWORD_LENGTH=8

class UserCreate(BaseModel):
    email: str
    password: str = Field(min_length=MIN_PASSWORD_LENGTH)
