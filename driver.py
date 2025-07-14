from machine import PWM, Pin


class FanDriver:
    def __init__(self, pwm_pin: int, freq: int = 25000):
        self.pwm = PWM(Pin(pwm_pin), freq=freq)
        self.set_speed(0)

    def set_speed(self, duty: int):
        # Map 0–255 to 0–1023 for ESP32
        self.pwm.duty(int(duty * 1023 / 255))
