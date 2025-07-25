# Default configuration for dryspace-vent
CONFIG = {
    # Common
    "role": "master",  # or 'slave'
    # Master
    "udp_ip": "0.0.0.0",
    "udp_port": 5005,
    "http_port": 8080,
    "pwm_pin": 18,
    # Slave
    "master_ip": "192.168.1.100",
    "dht_pin": 4,
    "fan_pwm_pin": 18,
}
