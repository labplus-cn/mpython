import network
import time

# wifi参数 
SSID="yourSSID"            #wifi名称
PASSWORD="yourPSW"         #密码

# 本函数实现wifi连接 
def connectWifi(ssid,passwd):
  global wlan
  wlan=network.WLAN(network.STA_IF)
  wlan.active(True)
  wlan.disconnect()
  wlan.connect(ssid,passwd)
  while(wlan.ifconfig()[0]=='0.0.0.0'):
    time.sleep(1)
    print("wifi connecting......)
  print("wifi connected!")
  return True