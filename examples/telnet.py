import network
import time
import socket
# wifi参数 
SSID="yourSSID"            #wifi名称
PASSWORD="yourPSW"         #密码

def connectWifi(ssid,passwd):
    global wlan
    wlan=network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.disconnect()
    wlan.connect(ssid,passwd)
    while(wlan.ifconfig()[0]=='0.0.0.0'):
        print("wifi connecting......")
        time.sleep(1)
    print("wifi connected!")
    return True
  
connectWifi(SSID,PASSWORD)
addr_info = socket.getaddrinfo("towel.blinkenlights.nl", 23)
addr = addr_info[0][-1]
s = socket.socket()
s.connect(addr)


while True:
    data = s.recv(500)
    print(str(data, 'utf8'), end='')









