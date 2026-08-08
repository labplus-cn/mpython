import time
class Face_recogization(object):
    """ maix人脸识别类"""
    def __init__(self, repl, name="fcr", task_fd=0x300000, task_ld=0x380000, task_fe=0x3d0000, face_num=1, accuracy=85, choice=1):
        self.asr_config = {}
        self.repl = repl
        self.name = name
        self.face_num = face_num
        self.task_fd = task_fd
        self.task_ld = task_ld
        self.task_fe = task_fe
        self.accuracy = accuracy
        self.choice = choice
        cmd = "from face_recognization import Face_recognization"
        self.repl.exec_(cmd)
        # cmd = "{0} = Face_recognization(task_fd={1}, task_ld={2}, task_fe={3}, face_num={4}, accuracy={5})".format(self.name, 
        #     self.task_fd, self.task_ld, self.task_fe, self.face_num, self.accuracy)
        cmd = "{0} = Face_recognization(face_num={1},accuracy={2},choice={3})".format(self.name, self.face_num, self.accuracy, self.choice)
        print(cmd)
        self.repl.exec_(cmd)

    def __repr__(self):
        return self.repl.eval(self.name)

    def add_face(self):
        cmd = "{0}.add_face()" .format(self.name)
        self.repl.exec_(cmd)

    def recognize(self):
        # self.repl.eval("{0}.recognize()".format(self.name))
        time.sleep_ms(5)
        try:
            return eval(self.repl.eval("{}.face_recognize()".format(self.name)))
        except:
            return None

    # def release(self):
    #     cmd = "{0}.asr_release()" .format(self.name)
    #     self.repl.exec_(cmd)        
