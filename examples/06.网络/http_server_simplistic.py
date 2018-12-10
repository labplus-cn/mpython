import socket
import network,time
from mpython import *

mywifi=wifi()     #实例化wifi类

mywifi.connectWiFi("ssid","password")                  # WiFi连接，设置ssid 和password

CONTENT = b"""\
HTTP/1.0 200 OK

<meta charset="utf-8">
欢迎使用mPython！你的光线传感器值是:%d
"""

def main():
    s = socket.socket()
    ai = socket.getaddrinfo(mywifi.sta.ifconfig()[0], 80)
    print("Bind address info:", ai)
    addr = ai[0][-1]
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(addr)
    s.listen(5)
    print("Listening, connect your browser to http://%s:80/" %addr[0])
    oled.DispChar('Connect your browser',0,0,)                       #oled显示掌控板ip地址
    oled.DispChar('http://%s' %addr[0],0,16)
    oled.show()
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