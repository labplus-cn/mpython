
from k210.image import Image


class KPU_net:
    """ kpu_net 类"""

    def __init__(self, repl, ref=None):
        self.repl = repl
        if ref is None:
            self.name = 'kpu_net_{}'.format(hex(id(self)))
        else:
            self.name = ref

    def __del__(self):
        """销毁kpu_net对象"""
        self.repl.exec_("del {}" .format(self.name))
        return "delete {}" .format(self.name)

    def __repr__(self):
        return self.repl.eval(self.name)

    def model_path(self):
        cmd = "{0} = model_path()" .format(self.name)
        return self.repl.eval(cmd)

    def model_addr(self):
        cmd = "{0} = model_addr()" .format(self.name)
        return eval(self.repl.eval(cmd))


class kpu_yolo2_find:

    def __init__(self, result):
        self._result = result

    def __repr__(self):
        return "{\"x\":%d, \"y\":%d, \"w\":%d, \"h\":%d, \"value\":%d, \"classid\":%d, \"index\":%d, \"objnum\":%d}" % (
            self._result['x'],
            self._result['y'],
            self._result['w'],
            self._result['h'],
            self._result['value'],
            self._result['classid'],
            self._result['index'],
            self._result['objnum'])

    def x(self):
        return self._result['x']

    def y(self):
        return self._result['y']

    def w(self):
        return self._result['w']

    def h(self):
        return self._result['h']

    def rect(self):
        return (self._result['x'],
                self._result['y'],
                self._result['w'],
                self._result['h'])


class KPU:
    def __init__(self, repl):
        self.repl = repl

    def load(self, path):
        """加载模型"""
        task_name = "kpu_task"
        if isinstance(path, int):
            cmd = "{0}=KPU.load({1})".format(task_name, path)
        if isinstance(path, str):
            cmd = "{0}=KPU.load('{1}')".format(task_name, path)
        self.repl.exec_(cmd)
        return KPU_net(self.repl, task_name)

    def init_yolo2(self, kpu_net, threshold, nms_value, anchor_num, anchor):
        """ 初始化yolo2网络 """
        if not isinstance(kpu_net, KPU_net):
            raise TypeError("argument #1 must be KPU_net object")
        cmd = "KPU.init_yolo2({0},{1},{2},{3},{4})".format(
            kpu_net.name, threshold, nms_value, anchor_num, anchor)
        return eval(self.repl.eval(cmd))

    def run_yolo2(self, kpu_net, image_t):
        """ 运行yolo2网络 """
        if not isinstance(kpu_net, KPU_net):
            raise TypeError("argument #1 must be KPU_net object")
        if not isinstance(image_t, Image):
            raise TypeError("argument #2 must be Image object")
        cmd = "KPU.run_yolo2({0},{1})".format(kpu_net.name, image_t.name)
        return eval(self.repl.eval(cmd))

    def deinit(self, kpu_net):
        """释放kpu"""
        if not isinstance(kpu_net, KPU_net):
            raise TypeError("argument must be KPU_net object")
        cmd = "KPU.deinit({0})" .format(kpu_net.name)
        return eval(self.repl.eval(cmd))

    def forward(self, kpu_net, img, out_index=0):
        if not isinstance(kpu_net, KPU_net):
            raise TypeError("argument #1 must be KPU_net object")
        if not isinstance(img, Image):
            raise TypeError("argument #2 must be Image object")
        cmd = "fmap=KPU.forward({0},{1},{2})".format(
            kpu_net.name, img.name, out_index)
        self.repl.exec_(cmd)
        return eval(self.repl.eval("fmap[:]"))
