import socket
import network,time
from mpython import *

SSID="yourSSID"       #wifi 名称
PASSWORD="yourPSW"    #wifi 密码
wlan=None

# 本函数实现wifi连接
def ConnectWifi(ssid=SSID,passwd=PASSWORD):
    global wlan
    wlan=network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.disconnect()
    wlan.disconnect()

    wlan.connect(ssid,passwd)
    while(wlan.ifconfig()[0]=='0.0.0.0'):
        time.sleep(1)
        print('Connecting to network...')
    print('WiFi Connection Successful,Network Config:%s' %str(wlan.ifconfig()))

ConnectWifi()

CONTENT = b"""\
HTTP/1.0 200 OK

<meta charset="utf-8">
欢迎使用mPython！你的光线传感器值是:%d
"""

def main():
    s = socket.socket()
    ai = socket.getaddrinfo(wlan.ifconfig()[0], 80)
    print("Bind address info:", ai)
    addr = ai[0][-1]
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(addr)
    s.listen(5)
    print("Listening, connect your browser to http://%s:80/" %addr[0])
    display.DispChar('Connect your browser',0,0,)                       #oled显示掌控板ip地址
    display.DispChar('http://%s' %addr[0],0,16)
    display.show()     
    while True:
        res = s.accept()
        client_s = res[0]
        client_addr = res[1]
        print("Client address:", client_addr)
        print("Client socket:", client_s)
        req = client_s.recv(4096)
        print("Request:")
        print(req)
        client_s.send(CONTENT % light.read())
        client_s.close()

main()