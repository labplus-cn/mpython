# v831

# from camera import *
# camera = CameraV831(tx=Pin.P16, rx=Pin.P15)



'''
人脸检测
'''

# from camera import *
# camera = CameraV831(tx=Pin.P16, rx=Pin.P15)
# camera.face_detect_init()

# while True:
#     camera.face_detect.recognize()
#     if camera.face_detect.face_num != None:
#         print(str('人脸数量：') + str(camera.face_detect.face_num))
#         print(str('置信度：') + str(camera.face_detect.max_score))
#     time.sleep_ms(20)


'''
数字识别
'''
# from camera import *

# camera = CameraV831(tx=Pin.P16, rx=Pin.P15)
# camera.mnist_init()
# while True:
#     camera.mnist.recognize()
#     if camera.mnist.id != None:
#         print(camera.mnist.id)
#     time.sleep_ms(20)


'''
20类
'''
# from camera import *
# camera = CameraV831(tx=Pin.P16, rx=Pin.P15)
# camera.yolo_detect_init()
# while True:
#     camera.yolo_detect.recognize()
#     if camera.yolo_detect.id != None:
#         print(str('类别：') + str(camera.yolo_detect.category_list[camera.yolo_detect.id]))
#         print(str('置信度：') + str(camera.yolo_detect.max_score))
#     time.sleep_ms(20)


'''
自学习
'''
from mpython import *
from camera import *
import time
index = None
score = None
camera = CameraV831(tx=Pin.P16, rx=Pin.P15)

ID = ['class1', 'class2', 'class3']

camera.self_learning_classifier_init(2, 6)
camera.slc.add_class_img()
camera.slc.add_sample_img()
camera.slc.train()
camera.slc.save_classifier('/root/self_learning_classifier/classes.bin')
camera.slc.load_classifier('/root/self_learning_classifier/classes.bin')

while True:
    camera.slc.predict()
    index = camera.slc.id
    score = camera.slc.max_score
    if index != None and score != None:
        if score >= 0.6:
            print(ID[index])
            print(score)
    time.sleep_ms(20)



'''
qr
'''
# from mpython import *
# from camera import *
# import time
# camera = CameraV831(tx=Pin.P16, rx=Pin.P15)

# camera.qrcode_init()
# camera.qrcode.add_qrcode(1)

# while True:
#     camera.qrcode.recognize()
#     if camera.qrcode.id != None:
#         print(camera.qrcode.id)
#         print(camera.qrcode.info)
#     time.sleep_ms(20)


'''
人脸识别
'''
# from mpython import *
# from camera import *
# import time

# camera = CameraV831(tx=Pin.P16, rx=Pin.P15)
# camera.face_recognize_init(1, 80)
# camera.fcr.add_face()

# while True:
#     camera.fcr.recognize()
#     if camera.fcr.id != None:
#         print(camera.fcr.id)
#         print(camera.fcr.max_score)
#     time.sleep_ms(20)


'''
apriltag
'''
# from mpython import *
# from camera import *
# import time

# camera = CameraV831(tx=Pin.P16, rx=Pin.P15)
# camera.apriltag_init(_choice=1)
# camera.apriltag.set_tag_families(16)
# while True:
#     camera.apriltag.recognize()
#     if camera.apriltag.tag_family != None:
#         print(camera.apriltag.tag_family)
#         print(camera.apriltag.tag_id)
#     time.sleep_ms(20)



'''
LAB颜色提取
'''
# from mpython import *
# from camera import *
# import time

# camera = CameraV831(tx=Pin.P16, rx=Pin.P15)
# camera.color_extracto_init()
# while True:
#     camera.color_extracto.recognize()
#     if camera.color_extracto.LAB_Data[0] != None:
#         print(camera.color_extracto.LAB_Data[0])
#         print(camera.color_extracto.LAB_Data[1])
#         print(camera.color_extracto.LAB_Data[2])
#     time.sleep_ms(20)


'''
颜色识别
'''
# from mpython import *
# from camera import *
# import time

# camera = CameraV831(tx=Pin.P16, rx=Pin.P15)
# camera.color_init()
# camera.color.add_color(2)
# while True:
#     camera.color.recognize()
#     if camera.color.id != None:
#         print(camera.color.id)
#     time.sleep_ms(20)



'''
色块识别
'''
from mpython import *
from camera import *
import time

camera = CameraV831(tx=Pin.P16, rx=Pin.P15)
camera.track_init()
camera.track_set_up([[0, 100, -128, 127, -128, -46], [0, 80, 15, 127, 15, 127], [0, 80, -70, -10, 0, 30], [40, 100, -25, 42, 7, 127]],100)
# while True:
#     camera.track.recognize()
#     if camera.track.x != None:
#         print(camera.track.x)
#         print(camera.track.cx)
#         print(camera.track.code)
#     print('===')
#     time.sleep_ms(20)



'''
yolo 模型
'''
from mpython import *
from camera import *
import time

camera = CameraV831(tx=Pin.P16, rx=Pin.P15)
camera.model_yolo_init(
                labels=["id1","id2",'id3'],            
                model_param="/root/model/opt_int8.param",
                model_bin="/root/model/opt_int8.bin",
                width=224,
                height=224,
                anchors=[4.069214876033057, 4.0495867768595035, 4.842875874125874, 4.626966783216783, 4.279592803030304, 4.3652935606060606, 5.198702830188679, 4.841686320754717, 4.55390625, 4.179166666666666]
                )

while True:
    camera.yolo_model.recognize()
    if camera.yolo_model.id != None:
        if camera.yolo_model.max_score >= 0.5:
            print(camera.yolo_model.id)
            print(camera.yolo_model.max_score)
    time.sleep_ms(10)


'''
Restnet18模型
'''
from mpython import *
from camera import *
import time

camera = CameraV831(tx=Pin.P16, rx=Pin.P15)
camera.model_restnet18_init(
                labels=["id1","id2",'id3'],            
                model_param="/home/model/resnet18_1000_awnn.param",
                model_bin="/home/model/resnet18_1000_awnn.bin",
                width=224,
                height=224)

while True:
    camera.restnet18_model.recognize()
    if camera.restnet18_model.id != None:
        if camera.restnet18_model.max_score >= 0.5:
            print(camera.restnet18_model.id)
            print(camera.restnet18_model.max_score)
    time.sleep_ms(10)


'''
路标
'''
from mpython import *
from camera import *
import time

camera = CameraV831(tx=Pin.P16, rx=Pin.P15)
camera.guidepost_init()
while True:
    camera.guidepost.recognize()
    if camera.guidepost.id != None and camera.guidepost.max_score >= 0.5:
        print(camera.guidepost.id)
        print(camera.guidepost.max_score)
    time.sleep_ms(20)


'''
图像寻线
'''
from mpython import *
from camera import *
import time

camera = CameraV831(tx=Pin.P16, rx=Pin.P15)
camera.find_line_init()

while True:
    camera.find_line.recognize()
    if camera.find_line.line_data != None:
        print(camera.find_line.line_data)
    time.sleep_ms(20)