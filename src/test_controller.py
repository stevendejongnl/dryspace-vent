from src.controller import FanController


def test_determine_duty_cycle_none():
    fc = FanController()
    assert fc.determine_duty_cycle(None, None) == 0


def test_determine_duty_cycle_local_above_threshold():
    fc = FanController(humidity_threshold=60)
    assert fc.determine_duty_cycle(65, 50) == 200


def test_determine_duty_cycle_remote_above_threshold():
    fc = FanController(humidity_threshold=60)
    assert fc.determine_duty_cycle(50, 70) == 200


def test_determine_duty_cycle_both_below_threshold():
    fc = FanController(humidity_threshold=60)
    assert fc.determine_duty_cycle(50, 50) == 100
