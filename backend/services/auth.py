import bcrypt
import os
import jwt
from datetime import datetime, timedelta, timezone

# Zapisujemy pod tą zmienną secret_key który można domyślnie znaleźć u każdego użytkownika
SECRET_KEY = os.environ["FLOWRATE_SECRET_KEY"]

# Zapisujemy kod formatu hashowania hasła
ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_DAYS = 30

def hash_password(password):
    # Zamieniamy hasło na bity
    password_bytes = password.encode("utf-8")

    # Generujemy losową sól dla hasła jako gotowe zabezpieczenie
    salt = bcrypt.gensalt()

    password_hash = bcrypt.hashpw(password_bytes, salt)

    password_hash = password_hash.decode("utf-8")

    return password_hash

def verify_password(password, password_hash):
    password_bytes = password.encode("utf-8")

    password_hash_bytes = password_hash.encode("utf-8")

    return bcrypt.checkpw(password_bytes, password_hash_bytes)

# Funkcja na podstawie daty utworzenia i wygaśnięcia, SECRET_KEY i algorytmu, tworzy access token dla użytkownika
def create_access_token(user_id):
    data = {"sub": str(user_id), "exp": datetime.now(timezone.utc) + timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)}

    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

