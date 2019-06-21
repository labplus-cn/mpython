import socket
from mpython import *

host = "172.25.1.63"          # TCP服务端的IP地址
port = 5001                   # TCP服务端的端口
s=None

mywifi=wifi()                 # 创建wifi类


# 捕获异常，如果在"try" 代码块中意外中断，则停止关闭套接字
try:
    mywifi.connectWiFi("ssid","password")                   # WiFi连接，设置ssid 和password
    # mywifi.enable_APWiFi("wifi_name",13)                  # 还可以开启AP模式,自建wifi网络
    ip=mywifi.sta.ifconfig()[0]                             # 获取本机IP地址
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   # 创建TCP的套接字,也可以不给定参数。默认为TCP通讯方式
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # 设置socket属性
    s.connect((host,port))                                  # 设置要连接的服务器端的IP和端口,并连接
    s.send("hello mPython,I am TCP Client")                 # 向服务器端发送数据

    while True:
        data = s.recv(1024)                                 # 从服务器端套接字中读取1024字节数据
        if(len(data) == 0):                                 # 如果接收数据为0字节时,关闭套接字
            print("close socket")
            s.close()                                      
            break
        print(data)
        data=data.decode('utf-8')                         # 以utf-8编码解码字符串
        oled.fill(0)                                      # 清屏
        oled.DispChar(data,0,0)                           # oled显示socket接收数据
        oled.show()                                       # 显示
        s.send(data)                                      # 向服务器端发送接收到的数据

# 当捕获异常,关闭套接字、网络
except:
    if (s):
        s.close()                              
    mywifi.disconnectWiFi()