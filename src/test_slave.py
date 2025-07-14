import sys
import types

# Patch dht and machine modules if not present
dht_mod = types.ModuleType("dht")
setattr(dht_mod, "DHT22", object)
machine_mod = types.ModuleType("machine")
setattr(machine_mod, "Pin", object)
sys.modules.setdefault("dht", dht_mod)
sys.modules.setdefault("machine", machine_mod)

from src.slave import SlaveController  # noqa: E402


class DummySensor:
    def __init__(self, pin):
        self._humidity = 55
        self.measured = False

    def measure(self):
        self.measured = True

    def humidity(self):
        return self._humidity


class DummyPin:
    def __init__(self, pin):
        self.pin = pin


class DummySocket:
    def __init__(self):
        self.sent = []
        self.timeout = None

    def sendto(self, msg, addr):
        self.sent.append((msg, addr))

    def settimeout(self, t):
        self.timeout = t


class DummyFan:
    def __init__(self, pwm_pin):
        self.pwm_pin = pwm_pin
        self.speeds = []

    def set_speed(self, duty):
        self.speeds.append(duty)


def test_slavecontroller_init():
    slave = SlaveController(
        master_ip="1.2.3.4",
        dht_cls=DummySensor,
        pin_cls=DummyPin,
        socket_cls=DummySocket,
        fan_driver_cls=DummyFan,
    )
    assert isinstance(slave.sensor, DummySensor)
    assert isinstance(slave.sock, DummySocket)
    assert isinstance(slave.fan, DummyFan)
    assert slave.master_ip == "1.2.3.4"


def test_set_fan_speed():
    slave = SlaveController(
        master_ip="1.2.3.4",
        dht_cls=DummySensor,
        pin_cls=DummyPin,
        socket_cls=DummySocket,
        fan_driver_cls=DummyFan,
    )
    slave.set_fan_speed(123)
    assert slave.fan.speeds[-1] == 123
    assert slave.current_duty == 123
