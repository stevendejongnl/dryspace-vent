import socket
import time

from controller import FanController
from driver import FanDriver


def run_master():
    UDP_IP = "0.0.0.0"
    UDP_PORT = 5005
    fan = FanDriver(pwm_pin=18)
    controller = FanController()
    slave_humidities = {}
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((UDP_IP, UDP_PORT))
    sock.settimeout(0.1)
    while True:
        try:
            while True:
                data, addr = sock.recvfrom(1024)
                try:
                    humidity = float(data.decode())
                    slave_humidities[addr[0]] = humidity
                    print(f"Received {humidity:.1f}% from {addr[0]}")
                except Exception as e:
                    print("Invalid data from", addr, e)
        except socket.timeout:
            pass
        remote_humidity = max(slave_humidities.values(), default=0)
        local_humidity = None
        duty = controller.determine_duty_cycle(local_humidity, remote_humidity)
        fan.set_speed(duty)
        print(f"Remote humidity: {remote_humidity:.1f} | Duty cycle: {duty}")
        time.sleep(5)
