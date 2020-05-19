from k210.image import Image


class Sensor:
    """Sensor 类"""

    # 支持帧大小
    QQQQVGA = 7     # 40x30
    QQQVGA = 8      # 80x60
    QQVGA = 9       # 160x120
    QVGA = 10       # 320x240
    VGA = 11        # 640x480
    # 支持帧格式
    BAYER = 1       # PIXFORMAT_BAYER       /* 1BPP/RAW*/
    RGB565 = 2      # PIXFORMAT_RGB565      /* 2BPP/RGB565*/
    YUV422 = 3      # PIXFORMAT_YUV422      /* 2BPP/YUV422*/
    GRAYSCALE = 4   # PIXFORMAT_GRAYSCALE   /* 1BPP/GRAYSCALE*/
    JPEG = 5        # PIXFORMAT_JPEG        /* JPEG/COMPRESSED*/

    def __init__(self, repl):
        self.repl = repl
        # 在maixpy创建camera的image对象
        cmd = "{0}=sensor.snapshot()".format("camera_img")
        self.repl.exec_(cmd)
        self.img = Image(self.repl, ref="camera_img")

    def snapshot(self):
        """拍摄图像"""
        cmd = "{0}=sensor.snapshot()".format(self.img.name)
        self.repl.exec_(cmd)
        return self.img

    def set_vflip(self, enable):
        """设置垂直镜像"""
        cmd = "sensor.set_vflip({0})" .format(enable)
        self.repl.exec_(cmd)

    def set_hmirror(self, enable):
        """设置水平镜像"""
        cmd = "sensor.set_hmirror({0})" .format(enable)
        self.repl.exec_(cmd)

    def set_framesize(self, framesize, set_regs=True):
        """设置帧大小"""
        cmd = "sensor.set_framesize({0},set_regs={1})" .format(
            framesize, set_regs)
        self.repl.exec_(cmd)

    def set_pixformat(self, framesize, set_regs=True):
        """设置帧格式"""
        cmd = "sensor.set_pixformat({0},set_regs={1})" .format(
            framesize, set_regs)
        self.repl.exec_(cmd)

    def skip_frames(self, n=None, time=None):
        """跳帧"""
        if n is not None and time is None:
            cmd = "sensor.skip_frames({0})" .format(n)
        elif n is None and time is not None:
            cmd = "sensor.skip_frames(time={0})" .format(time)
        elif n is None and time is None:
            cmd = "sensor.skip_frames(time={0})" .format(300)
        elif n is not None and time is not None:
            cmd = "sensor.skip_frames({0},time={1})" .format(n, time)
        self.repl.exec_(cmd)

    def run(self, enable):
        """启动或关闭捕获图像功能(默认经过复位，设置帧大小，设置像素格式后会自动启动摄像头，不调用run(1)也会开始采集图像)"""
        cmd = "sensor.run({0})" .format(enable)
        return eval(self.repl.eval(cmd))

    def shutdown(self, enable):
        """使相机进入比睡眠状态低的功耗模式(但相机必须在被唤醒时重置)"""
        cmd = "sensor.shutdown({0})" .format(enable)
        self.repl.exec_(cmd)

    def width(self):
        """分辨率宽度"""
        cmd = "sensor.width()"
        return eval(self.repl.eval(cmd))

    def height(self):
        """分辨率高度"""
        cmd = "sensor.height()"
        return eval(self.repl.eval(cmd))

    def reset(self, freq=24000000, set_regs=True, dual_buff=False):
        """初始化"""
        cmd = "sensor.reset({0},{1},{2})" .format(freq, set_regs, dual_buff)
        self.repl.exec_(cmd)

    def set_colorbar(self, enable):
        """设置彩条测试模式"""
        cmd = "sensor.set_colorbar({0})" .format(enable)
        return eval(self.repl.eval(cmd))

    def set_brightness(self, brightness):
        """设置亮度"""
        cmd = "sensor.set_brightness({0})" .format(brightness)
        return eval(self.repl.eval(cmd))

    def set_contrast(self, contrast):
        """设置对比度"""
        cmd = "sensor.set_contrast({0})" .format(contrast)
        return eval(self.repl.eval(cmd))

    def set_saturation(self, saturation):
        """设置饱和度"""
        cmd = "sensor.set_saturation({0})" .format(saturation)
        return eval(self.repl.eval(cmd))

    def set_auto_gain(self, enable, gain_db):
        """设置自动增益"""
        cmd = "sensor.set_auto_gain({0},{1})" .format(enable, gain_db)
        self.repl.exec_(cmd)

    def get_gain_db(self):
        """设置自动增益"""
        cmd = "sensor.get_gain_db()"
        return eval(self.repl.eval(cmd))

    def set_auto_whitebal(self, enable):
        """自动白平衡"""
        cmd = "sensor.set_auto_whitebal({0})" .format(enable)
        self.repl.exec_(cmd)

    def set_windowing(self, roi):
        """将相机的分辨率设置为当前分辨率的子分辨率"""
        cmd = "sensor.set_windowing({0})".format(roi)
        return eval(self.repl.eval(cmd))
