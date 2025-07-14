import sys
import types

# Patch machine module if not present
machine_mod = types.ModuleType("machine")
setattr(machine_mod, "PWM", object)
setattr(machine_mod, "Pin", object)
sys.modules.setdefault("machine", machine_mod)

from src.driver import FanDriver  # noqa: E402


class DummyPWM:
    def __init__(self, pin, freq=25000):
        self.pin = pin
        self.freq = freq
        self.duty_value = None

    def duty(self, value):
        self.duty_value = value


class DummyPin:
    def __init__(self, pin):
        self.pin = pin


def test_fandriver_init_sets_speed(monkeypatch):
    monkeypatch.setattr("src.driver.PWM", DummyPWM)
    monkeypatch.setattr("src.driver.Pin", DummyPin)
    driver = FanDriver(pwm_pin=5)
    assert isinstance(driver.pwm, DummyPWM)
    assert driver.pwm.pin.pin == 5
    assert driver.pwm.freq == 25000
    # Should set speed to 0 on init
    assert driver.pwm.duty_value == 0


def test_fandriver_set_speed(monkeypatch):
    monkeypatch.setattr("src.driver.PWM", DummyPWM)
    monkeypatch.setattr("src.driver.Pin", DummyPin)
    driver = FanDriver(pwm_pin=7)
    driver.set_speed(255)
    # 255 should map to 1023
    assert driver.pwm.duty_value == 1023
    driver.set_speed(128)
    # 128 should map to int(128*1023/255) = 513
    assert driver.pwm.duty_value == 513
