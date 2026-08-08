
import time
class color_recognization(object):
    """ 颜色识别"""
    def __init__(self, repl, name="_color_recognization", choice=1):
        self.repl = repl
        self.name = name
        self.choice = choice
        cmd = "from color import color_recognization"
        self.repl.exec_(cmd)
      
        cmd = "{0} = color_recognization(choice={1})".format(self.name, self.choice)
        print(cmd)
        self.repl.exec_(cmd)

    def __repr__(self):
        return self.repl.eval(self.name)

    def add_color(self, num):
        cmd = "{0}.add_color({1})" .format(self.name, num)
        self.repl.exec_(cmd)

    def recognize(self):
        time.sleep_ms(5)
        try:
            return eval(self.repl.eval("{}.recognize()".format(self.name)))
        except:
            return None