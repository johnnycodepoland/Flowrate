import pytest
from backend.services.training_load import get_pb_speed

PERSONAL_BESTS = {50: 26.1, 100: 58.5, 200: 128.0, 400: 280.0}

def test_pb_speed_exact_distance():
    # Sprawdzamy poprawność danego warunku przy pomocy assert, porównójąc to co zwraca funkcja z tym co powinna zwrócić poprzez pytest.approx, z dokładnościa do 0.001
    assert get_pb_speed(100, PERSONAL_BESTS) == pytest.approx(1.709, abs=0.001)

def test_pb_speed_below_range():
    assert get_pb_speed(25, PERSONAL_BESTS) == pytest.approx(1.916, abs=0.001)
                        
def test_pb_speed_above_range():
    assert get_pb_speed(500, PERSONAL_BESTS) == pytest.approx(1.429, abs=0.001)

def test_pb_speed_interpolated():
    assert get_pb_speed(75, PERSONAL_BESTS) == pytest.approx(1.813, abs=0.001)

                        