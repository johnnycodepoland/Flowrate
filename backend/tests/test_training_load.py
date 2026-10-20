import pytest
from backend.services.training_load import get_pb_speed, get_critical_speed, segment_intensity
from backend.models.training import TaskSegmentsCreate

PERSONAL_BESTS = {50: 26.1, 100: 58.5, 200: 128.0, 400: 280.0}

PERSONAL_BESTS_HIGHER_200_THAN_400 = {50: 26.1, 100: 58.5, 200: 128.0, 400: 250.0}

def test_pb_speed_exact_distance():
    # Sprawdzamy poprawność danego warunku przy pomocy assert, porównójąc to co zwraca funkcja z tym co powinna zwrócić poprzez pytest.approx, z dokładnościa do 0.001
    assert get_pb_speed(100, PERSONAL_BESTS) == pytest.approx(1.709, abs=0.001)

def test_pb_speed_below_range():
    assert get_pb_speed(25, PERSONAL_BESTS) == pytest.approx(1.916, abs=0.001)
                        
def test_pb_speed_above_range():
    assert get_pb_speed(500, PERSONAL_BESTS) == pytest.approx(1.429, abs=0.001)

def test_pb_speed_interpolated():
    assert get_pb_speed(75, PERSONAL_BESTS) == pytest.approx(1.813, abs=0.001)

def test_critical_speed():
    assert get_critical_speed(PERSONAL_BESTS) == pytest.approx(1.316, abs=0.001)

def test_critical_speed_faster_400_than_200():
    result = get_critical_speed(PERSONAL_BESTS_HIGHER_200_THAN_400)
    assert result is None

SEGMENT = TaskSegmentsCreate(position=1, description="text", distance=100, average_time=68)

def test_segment_intensity():
    assert segment_intensity(SEGMENT, get_critical_speed(PERSONAL_BESTS)) == pytest.approx(1.117, abs=0.001)

SEGMENT_WITH_TIMES = TaskSegmentsCreate(position=1, description="text", distance=100, times=[67, 68, 69])

def test_segment_intensity_with_times():
    assert segment_intensity(SEGMENT_WITH_TIMES, get_critical_speed(PERSONAL_BESTS)) == pytest.approx(1.117, abs=0.001)

SEGMENT_WITH_EMPTY_TIMES_AND_WITHOUT_AVERAGE_TIME = TaskSegmentsCreate(position=1, description="text", distance=100, times=[])

def test_segment_intensity_with_empty_times_and_without_average_time():
    result = segment_intensity(SEGMENT_WITH_EMPTY_TIMES_AND_WITHOUT_AVERAGE_TIME, get_critical_speed(PERSONAL_BESTS))
    assert result is None

SEGMENT_WITHOUT_TIMES = TaskSegmentsCreate(position=1, description="text", distance=100)

def test_segment_intensity_without_times():
    result = segment_intensity(SEGMENT_WITHOUT_TIMES, get_critical_speed(PERSONAL_BESTS))
    assert result is None

def test_segment_intensity_with_none_critical_speed():
    result = segment_intensity(SEGMENT, critical_speed=None)
    assert result is None






                        