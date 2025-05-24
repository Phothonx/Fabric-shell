import psutil
from imports import *


class Battery(Box):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.batteryInfo = Fabricator(
            poll_from=lambda f: {
                "battery": int(
                    psutil.sensors_battery().percent
                    if psutil.sensors_battery() is not None
                    else 0
                ),
                "secsleft": int(
                    psutil.sensors_battery().secsleft
                    if psutil.sensors_battery() is not None
                    else 0
                ),
                "charging": bool(
                    psutil.sensors_battery().power_plugged
                    if psutil.sensors_battery() is not None
                    else False
                ),
            },
            interval=1000,
        )
