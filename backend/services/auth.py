import bcrypt
import os
import jwt
from datetime import datetime, timedelta, timezone

SECRET_KEY = os.environ["FLOWRATE_SECRET_KEY"]
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_DAYS = 30

def hash_password(password):
    password_bytes = password.encode("utf-8")

    salt = bcrypt.gensalt()

    password_hash = bcrypt.hashpw(password_bytes, salt)

    password_hash = password_hash.decode("utf-8")

    return password_hash

def verify_password(password, password_hash):
    password_bytes = password.encode("utf-8")

    password_hash_bytes = password_hash.encode("utf-8")

    return bcrypt.checkpw(password_bytes, password_hash_bytes)

def create_access_token(user_id):
    data = {"sub": str(user_id), "exp": datetime.now(timezone.utc) + timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)}

    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

