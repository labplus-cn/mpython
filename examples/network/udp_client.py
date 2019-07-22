from mpython import *
import socket 

mywifi=wifi()                                           # 创建wifi对象
mywifi.connectWiFi("ssid","password")                   # 连接网络
dst = ("192.168.0.3", 6000)                             # 目的ip地址和端口号

# 捕获异常，如果在"try" 代码块中意外中断，则停止关闭套接字
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)               # 创建UDP的套接字
    s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)              # 设置套接字属性

    while True:
        s.sendto(b'hello message from mPython\r\n',dst)                # 发送数据发送至目的ip
        sleep(2)

# 当捕获异常,关闭套接字、网络
except:
    if (s):
        s.close()
    mywifi.disconnectWiFi()