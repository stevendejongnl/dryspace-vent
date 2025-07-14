from unittest import mock
from src.master import MasterController


class DummyFan:
    def __init__(self, pwm_pin):
        self.pwm_pin = pwm_pin
        self.set_speed_calls = []

    def set_speed(self, duty):
        self.set_speed_calls.append(duty)


class DummyController:
    def __init__(self):
        self.calls = []

    def determine_duty_cycle(self, local, remote):
        self.calls.append((local, remote))
        return 123


def test_mastercontroller_init_binds_socket(monkeypatch):
    dummy_fan = DummyFan
    dummy_controller = DummyController
    dummy_sock = mock.MagicMock()
    monkeypatch.setattr("socket.socket", lambda *a, **kw: dummy_sock)
    mc = MasterController(fan_driver_cls=dummy_fan, fan_controller_cls=dummy_controller)
    assert isinstance(mc.fan, DummyFan)
    assert isinstance(mc.controller, DummyController)
    assert mc.sock is dummy_sock
    assert mc.udp_ip == "0.0.0.0"
    assert mc.udp_port == 5005
    assert mc.http_port == 8080
    assert mc.latest == {"remote_humidity": 0, "local_humidity": None, "duty": 0}
    dummy_sock.bind.assert_called_with(("0.0.0.0", 5005))
    dummy_sock.settimeout.assert_called()


def test_start_http_server(monkeypatch):
    # Patch _thread and socket
    thread_started = {}
    monkeypatch.setattr(
        "_thread.start_new_thread",
        lambda f, args: thread_started.setdefault("started", True),
    )
    monkeypatch.setattr("socket.socket", lambda *a, **kw: mock.MagicMock())
    mc = MasterController(fan_driver_cls=DummyFan, fan_controller_cls=DummyController)
    mc.start_http_server()
    assert thread_started["started"]
