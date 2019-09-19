from mpython import *
from mpython_classroom_kit import *

# 加载20classes yolo模型
model.select_model(model.CLASS_20_YOLO)

while True:
    # yolo模型计算,返回预测结果
    result = model.detect_yolo()
    print(result)

