

class Image:
    """Image 类"""

    def __init__(self, repl, ref=None):
        self.repl = repl
        # 没有引用的image,创建一个新的对象
        if ref is None:
            self.name = 'img_{}'.format(hex(id(self)))
            self.repl.exec_('{0}=image.Image()'.format(self.name))
        # 从引用对象创建image
        else:
            self.name = ref

    def __repr__(self):
        # return "<{}>" .format(self.name)
        return self.repl.eval(self.name).decode()

    def __del__(self):
        """销毁image对象"""
        self.repl.exec_("del {}" .format(self.name))
        return "delete {}" .format(self.name)

    ####################
    ## 兼容掌控板绘图相关函数
    ####################

    def DispChar(self, text, x, y, color=(255, 255, 255)):
        cmd = 'Draw_CJK_String("{0}",{1},{2},{3},{4})'.format(
            text, x, y, self.name, color)
        self.repl.exec_(cmd)

    def fill(self, c):
        cmd = "{0}.draw_rectangle(0,0,{1},{2},color={3},fill=True)".format(
            self.name, self.width(), self.height(), c)
        self.repl.exec_(cmd)

    def pixel(self, x, y, c):
        cmd = "{0}.set_pixel({1},{2},{3})".format(self.name, x, y, c)
        self.repl.exec_(cmd)

    def hline(self, x, y, w, c=(255, 255, 255), thickness=1):
        cmd = "{0}.draw_line({1},{2},{3},{4},{5},{6})".format(
            self.name, x, y, x+w, y, c, thickness)
        self.repl.exec_(cmd)

    def vline(self, x, y, h, c=(255, 255, 255), thickness=1):
        cmd = "{0}.draw_line({1},{2},{3},{4},{5},{6})".format(
            self.name, x, y, x, y+h, c, thickness)
        self.repl.exec_(cmd)

    def line(self, x0, y0, x1, y1, c=(255, 255, 255), thickness=1):
        cmd = "{0}.draw_line({1},{2},{3},{4},{5},{6})".format(
            self.name, x0, y0, x1, y1, c, thickness)
        self.repl.exec_(cmd)

    def rect(self, x, y, w, h, c=(255, 255, 255), thickness=1):
        rect = (x, y, w, h)
        cmd = "{0}.draw_rectangle({1},color={2},thickness={3})".format(
            self.name, rect, c, thickness)
        self.repl.exec_(cmd)

    def fill_rect(self, x, y, w, h, c=(255, 255, 255)):
        roi = (x, y, w, h)
        cmd = "{0}.draw_rectangle({1},color={2},thickness=1,fill=True)".format(
            self.name, roi, c)
        self.repl.exec_(cmd)

    ################
    ## OpenMV 相关函数
    ################

    def load(self, path, copy_to_fb=True):
        """加载图片"""
        name = "img_load"
        cmd = "{0}=image.Image('{1}',copy_to_fb={2})" .format(
            name, path, copy_to_fb)
        self.repl.exec_(cmd)
        return Image(self.repl, ref=name)

    def save(self, path, roi=None, quality=50):
        """图片保存"""
        if roi is None:
            cmd = "{0}.save('{1}',quality={2})" .format(
                self.name, path, quality)
        else:
            cmd = "{0}.save('{1}',roi={2},quality={3})" .format(
                self.name, path, roi, quality)
        self.repl.exec_(cmd)

    def width(self):
        """返回图像的宽度"""
        return eval(self.repl.eval("{}.width()".format(self.name)))

    def height(self):
        """返回图像的高度"""
        return eval(self.repl.eval("{}.height()".format(self.name)))

    def format(self):
        """返回图像格式"""
        return eval(self.repl.eval("{}.format()".format(self.name)))

    def size(self):
        """返回图像大小"""
        return eval(self.repl.eval("{}.size()".format(self.name)))

    def clear(self):
        self.repl.exec_("{}.clear()".format(self.name))
        return self

    def pix_to_ai(self):
        cmd = "{0}.pix_to_ai()".format(self.name)
        self.repl.exec_(cmd)

    def binary(self, threshold, invert=False, zero=False):
        cmd = "{0}.binary({1}, invert={2},zero={3})".format(
            self.name, threshold, invert, zero)
        self.repl.exec_(cmd)

    def strech_char(self, de_dark):
        cmd = "{0}.strech_char({1})".format(self.name, de_dark)
        self.repl.exec_(cmd)

    def invert(self):
        cmd = "{0}.invert()".format(self.name)
        self.repl.exec_(cmd)

    def draw_string(self, x, y, text, scale=1, x_spacing=0, y_spacing=0, mono_space=True):
        cmd = "{0}.draw_string({1},{2},'{3}',scale={4},x_spacing={5},y_spacing={6},mono_space={7})" .format(
            self.name, x, y, text, scale, x_spacing, y_spacing, mono_space)
        self.repl.exec_(cmd)

    def draw_line(self, x0, y0, x1, y1, color=(255, 255, 255), thickness=1):
        cmd = "{0}.draw_line({1},{2},{3},{4},color={5},thickness={6})" .format(
            self.name, x0, y0, x1, y1, color, thickness)
        self.repl.exec_(cmd)

    def draw_circle(self, x, y, radius, color=(255, 255, 255), thickness=1, fill=False):
        cmd = "{0}.draw_circle({1},{2},{3},color={4},thickness={5},fill={6})" .format(
            self.name, x, y, radius, color, thickness, fill)
        self.repl.exec_(cmd)

    def draw_rectangle(self, x, y, w, h, color=(255, 255, 255), thickness=1, fill=False):
        rect = (x, y, w, h)
        cmd = "{0}.draw_rectangle({1},color={2},thickness={3},fill={4})" .format(
            self.name, rect, color, thickness, fill)
        self.repl.exec_(cmd)

    def draw_cross(self, x, y, color=(255, 255, 255), size=5, thickness=1):
        cmd = "{0}.draw_cross({1},{2},color={3},size={4},thickness={5})" .format(
            self.name, x, y, color, size, thickness)
        self.repl.exec_(cmd)

    def draw_arrow(self, x0, y0, x1, y1, color=(255, 255, 255), thickness=1):
        cmd = "{0}.draw_arrow({1},{2},{3},{4},color={5},thickness={6})" .format(
            self.name, x0, y0, x1, y1, color, thickness)
        self.repl.exec_(cmd)

    def find_blobs(self, thresholds, invert=False, roi=None, x_stride=2, y_stride=1, area_threshold=10, pixels_threshold=10, merge=False, margin=0):
        if roi is None:
            cmd = "{0}.find_blobs({1},invert={2},x_stride={3},y_stride={4},area_threshold={5},pixels_threshold={6},merge={7},margin={8})".format(
                self.name, thresholds, invert, x_stride, y_stride, area_threshold, pixels_threshold, merge, margin)
        else:
            cmd = "{0}.find_blobs({1},invert={2},roi={3},x_stride={4},y_stride={5},area_threshold={6},pixels_threshold={7},merge={8},margin={9})".format(
                self.name, thresholds, invert, roi, x_stride, y_stride, area_threshold, pixels_threshold, merge, margin)
        return eval(self.repl.eval(cmd))

    def draw_image(self, image, x, y, x_scale=1.0, y_scale=1.0, alpha=256):
        if not isinstance(image, Image):
            raise TypeError("arguments must be Image object")
        cmd = "{0}.draw_image({1},{2},{3},x_scale={4}, y_scale={5}, alpha={6})".format(
            self.name, image.name, x, y, x_scale, y_scale, alpha)
        self.repl.exec_(cmd)

    def get_pixel(self, x, y):
        cmd = "{0}.get_pixel({1},{2})" .format(self.name, x, y)
        return eval(self.repl.eval(cmd))

    def set_pixel(self, x, y, pixel):
        cmd = "{0}.set_pixel({1},{2},{3})" .format(self.name, x, y, pixel)
        self.repl.exec_(cmd)
        return self

    def mean_pool(self, x_div, y_div):
        cmd = "{0}.mean_pool({1},{2})".format(self.name, x_div, y_div)
        self.repl.exec_(cmd)
        return self

    def to_rainbow(self):
        cmd = "{0}.to_rainbow()".format(self.name)
        self.repl.exec_(cmd)
        return self

    ### 从已有的image创建一个新image对象

    def copy(self, roi, copy_to_fb=True):
        """copy :Creates a deep copy of the image object.

        Parameters
        ----------
        roi : [type] is the region-of-interest rectangle (x, y, w, h) to copy from. 
        If not specified, it is equal to the image rectangle which copies the entire image.
        This argument is not applicable for JPEG images.

        Returns
        -------
        [type]
            [description]
        """
        name = 'img_{}'.format(hex(id(self)))
        cmd = "{0} = {1}.copy({2},copy_to_fb={3})".format(
            name, self.name, roi, copy_to_fb)
        self.repl.exec_(cmd)
        return Image(self.repl, ref=name)

    def to_grayscale(self, copy=False, rgb_channel=-1):
        """to_grayscale 
        Converts an image to a grayscale image. This method modifies the underlying image pixels 
        changing the image size in bytes too so it can only be done in place on a Grayscale or an RGB565 image. 
        Otherwise copy must be True to create a new modified image on the heap.

        Returns
        -------
        [type]
            [description]
        """
        name = 'img_{}'.format(hex(id(self)))
        cmd = "{0}={1}.to_grayscale(copy={2},rgb_channel={3})".format(
            name, self.name, copy, rgb_channel)
        self.repl.exec_(cmd)
        return Image(self.repl, ref=name)

    def resize(self, w, h):
        name = 'img_{}'.format(hex(id(self)))
        cmd = "{0}={1}.resize({2},{3})".format(name, self.name, w, h)
        self.repl.exec_(cmd)
        return Image(self.repl, ref=name)

