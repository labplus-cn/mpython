import socket
import network
import time


host='192.168.3.147'
port = 10000
SSID="yourSSID"
PASSWORD="yourPASSWD"
wlan=None
s=None

def connectWifi(ssid,passwd):
  global wlan
  wlan=network.WLAN(network.STA_IF)                 #create a wlan object
  wlan.active(True)                                 #Activate the network interface
  wlan.disconnect()                                 #Disconnect the last connected WiFi
  wlan.connect(ssid,passwd)                         #connect wifi
  while(wlan.ifconfig()[0]=='0.0.0.0'):
    time.sleep(1)
  return True
  
#Catch exceptions,stop program if interrupted accidentally in the 'try'
try:
  if(connectWifi(SSID,PASSWORD) == True):           #judge whether to connect WiFi
    s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  #create socket
    s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)  #Set the value of the given socket option
    ip=wlan.ifconfig()[0]                           #get ip addr
    while True:
      s.sendto(b'hello DFRobot\r\n',(host,port))    #send data
      time.sleep(1)
except:
  if (s):
    s.close()
  wlan.disconnect()
  wlan.active(False)