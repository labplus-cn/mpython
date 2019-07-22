from mpython import *
import framebuf,time


images = []
for n in range(1,7):
    with open('scatman.%s.pbm' % n, 'rb') as f:
        f.readline() # Magic number
        f.readline() # Creator comment
        f.readline() # Dimensions
        data = bytearray(f.read())
    fbuf = framebuf.FrameBuffer(data, 128, 64, framebuf.MONO_HLSB)
    images.append(fbuf)

oled.invert(1)
while True:
    for i in images:
        oled.blit(i, 0, 0)
        oled.show()
        time.sleep(0.1)