import pytest
from pydantic import ValidationError
from backend.models.user import UserCreate

def test_only_space_in_password():
    with pytest.raises(ValidationError):
        assert UserCreate(email="a@b.pl", password=" " * 8)

def test_too_long_password_in_bites():
    with pytest.raises(ValidationError):
        assert UserCreate(email="a@b.pl", password="ą" * 37)

def test_password_with_spaces_inside():
    user = UserCreate(email="a@b.pl", password=" john has a plane ")
    assert user.password == " john has a plane "