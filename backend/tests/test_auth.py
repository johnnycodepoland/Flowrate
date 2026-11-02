import pytest
from backend.services.auth import hash_password, verify_password, create_access_token, decode_access_token
from fastapi import HTTPException

def test_verify_correct_password():
    password_hash = hash_password("kraul123")
    assert verify_password("kraul123", password_hash) is True

def test_verify_wrong_password():
    password_hash = hash_password("kraul123")
    assert verify_password("zlehaslo", password_hash) is False

def test_same_password_gives_different_hashes():
    password_hash = hash_password("kraul123")
    password_hash_2 = hash_password("kraul123")

    assert password_hash != password_hash_2

TOKEN = create_access_token(1)

CHANGED_TOKEN = create_access_token(1) + "x"

def test_decode_access_token():
    assert decode_access_token(TOKEN) == 1

def test_decode_access_token_with_changed_token():
    # Sprawdzamy czy funkcja wywoła wyjątek
    with pytest.raises(HTTPException):
        decode_access_token(CHANGED_TOKEN)