import pytest
from backend.services.auth import hash_password, verify_password

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