import _thread
import json
import socket
import time
from src.logger import log


class MasterController:
    def __init__(
        self,
        udp_ip="0.0.0.0",
        udp_port=5005,
        http_port=8080,
        pwm_pin=18,
        fan_driver_cls=None,
        fan_controller_cls=None,
        wifi_ssid=None,
        wifi_password=None,
    ):
        # WiFi credentials uit config
        try:
            from src.config import CONFIG as USER_CONFIG
        except ImportError:
            from src.config_default import CONFIG as USER_CONFIG
        if wifi_ssid is None:
            wifi_ssid = USER_CONFIG.get("wifi_ssid", "YOUR_WIFI_SSID")
        if wifi_password is None:
            wifi_password = USER_CONFIG.get("wifi_password", "YOUR_WIFI_PASSWORD")

        # ESP32 WiFi setup (MicroPython)
        try:
            import network
            wlan = network.WLAN(network.STA_IF)
            wlan.active(True)
            if not wlan.isconnected():
                log('Connecting to WiFi...', 'INFO')
                wlan.connect(wifi_ssid, wifi_password)
                timeout = 20
                while not wlan.isconnected() and timeout > 0:
                    time.sleep(1)
                    timeout -= 1
                if wlan.isconnected():
                    log('WiFi connected: {}'.format(wlan.ifconfig()), 'INFO')
                else:
                    log('WiFi connection failed!', 'ERROR')
            else:
                log('Already connected to WiFi: {}'.format(wlan.ifconfig()), 'INFO')
        except ImportError:
            log('network module not available (not running on MicroPython ESP32)', 'WARN')

        from src.driver import FanDriver
        from src.controller import FanController

        self.udp_ip = udp_ip
        self.udp_port = udp_port
        self.http_port = http_port
        self.fan = (fan_driver_cls or FanDriver)(pwm_pin=pwm_pin)
        self.controller = (fan_controller_cls or FanController)()
        self.slave_humidities = {}
        self.latest = {"remote_humidity": 0, "local_humidity": None, "duty": 0}
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.udp_ip, self.udp_port))
        self.sock.settimeout(0.1)

    def start_http_server(self):
        def http_server():
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((self.udp_ip, self.http_port))
            s.listen(1)
            log('HTTP server started on {}:{}'.format(self.udp_ip, self.http_port), 'INFO')
            while True:
                conn, addr = s.accept()
                req = conn.recv(1024)
                log('HTTP request from {}: {}'.format(addr, req), 'DEBUG')
                if b"GET /api/sensors" in req:
                    resp = json.dumps(self.latest)
                    conn.send(
                        b"HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n\r\n"
                        + resp.encode()
                    )
                    log('Sent sensor data: {}'.format(resp), 'DEBUG')
                else:
                    conn.send(b"HTTP/1.1 404 Not Found\r\n\r\n")
                    log('404 Not Found sent to {}'.format(addr), 'WARN')
                conn.close()

        _thread.start_new_thread(http_server, ())

    def run(self):
        log('MasterController started', 'INFO')
        self.start_http_server()
        while True:
            try:
                while True:
                    data, addr = self.sock.recvfrom(1024)
                    try:
                        humidity = float(data.decode())
                        self.slave_humidities[addr[0]] = humidity
                        log('Received humidity {:.1f}% from {}'.format(humidity, addr[0]), 'INFO')
                    except Exception as e:
                        log('Invalid data from {}: {}'.format(addr, e), 'ERROR')
            except Exception as e:
                log('Socket receive error: {}'.format(e), 'WARN')
            remote_humidity = max(self.slave_humidities.values(), default=0)
            local_humidity = None
            duty = self.controller.determine_duty_cycle(local_humidity, remote_humidity)
            self.fan.set_speed(duty)
            log('Remote humidity: {:.1f} | Duty cycle: {}'.format(remote_humidity, duty), 'INFO')
            self.latest["remote_humidity"] = remote_humidity
            self.latest["local_humidity"] = local_humidity
            self.latest["duty"] = duty
            time.sleep(5)


def main():
    master = MasterController()
    master.run()


if __name__ == "__main__":
    main()
