import socket
import time
import dht  # type: ignore[import]
from machine import Pin  # type: ignore[import]
from driver import FanDriver


class SlaveController:
    def __init__(
        self,
        master_ip,
        udp_port=5005,
        dht_pin=4,
        fan_pwm_pin=18,
        dht_cls=None,
        pin_cls=None,
        socket_cls=None,
        fan_driver_cls=None,
    ):
        if dht_cls is None or pin_cls is None:
            dht_cls = dht.DHT22
            pin_cls = Pin
        if socket_cls is None:
            import socket

            socket_cls = socket.socket
        if fan_driver_cls is None:
            from driver import FanDriver

            fan_driver_cls = FanDriver
        self.master_ip = master_ip
        self.udp_port = udp_port
        self.sensor = dht_cls(pin_cls(dht_pin))
        self.sock = socket_cls()
        self.fan = fan_driver_cls(pwm_pin=fan_pwm_pin)
        self.current_duty = 0

    def set_fan_speed(self, duty):
        self.fan.set_speed(duty)
        self.current_duty = duty

    def run(self):
        while True:
            try:
                self.sensor.measure()
                humidity = self.sensor.humidity()
                msg = str(humidity).encode()
                self.sock.sendto(msg, (self.master_ip, self.udp_port))
                print("Sent humidity:", humidity)
                # Wait for master's response with new duty cycle
                self.sock.settimeout(5)
                try:
                    data, _ = self.sock.recvfrom(1024)
                    duty = float(data.decode())
                    self.set_fan_speed(duty)
                    print("Set fan duty from master:", duty)
                except Exception as e:
                    print("No duty received from master or error:", e)
            except Exception as e:
                print("Sensor error:", e)
            time.sleep(5)
