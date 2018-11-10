# labplus mPython Servo library
# MIT license; Copyright (c) 2018 labplus
# V1.0 Tangliufeng

from mpython import MPythonPin,PinMode
class Servo:
    def __init__(self, pin, min_us=750, max_us=2250, actuation_range=180):
        self.min_us = min_us
        self.max_us = max_us
        self.actuation_range = actuation_range
        self.servoPin=MPythonPin(pin,PinMode.PWM)
        

    def write_us(self, us):
        if us < self.min_us or us > self.max_us:
            raise ValueError("us out of range")
        duty = round(us / 20000 * 1023)
        self.servoPin.write_analog(duty, 50)

    def write_angle(self, angle):
        if angle < 0 or angle > self.actuation_range:
            raise ValueError("Angle out of range")
        us_range = self.max_us - self.min_us
        us = self.min_us + round(angle * us_range / self.actuation_range)
        self.write_us(us)
