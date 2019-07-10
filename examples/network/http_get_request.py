import urequests
from mpython import *

my_wifi = wifi()
my_wifi.connectWiFi('ssid','psw')

# http get方法
r = urequests.get('http://micropython.org/ks/test.html')
# 响应的内容
r.content