from umqtt.simple import MQTTClient
from mpython import *
from machine import Timer
import json

# MQTT服务器地址域名为：183.230.40.39,不变
SERVER = "183.230.40.39"
#设备ID
CLIENT_ID = "deviceID"
#产品ID
username='productID'
#产品APIKey:
password='APIKey'

mywifi=wifi()

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


mywifi.connectWiFi("ssid","password")

c = MQTTClient(CLIENT_ID, SERVER,6002,username,password)
c.connect()
print("Connected to %s" % SERVER)
tim1.init(period=1000, mode=Timer.PERIODIC, callback=lambda _:publishSenser())     #每隔一秒上传数据点