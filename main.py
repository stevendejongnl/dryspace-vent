import time

import dht
from machine import Pin

from controller import FanController
from driver import FanDriver

fan = FanDriver(pwm_pin=18)
controller = FanController()
sensor = dht.DHT22(Pin(4))

# Dummy remote humidity value (replace with MQTT or ESP-NOW data)
remote_humidity = 55.0

while True:
    try:
        sensor.measure()
        local_humidity = sensor.humidity()
        duty = controller.determine_duty_cycle(local_humidity, remote_humidity)
        fan.set_speed(duty)
        print("Local humidity:", local_humidity, "| Duty cycle:", duty)
    except Exception as e:
        print("Sensor error:", e)
    time.sleep(5)
