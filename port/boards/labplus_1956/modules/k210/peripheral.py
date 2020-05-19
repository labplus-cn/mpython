

class Motor:
    """外设电机"""

    def __init__(self, channel, repl):
        self.repl = repl
        if channel not in range(1, 5):
            raise ValueError('channel must in range 0-3')
        # reset the motor to 0
        self._m = "m{0}".format(channel)
        cmd = "{0}.speed=0".format(self._m)
        self.repl.exec_(cmd)
        self._speed = 0

    @property
    def speed(self):
        return self._speed

    @speed.setter
    def speed(self, speed):
        self._speed = speed
        cmd = "{0}.speed={1}".format(self._m, self._speed)
        self.repl.exec_(cmd)


class Light:
    """ 摄像头上的补光灯控制
    Returns
    -------
    [type]
        [description]
    """

    def __init__(self, repl, name='light'):
        self.repl = repl
        self.name = name

    def on(self):
        cmd = "{0}.on()".format(self.name)
        self.repl.exec_(cmd)

    def off(self):
        cmd = "{0}.off()".format(self.name)
        self.repl.exec_(cmd)


class Button:
    """按键控制"""

    def __init__(self, repl, name='btn'):
        self.repl = repl
        self.name = name

    def is_pressed(self):
        return eval(self.repl.eval("{0}.is_pressed()".format(self.name)))

    def was_pressed(self):
        return eval(self.repl.eval("{0}.was_pressed()".format(self.name)))

    def get_presses(self):
        return eval(self.repl.eval("{0}.get_presses()".format(self.name)))


class Ultrasonic:
    """外设超声波"""
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance == None:
            cls.__instance = object.__new__(cls)
        return cls.__instance

    def __init__(self, repl, name='ultrasonic'):
        self.repl = repl
        self.name = name

    @property
    def distance(self):
        return eval(self.repl.eval("{0}.distance".format(self.name)))
