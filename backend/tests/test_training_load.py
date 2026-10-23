import pytest
from backend.services.training_load import get_pb_speed, get_critical_speed, segment_intensity, get_segment_speed, segment_reserve_usage, task_density, task_load, training_load
from backend.models.training import TaskSegmentsCreate, TrainingTaskCreate, TrainingCreate
from datetime import date

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

def test_get_segment_speed():
    assert get_segment_speed(SEGMENT) == pytest.approx(1.471, abs=0.001)

SEGMENT_WITHOUT_DISTANCE = TaskSegmentsCreate(position=1, description="text", distance=0, average_time=68)

def test_get_segment_speed_without_distance():
    result = get_segment_speed(SEGMENT_WITHOUT_DISTANCE)
    assert result is None

def test_segment_reserve_usage():
    assert segment_reserve_usage(SEGMENT, get_critical_speed(PERSONAL_BESTS), PERSONAL_BESTS) == pytest.approx(0.393, abs=0.001)

SEGMENT_WITH_AVERAGE_TIME_85_S = TaskSegmentsCreate(position=1, description="text", distance=100, average_time=85)

def test_segment_reserve_usage_with_average_time_85_seconds():
    assert segment_reserve_usage(SEGMENT_WITH_AVERAGE_TIME_85_S, get_critical_speed(PERSONAL_BESTS), PERSONAL_BESTS) == 0

SEGMENT_WITH_AVERAGE_TIME_55_S = TaskSegmentsCreate(position=1, description="text", distance=100, average_time=55)

def test_segment_reserve_usage_with_average_time_55_seconds():
    assert segment_reserve_usage(SEGMENT_WITH_AVERAGE_TIME_55_S, get_critical_speed(PERSONAL_BESTS), PERSONAL_BESTS) == 1

SEGMENT_WITH_50_M_DISTANCE = TaskSegmentsCreate(position=1, description="text", distance=50, average_time=26.5)

def test_segment_reserve_usage_with_50_m_distance():
    assert segment_reserve_usage(SEGMENT_WITH_50_M_DISTANCE, get_critical_speed(PERSONAL_BESTS), PERSONAL_BESTS) == pytest.approx(0.951, abs=0.001)

def test_segment_reserve_usage_without_times():
    result = segment_reserve_usage(SEGMENT_WITHOUT_TIMES, get_critical_speed(PERSONAL_BESTS), PERSONAL_BESTS)
    assert result is None

TASK = TrainingTaskCreate(description="text", task_reps=15, task_break=20, segments=[SEGMENT])

def test_task_density():
    assert task_density(TASK) == pytest.approx(0.785, abs=0.001)

TASK_WITH_60_SECONDS_BREAK = TrainingTaskCreate(description="text", task_reps=15, task_break=60, segments=[SEGMENT])

def test_task_density_with_60_seconds_break():
    assert task_density(TASK_WITH_60_SECONDS_BREAK) == pytest.approx(0.548, abs=0.001)

TASK_WITH_1_REP = TrainingTaskCreate(description="text", task_reps=1, task_break=20, segments=[SEGMENT])

def test_task_density_with_1_rep():
    assert task_density(TASK_WITH_1_REP) == pytest.approx(1)

TASK_WITH_SEGMENT_WITHOUT_TIMES = TrainingTaskCreate(description="text", task_reps=1, task_break=20, segments=[SEGMENT_WITHOUT_TIMES])

def test_task_density_with_segment_without_times():
    result = task_density(TASK_WITH_SEGMENT_WITHOUT_TIMES)
    assert result is None

SECOND_SEGMENT = TaskSegmentsCreate(position=1, description="text", distance=50, average_time=28)

THIRD_SEGMENT = TaskSegmentsCreate(position=2, description="text", distance=100, average_time=85)

TASK_WITH_2_SEGMENTS = TrainingTaskCreate(description="text", task_reps=4, task_break=30, segments=[SECOND_SEGMENT, THIRD_SEGMENT])

def test_task_density_with_2_segments():
    assert task_density(TASK_WITH_2_SEGMENTS) == pytest.approx(0.834, abs=0.001)

TASK_WITHOUT_REPS = TrainingTaskCreate(description="text", task_reps=0, task_break=20, segments=[SEGMENT])

def test_task_density_with_task_without_reps():
    result = task_density(TASK_WITHOUT_REPS)
    assert result is None

TASK_FOR_TESTING_TASK_LOAD = TrainingTaskCreate(description="text", task_reps=15, task_break=20, segments=[SEGMENT])

def test_task_load():
    assert task_load(TASK_FOR_TESTING_TASK_LOAD, get_critical_speed(PERSONAL_BESTS), PERSONAL_BESTS) == pytest.approx(3755, abs=1)

TASK_FOR_TESTING_TASK_LOAD_WITH_LONGER_BREAK = TrainingTaskCreate(description="text", task_reps=15, task_break=60, segments=[SEGMENT])

def test_task_load_with_longer_break():
    assert task_load(TASK_FOR_TESTING_TASK_LOAD_WITH_LONGER_BREAK, get_critical_speed(PERSONAL_BESTS), PERSONAL_BESTS) == pytest.approx(1813, abs=1)

SEGMENT_FOR_TESTING_TASK_LOAD_20_TIMES_100_M = TaskSegmentsCreate(position=1, description="text", distance=100, average_time=85)

TASK_FOR_TESTING_TASK_LOAD_20_TIMES_100_M = TrainingTaskCreate(description="text", task_reps=20, task_break=10, segments=[SEGMENT_FOR_TESTING_TASK_LOAD_20_TIMES_100_M])

def test_task_load_with_task_20_times_100_m():
    assert task_load(TASK_FOR_TESTING_TASK_LOAD_20_TIMES_100_M, get_critical_speed(PERSONAL_BESTS), PERSONAL_BESTS) == pytest.approx(1215, abs=1)

TASK_FOR_TESTING_TASK_LOAD_WITH_1_REP = TrainingTaskCreate(description="text", task_reps=1, task_break=20, segments=[SEGMENT])

def test_task_load_with_1_rep():
    assert task_load(TASK_FOR_TESTING_TASK_LOAD_WITH_1_REP, get_critical_speed(PERSONAL_BESTS), PERSONAL_BESTS) == pytest.approx(94.9, abs=1)

def test_task_load_with_segment_without_times():
    assert task_load(TASK_WITH_SEGMENT_WITHOUT_TIMES, get_critical_speed(PERSONAL_BESTS), PERSONAL_BESTS) == pytest.approx(0)

TRAINING = TrainingCreate(date=date(2026, 10, 23), time=90, distance=2000, RPE=8, tasks=[TASK_FOR_TESTING_TASK_LOAD, TASK_FOR_TESTING_TASK_LOAD_20_TIMES_100_M])

def test_training_load():
    assert training_load(TRAINING, PERSONAL_BESTS) == pytest.approx(4970, abs=1)
    











                        