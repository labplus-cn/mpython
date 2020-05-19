from k210.image import Image


class LCD:
    """LCD 类"""

    # 颜色常量
    BLACK = 0
    NAVY = 3840
    DARKGREEN = 57347
    DARKCYAN = 61187
    MAROON = 120
    PURPLE = 30735
    OLIVE = 57467
    LIGHTGREY = 6342
    DARKGREY = 61307
    BLUE = 7936
    GREEN = 57351
    RED = 248
    MAGENTA = 8184
    YELLOW = 57599
    WHITE = 65535
    ORANGE = 8445
    GREENYELLOW = 58799
    PINK = 8184

    def __init__(self, repl):
        self.repl = repl

    def init(self, type=1, freq=15000000, color=0):
        """初始化显示屏"""
        cmd = "lcd.init({0},{1},{2})" .format(type, freq, color)
        self.repl.exec_(cmd)

    def display(self, image, roi=None, oft=None):
        """在显示屏显示Image"""
        if not isinstance(image, Image):
            raise TypeError("arguments must be Image object")
        if roi is None and oft is None:
            cmd = "lcd.display({0})" .format(image.name)
        elif roi is None and oft is not None:
            cmd = "lcd.display({0},oft={1})" .format(image.name, oft)
        elif roi is not None and oft is None:
            cmd = "lcd.display({0},roi={1})" .format(image.name, roi)
        elif roi is not None and oft is not None:
            cmd = "lcd.display({0},roi={1},oft={})" .format(
                image.name, roi, oft)
        self.repl.exec_(cmd)

    def clear(self, color=(0, 0, 0)):
        """将显示屏清空"""
        cmd = "lcd.clear({0})".format(color)
        self.repl.exec_(cmd)

    def draw_string(self, x, y, text, font_color=248, bg_color=0):
        """在显示屏显示文本"""
        cmd = "lcd.draw_string({0},{1},'{2}',{3},{4})".format(
            x, y, text, font_color, bg_color)
        self.repl.exec_(cmd)

    def width(self):
        """返回显示屏宽度"""
        cmd = "lcd.width()"
        return eval(self.repl.eval(cmd))

    def height(self):
        """返回显示屏高度"""
        cmd = "lcd.height()"
        return eval(self.repl.eval(cmd))

    def deinit(self):
        """释放显示屏"""
        cmd = "lcd.deinit()"
        self.repl.exec_(cmd)

    def rotation(self, dir):
        """设置屏幕方向"""
        cmd = "lcd.rotation({0})" .format(dir)
        return eval(self.repl.eval(cmd))

    def mirror(self, dir):
        """设置显示屏是否镜面显示"""
        cmd = "lcd.mirror({0})" .format(dir)
        return eval(self.repl.eval(cmd))
