from mpython import *
import bigiot

my_wifi = wifi()
my_wifi.connectWiFi("youruser", "yourpassword")

ID = ""                             # 设备ID
API_KEY = ""                        # 设备APIKEY



def say_cb(msg):                    # 回调函数
    print(msg)
    oled.DispChar("%s,%s" %(msg[0],msg[1]),0,10)    # 显示到oled
    oled.show()
    oled.fill(0)


device = bigiot.Device(ID, API_KEY)         # 构建bigiot 设备

device.say_callback(say_cb)                 # 设置say通讯的回调函数

device.check_in()                           # 登陆