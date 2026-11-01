import bcrypt
import os
import jwt
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

# Tworzymy odczytwać na poziomie modułu który sprawdzi token w żądaniu api
bearer_scheme = HTTPBearer()

# Tajny klucz do podpisywania tokenów ze zmiennej środowiskowej, jest tworzony dla całego serwera
SECRET_KEY = os.environ["FLOWRATE_SECRET_KEY"]

# Algorytm podpisu tokena
ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_DAYS = 30

def hash_password(password):
    # Zamieniamy hasło na bajty
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

def decode_access_token(token):
    try:
        # Dekodujemy token 
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return int(payload["sub"])

    except jwt.InvalidTokenError:
        # Dodajemy infromacje o typie logwania oczekiwanego przez serwer
        raise HTTPException(status_code=401, detail="Invalid or expired token", headers={"WWW-Authenticate": "Bearer"})

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    token = credentials.credentials

    return decode_access_token(token)




