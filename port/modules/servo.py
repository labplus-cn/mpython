
from machine import SERVO_PWM, Pin

pin_remap_esp32 = (33, 32, 35, 34, 39, 0, 16, 17, 26, 25, 36, 2, -1, 18, 19, 21, 5, -1, -1, 22, 23, -1, -1, 27, 14, 12,
                    13, 15, 4)

class Servo():
    global pin_remap_esp32
    def __init__(self, pin, min_us=750, max_us=2250, actuation_range=180):
        self.min_us = min_us
        self.max_us = max_us
        self.actuation_range = actuation_range
        self.servoPin_id = pin_remap_esp32[pin]
        print(self.servoPin_id)
        self.pwm = SERVO_PWM(Pin(self.servoPin_id), duty = 0, freq = 50)
        
    def write_us(self, us):
        if us < self.min_us or us > self.max_us:
            raise ValueError("us out of range")
        duty = round(us / 20000 * 1023)
        self.pwm.duty(duty)

    def write_angle(self, angle):
        if angle < 0 or angle > self.actuation_range:
            raise ValueError("Angle out of range")
        us_range = self.max_us - self.min_us
        us = self.min_us + round(angle * us_range / self.actuation_range)
        self.write_us(us)