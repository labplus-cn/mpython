from mpython import *
from mpython_classroom_kit import *

# 加载Mnist手写数字 MobileNet模型
model.select_model(model.MNIST_NET)

while True:
    # MobileNet模型计算,返回预测结果
     result = model.predict_net()
     print(result)

