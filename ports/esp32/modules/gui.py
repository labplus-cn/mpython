# gui for mpython
# MIT license; Copyright (c) 2019 Zhang Kaihua(apple_eat@126.com)
import time, math, struct, gc
from framebuf import FrameBuffer
import adafruit_miniqr,gc

class UI():
    def __init__(self, oled):
        self.display = oled

    def ProgressBar(self, x, y, width, height, progress):
        radius = int(height / 2)
        xRadius = x + radius
        yRadius = y + radius
        doubleRadius = 2 * radius
        innerRadius = radius - 2

        self.display.RoundRect(x, y, width, height, radius, 1)
        maxProgressWidth = int((width - doubleRadius + 1) * progress / 100)
        self.display.fill_circle(xRadius, yRadius, innerRadius, 1)
        self.display.fill_rect(xRadius + 1, y + 2, maxProgressWidth, height - 3, 1)
        self.display.fill_circle(xRadius + maxProgressWidth, yRadius, innerRadius, 1)

    def stripBar(self, x, y, width, height, progress, dir=1, frame=1):

        self.display.rect(x, y, width, height, frame)
        if dir:
            Progress = int(progress / 100 * width)
            self.display.fill_rect(x, y, Progress, height, 1)
        else:
            Progress = int(progress / 100 * height)
            self.display.fill_rect(x, y + (height - Progress), width, Progress, 1)


    def qr_code(self,str,x,y,scale=2):
        qr = adafruit_miniqr.QRCode(qr_type=3, error_correct=adafruit_miniqr.L)
        qr.add_data(str.encode())
        qr.make()
        for _y in range(qr.matrix.height):    # each scanline in the height
            for _x in range(qr.matrix.width):
                if qr.matrix[_x, _y]:
            
                    self.display.fill_rect(_x*scale + x,_y*scale + y ,scale,scale,0)
                else:
              
                    self.display.fill_rect(_x*scale + x ,_y*scale + y,scale,scale,1)
        gc.collect()
        
class multiScreen():
    def __init__(self, oled, framelist, w, h):
        self.display = oled
        self.framelist = framelist
        self.width = w
        self.hight = h
        self.frameCount = len(framelist)
        self.activeSymbol = bytearray([0x00, 0x18, 0x3c, 0x7e, 0x7e, 0x3c, 0x18, 0x00])
        self.inactiveSymbol = bytearray([0x00, 0x0, 0x0, 0x18, 0x18, 0x0, 0x0, 0x00])
        self.SymbolInterval = 1

    def drawScreen(self, index):
        self.index = index
        self.display.fill(0)
        self.display.Bitmap(int(64 - self.width / 2), int(0.3 * self.hight), self.framelist[self.index], self.width,
                            self.hight, 1)
        SymbolWidth = self.frameCount * 8 + (self.frameCount - 1) * self.SymbolInterval
        SymbolCenter = int(SymbolWidth / 2)
        starX = 64 - SymbolCenter
        for i in range(self.frameCount):
            x = starX + i * 8 + i * self.SymbolInterval
            y = int(1.1 * self.hight) + 8
            if i == self.index:
                self.display.Bitmap(x, y, self.activeSymbol, 8, 8, 1)
            else:
                self.display.Bitmap(x, y, self.inactiveSymbol, 8, 8, 1)

    def nextScreen(self):
        self.index = (self.index + 1) % self.frameCount
        self.drawScreen(self.index)


class Clock:
    def __init__(self, oled, x, y, radius):  #定义时钟中心点和半径
        self.display = oled
        self.xc = x
        self.yc = y
        self.r = radius

    def settime(self):  #设定时间
        t = time.localtime()
        self.hour = t[3]
        self.min = t[4]
        self.sec = t[5]

    def drawDial(self):  #画钟表刻度
        r_tic1 = self.r - 1
        r_tic2 = self.r - 2

        self.display.circle(self.xc, self.yc, self.r, 1)
        self.display.fill_circle(self.xc, self.yc, 2, 1)

        for h in range(12):
            at = math.pi * 2.0 * h / 12.0
            x1 = round(self.xc + r_tic1 * math.sin(at))
            x2 = round(self.xc + r_tic2 * math.sin(at))
            y1 = round(self.yc - r_tic1 * math.cos(at))
            y2 = round(self.yc - r_tic2 * math.cos(at))
            self.display.line(x1, y1, x2, y2, 1)

    def drawHour(self):  #画时针

        r_hour = int(self.r / 10.0 * 5)
        ah = math.pi * 2.0 * ((self.hour % 12) + self.min / 60.0) / 12.0
        xh = int(self.xc + r_hour * math.sin(ah))
        yh = int(self.yc - r_hour * math.cos(ah))
        self.display.line(self.xc, self.yc, xh, yh, 1)

    def drawMin(self):  #画分针

        r_min = int(self.r / 10.0 * 7)
        am = math.pi * 2.0 * self.min / 60.0

        xm = round(self.xc + r_min * math.sin(am))
        ym = round(self.yc - r_min * math.cos(am))
        self.display.line(self.xc, self.yc, xm, ym, 1)

    def drawSec(self):  #画秒针

        r_sec = int(self.r / 10.0 * 9)
        asec = math.pi * 2.0 * self.sec / 60.0
        xs = round(self.xc + r_sec * math.sin(asec))
        ys = round(self.yc - r_sec * math.cos(asec))
        self.display.line(self.xc, self.yc, xs, ys, 1)

    def drawClock(self):  #画完整钟表
        self.drawDial()
        self.drawHour()
        self.drawMin()
        self.drawSec()

    def clear(self):  #清除
        self.display.fill_circle(self.xc, self.yc, self.r, 0)


class Image():
    def __init__(self):
        self.image_type = None

    def load(self, path, invert=0):
        self.invert = invert
        with open(path, 'rb') as file:
            self.image_type = file.read(2).decode()
            file.seek(0)
            img_arrays = bytearray(file.read())
            if self.image_type == 'P4':
                fb = self._pbm_decode(img_arrays)

            elif self.image_type == 'BM':
                fb = self._bmp_decode(img_arrays)
            else:
                raise TypeError("Unsupported image format {}".format(self.image_type))
            gc.collect()
            return fb

    def _pbm_decode(self, img_arrays):
        next_value = bytearray()
        pnm_header = []
        stat = True
        index = 3
        while stat:
            next_byte = bytes([img_arrays[index]])
            if next_byte == b"#":
                while bytes([img_arrays[index]]) not in [b"", b"\n"]:
                    index += 1
            if not next_byte.isdigit():
                if next_value:
                    pnm_header.append(int("".join(["%c" % char for char in next_value])))
                    next_value = bytearray()
            else:
                next_value += next_byte
            if len(pnm_header) == 2:
                stat = False
            index += 1
        pixel_arrays = img_arrays[index:]
        if self.invert == 1:
            for i in range(len(pixel_arrays)):
                pixel_arrays[i] = (~pixel_arrays[i]) & 0xff
        return FrameBuffer(pixel_arrays, pnm_header[0], pnm_header[1], 3)

    def _bmp_decode(self, img_arrays):

        file_size = int.from_bytes(img_arrays[2:6], 'little')
        offset = int.from_bytes(img_arrays[10:14], 'little')
        width = int.from_bytes(img_arrays[18:22], 'little')
        height = int.from_bytes(img_arrays[22:26], 'little')
        bpp = int.from_bytes(img_arrays[28:30], 'little')
        if bpp != 1:
            raise TypeError("Only support 1 bit color bmp")
        line_bytes_size = (bpp * width + 31) // 32 * 4
        array_size = width * abs(height) // 8
        pixel_arrays = bytearray(array_size)

        if width % 8:
            array_row = width // 8 + 1
        else:
            array_row = width // 8
        array_col = height

        # print("fileSize:{}, offset: {} ".format(file_size, offset))
        # print("width:{}, height: {},bit_count:{},line_bytes_size:{},array_size:{},".format(
        #     width, height, bpp, line_bytes_size, array_size))
        # print('array_col:{},array_row:{}'.format(array_col, array_row))

        for i in range(array_col):
            for j in range(array_row):
                index = -(array_row * (i + 1) - j)
                _offset = offset + i * line_bytes_size + j
                if self.invert == 0:
                    pixel_byte = (~img_arrays[_offset]) & 0xff
                else:
                    pixel_byte = img_arrays[_offset]
                pixel_arrays[index] = pixel_byte

        return FrameBuffer(pixel_arrays, width, height, 3)

