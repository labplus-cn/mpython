from simple import MQTTClient
from mpython import *
from machine import Timer
import time,network,json

# MQTT服务器地址域名为：183.230.40.39,不变
SERVER = "183.230.40.39"
#设备ID
CLIENT_ID = "deviceID"
#产品ID
username='productID'
#产品APIKey:
password='APIKey'

# wifi参数 
SSID="yourSSID"            #wifi名称
PASSWORD="yourPWD"         #密码
wlan=None

message = {'datastreams':[
{
'id':'sound',
'datapoints':[{'value':0}]
},
{
'id':'light',
'datapoints':[{'value':0}]
}
]} 
  
tim1 = Timer(1)       # 创建定时器

# 本函数实现wifi连接 
def ConnectWifi(ssid=SSID,passwd=PASSWORD):
    global wlan
    wlan=network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.disconnect()
    wlan.connect(ssid,passwd)
  
    while(wlan.ifconfig()[0]=='0.0.0.0'):
        time.sleep(1)
        print('Connecting to network...')
    print('WiFi Connection Successful,Network Config:%s' %str(wlan.ifconfig()))

def pubdata(data):
    j_d = json.dumps(data)
    j_l = len(j_d)
    arr = bytearray(j_l + 3)
    arr[0] = 1 #publish数据类型为json
    arr[1] = int(j_l / 256) # json数据长度 高位字节
    arr[2] = j_l % 256      # json数据长度 低位字节
    arr[3:] = j_d.encode('ascii') # json数据
    return arr

def publishSenser():
  message['datastreams'][0]['datapoints'][0]['value']=sound.read()
  message['datastreams'][1]['datapoints'][0]['value']=light.read()
  c.publish('$dp',pubdata(message))                   #publish报文上传数据点
  print('publish message:',message)
  
 
ConnectWifi()

c = MQTTClient(CLIENT_ID, SERVER,6002,username,password)
c.connect()
print("Connected to %s" % SERVER)
tim1.init(period=1000, mode=Timer.PERIODIC, callback=lambda _:publishSenser())     #每隔一秒上传数据点





