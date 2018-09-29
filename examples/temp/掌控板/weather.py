# weather.py
# 利用板载传感器BME280采集天气数据，通过oled显示出来

from labplus import *
import time

weather = BME280() # 定义一个气压传感器实例
oled = OLED()          # 定义一个oled实例 

while True:
  oled.fill(0)
  oled.show()
  oled.drawStringAt("天气信息",35,0,1)
  oled.drawStringAt("温度",0,20,1)
  oled.drawStringAt("湿度",64,20,1)
  oled.drawStringAt("气压",0,40,1)

  temp = "%d" %  (weather.temperature())   #获取气温值，转为字符串
  humidity = "%d" %  (weather.humidity())    #获取湿度值，转为字符串
  presure = "%0.1f" %  (weather.pressure()/1000)   #获取气压值，转为字符串
  oled.text(temp,35,27,1)
  oled.text(humidity ,97,27,1) 
  oled.text(presure,35,47,1) 
  oled.show()
  time.sleep(1)
  


