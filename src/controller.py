from typing import Optional


class FanController:
    def __init__(self, humidity_threshold: float = 60.0):
        self.humidity_threshold = humidity_threshold

    def determine_duty_cycle(
        self, local_hum: Optional[float], remote_hum: Optional[float]
    ) -> int:
        if local_hum is None and remote_hum is None:
            return 0
        if (local_hum and local_hum >= self.humidity_threshold) or (
            remote_hum and remote_hum >= self.humidity_threshold
        ):
            return 200
        return 100
