import pytest

from controller import FanController


@pytest.fixture
def controller():
    return FanController(humidity_threshold=60)


def test_both_low(controller):
    assert controller.determine_duty_cycle(50, 55) == 100


def test_local_high(controller):
    assert controller.determine_duty_cycle(70, 40) == 200


def test_remote_high(controller):
    assert controller.determine_duty_cycle(45, 61) == 200


def test_both_none(controller):
    assert controller.determine_duty_cycle(None, None) == 0
