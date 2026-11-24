from pydantic import BaseModel, Field, validator

MIN_PASSWORD_LENGTH=8

class UserCreate(BaseModel):
    email: str
    password: str = Field(min_length=MIN_PASSWORD_LENGTH)

    # Korzystamy z validator, który sprawdzi nam długość hasła w bajtach, a także to czy hasło to np. nie same spacje
    @validator("password")
    # dodajemy klasę do funkcji
    def validate_password(cls, value: str) -> str:
        if value.strip() == "":
            raise ValueError("Password cannot be only whitespace")
        elif len(value.encode("utf-8")) > 72:
            raise ValueError("Password is too long (max 72 bytes)")
        # zwracamy już sprawdzone hasło
        return value

class UserLogin(BaseModel):
    email: str
    password: str