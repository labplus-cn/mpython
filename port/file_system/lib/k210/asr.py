
import time
class Maix_asr(object):
    """ maix语音识别类"""
    def __init__(self, repl, name='asr'):
        self.asr_config = {}
        self.repl = repl
        self.name = name
        cmd = "from speech_recognizition import speech_recognize"
        self.repl.exec_(cmd)
        cmd = "{0} = speech_recognize()".format(self.name)
        self.repl.exec_(cmd)

    def __repr__(self):
        return self.repl.eval(self.name)

    def config(self, sets):
        cmd = "{0}.config({1})" .format(self.name, sets)
        self.repl.exec_(cmd)
        print('开始语音识别...')

    def recognize(self):
        # self.repl.eval("{0}.recognize()".format(self.name))
        time.sleep_ms(5)
        try:
            return eval(self.repl.eval("{}.recognize()".format(self.name)))
        except:
            return None

    def release(self):
        cmd = "{0}.asr_release()" .format(self.name)
        self.repl.exec_(cmd)        
