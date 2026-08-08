from mpython import *
from servo import Servo as SERVO

class Servo:
    def __init__(self,pin):
        self.pin=pin.id
        self.sv=SERVO(self.pin, min_us=500, max_us=2500, actuation_range=180)

    def angle(self,angle):
        self.sv.write_angle(angle)