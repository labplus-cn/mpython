
import time
class Self_learning_classfier(object):
    """ maix自学习分类"""
    def __init__(self, repl, name="slc", model_addr=0x850000, class_num=1, sample_num=15, threshold=11, choice=1):
        self.asr_config = {}
        self.repl = repl
        self.name = name
        self.model_addr = model_addr
        self.class_num = class_num
        self.sample_num = sample_num
        self.threshold = threshold
        self.choice = choice
        cmd = "from self_learning_classifier import Self_learning_classifier"
        self.repl.exec_(cmd)
        cmd = "{0} = Self_learning_classifier(model_addr={1},class_num={2}, sample_num={3}, threshold={4}, choice={5})".format(self.name, 
        self.model_addr,self.class_num, self.sample_num, self.threshold, self.choice)
        print(cmd)
        self.repl.exec_(cmd)

    def __repr__(self):
        return self.repl.eval(self.name)

    def add_class_img(self):
        cmd = "{0}.add_class_img()" .format(self.name)
        self.repl.exec_(cmd)

    def add_sample_img(self):
        cmd = "{0}.add_sample_img()" .format(self.name)
        self.repl.exec_(cmd)

    def train(self):
        cmd = "{0}.train()" .format(self.name)
        self.repl.exec_(cmd)

    def predict(self):
        time.sleep_ms(5)
        cmd = "{0}.predict()".format(self.name)
        try:
            return eval(self.repl.eval(cmd))
        except:
            return None

    def save_classifier(self, name):
        cmd = "{0}.save_classifier('{1}')".format(self.name, name)
        self.repl.exec_(cmd)

    def load_classifier(self, name):
        cmd = "{0}.load_classifier('{1}')".format(self.name, name)
        self.repl.exec_(cmd)

    def recognize(self):
        return eval(self.repl.eval("{}.face_recognize()".format(self.name)))

    def class_names(self):
        cmd = "{0}.class_names()".format(self.name)
        return eval(self.repl.eval(cmd))

    # def release(self):
    #     cmd = "{0}.asr_release()" .format(self.name)
    #     self.repl.exec_(cmd)  
    

