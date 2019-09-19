from mpython import *
from mpython_classroom_kit import *

# 加载face detect yolo模型
model.select_model(model.FACE_YOLO)

while True:
    # yolo模型计算,返回预测结果
    result = model.detect_yolo()
    print(result)

