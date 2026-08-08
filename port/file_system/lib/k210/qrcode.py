
import time
class QRCode_recognization(object):
    """ 二维码识别类"""
    def __init__(self, repl, name="qrcode", choice=1):
        self.repl = repl
        self.name = name
        self.choice = choice
        cmd = "from qrcode import QRCode_recognization"
        self.repl.exec_(cmd)
      
        cmd = "{0} = QRCode_recognization(choice={1})".format(self.name, self.choice)
        print(cmd)
        self.repl.exec_(cmd)

    def __repr__(self):
        return self.repl.eval(self.name)

    def add_qrcode(self, id):
        cmd = "{0}.add_qrcode({1})" .format(self.name, id)
        self.repl.exec_(cmd)

    def recognize(self):
        time.sleep_ms(5)
        try:
            return eval(self.repl.eval("{}.recognize()".format(self.name)))   
        except:
            return None