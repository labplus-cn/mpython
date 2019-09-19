
# Blob Detection Example

from mpython import *
from mpython_classroom_kit import *


thresholds = [(0, 80, 15, 127, 15, 127), # generic_red_thresholds
              (0, 80, -70, -10, 0, 30), # generic_green_thresholds
              (0, 80, 23, 60, -88, -44)] # generic_blue_thresholds

# 关闭自动白平衡
camera.set_auto_whitebal(False)     
camera.run(1)

# 找出最大色块函数
def find_max(blobs):
    max_size = 0
    for blob in blobs:
        if blob.w()*blob.h() > max_size:
            max_blob = blob
            max_size = blob.w()*blob.h()
    return max_blob


while True:
    camera.snapshot()  # Take a picture and return the image.
    #  find green blob
    blobs = image.find_blobs([thresholds[1]], pixels_threshold=200, area_threshold=200)
    if blobs:
        # compare maximize blobs
        max_blobs = find_max(blobs)
        print("max_blobs:%s" % max_blobs)
        # draw rect
        image.draw_rectangle(max_blobs.rect())
        # draw cross
        image.draw_cross(max_blobs.cx(), max_blobs.cy())
    lcd.display()
