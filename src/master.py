import _thread
import json
import socket
import time


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
                print('Connecting to WiFi...')
                wlan.connect(wifi_ssid, wifi_password)
                timeout = 20
                while not wlan.isconnected() and timeout > 0:
                    time.sleep(1)
                    timeout -= 1
                if wlan.isconnected():
                    print('WiFi connected:', wlan.ifconfig())
                else:
                    print('WiFi connection failed!')
        except ImportError:
            print('network module not available (not running on MicroPython ESP32)')

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
            while True:
                conn, addr = s.accept()
                req = conn.recv(1024)
                if b"GET /api/sensors" in req:
                    resp = json.dumps(self.latest)
                    conn.send(
                        b"HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n\r\n"
                        + resp.encode()
                    )
                else:
                    conn.send(b"HTTP/1.1 404 Not Found\r\n\r\n")
                conn.close()

        _thread.start_new_thread(http_server, ())

    def run(self):
        self.start_http_server()
        while True:
            try:
                while True:
                    data, addr = self.sock.recvfrom(1024)
                    try:
                        humidity = float(data.decode())
                        self.slave_humidities[addr[0]] = humidity
                        print(f"Received {humidity:.1f}% from {addr[0]}")
                    except Exception as e:
                        print("Invalid data from", addr, e)
            except Exception:
                pass
            remote_humidity = max(self.slave_humidities.values(), default=0)
            local_humidity = None
            duty = self.controller.determine_duty_cycle(local_humidity, remote_humidity)
            self.fan.set_speed(duty)
            print(f"Remote humidity: {remote_humidity:.1f} | Duty cycle: {duty}")
            self.latest["remote_humidity"] = remote_humidity
            self.latest["local_humidity"] = local_humidity
            self.latest["duty"] = duty
            time.sleep(5)


def main():
    master = MasterController()
    master.run()


if __name__ == "__main__":
    main()
