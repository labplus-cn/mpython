import urequests
from mpython import *

#连接网络
my_wifi = wifi()
my_wifi.connectWiFi('', '')

# 访问ip地址 api
r = requests.get("http://ip-api.com/json/")
print(r)
print(r.content)  # 返回响应的内容
print(r.text)  # 以文本方式返回响应的内容
print(r.content)
print(r.json())  # 返回响应的json编码内容并转为dict类型

# It's mandatory to close response objects as soon as you finished
# working with them. On MicroPython platforms without full-fledged
# OS, not doing so may lead to resource leaks and malfunction.
r.close()
