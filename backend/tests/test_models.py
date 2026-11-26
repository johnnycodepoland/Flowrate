import pytest
from pydantic import ValidationError
from backend.models.training import TaskSegmentsCreate

BASE = {"position": 1, "description": "100", "distance": 100}

def test_task_segment_create_with_both_rest_after_and_send_off():
    with pytest.raises(ValidationError):
        TaskSegmentsCreate(**BASE, rest_after=20, send_off=105)

def test_task_segment_create_with_rest_after_0():
    segment = TaskSegmentsCreate(**BASE, rest_after=0)

    assert segment.rest_after == 0

def test_task_segment_create_with_send_off_lower_than_0():
    with pytest.raises(ValidationError):
        TaskSegmentsCreate(**BASE, send_off=-1)

def test_task_segment_create_without_send_off_and_rest_after():
    segment = TaskSegmentsCreate(**BASE)

    assert segment.rest_after is None
    assert segment.send_off is None

