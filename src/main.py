try:
    from src import config as config
except ImportError:
    from src import config_default as config
import os
import importlib.util
from src.master import MasterController
from src.slave import SlaveController

# Try to load config.py, fallback to config_default.py
config_path = os.path.join(os.path.dirname(__file__), "config.py")
CONFIG = config.CONFIG

ROLE = CONFIG.get("role", os.getenv("ROLE", "master"))
MASTER_IP = CONFIG.get("master_ip", os.getenv("MASTER_IP", None))


def main():
    if ROLE == "master":
        controller = MasterController(
            udp_ip=CONFIG.get("udp_ip", "0.0.0.0"),
            udp_port=CONFIG.get("udp_port", 5005),
            http_port=CONFIG.get("http_port", 8080),
            pwm_pin=CONFIG.get("pwm_pin", 18),
        )
        controller.run()
    elif ROLE == "slave":
        if not MASTER_IP:
            raise ValueError(
                "MASTER_IP environment variable or config is required for slave role"
            )
        controller = SlaveController(
            MASTER_IP,
            udp_port=CONFIG.get("udp_port", 5005),
            dht_pin=CONFIG.get("dht_pin", 4),
            fan_pwm_pin=CONFIG.get("fan_pwm_pin", 18),
        )
        controller.run()
    else:
        raise ValueError("Unknown ROLE: {}".format(ROLE))


if __name__ == "__main__":
    main()
