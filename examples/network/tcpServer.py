import socket
from mpython import *

port=5001                   # TCP服务端的端口,range0~65535
listenSocket=None              

mywifi=wifi()               # 创建wifi类

# 捕获异常，如果在"try" 代码块中意外中断，则停止关闭套接字
try:
    mywifi.connectWiFi("ssid","password")                                   # WiFi连接，设置ssid 和password
    # mywifi.enable_APWiFi("wifi_name",13)                                  # 还可以开启AP模式,自建wifi网络
    ip= mywifi.sta.ifconfig()[0]                                            # 获取本机IP地址
    listenSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)        # 创建socket,不给定参数默认为TCP通讯方式
    listenSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)      # 设置套接字属性参数
    listenSocket.bind((ip,port))                                            # 绑定ip和端口
    listenSocket.listen(3)                                                  # 开始监听并设置最大连接数
    print ('tcp waiting...')
    oled.DispChar("%s:%s" %(ip,port),0,0)                                   # oled屏显示本机服务端ip和端口            
    oled.DispChar('accepting.....',0,16)                                            
    oled.show()

    while True:
        print("accepting.....")
        conn,addr = listenSocket.accept()                                   # 阻塞,等待客户端的请求连接,如果有新的客户端来连接服務器，那麼会返回一个新的套接字专门为这个客户端服务
        print(addr,"connected")                                                         
    
        while True:
            data = conn.recv(1024)                                          # 接收对方发送过来的数据,读取字节设为1024字节
            if(len(data) == 0):
                print("close socket")
                conn.close()                                                # 如果接收数据为0字节时,关闭套接字
                break
            data_utf=data.decode()                                          # 接收到的字节流以utf8编码解码字符串
            print(data_utf)
            oled.DispChar(data_utf,0,48)                                    # 将接收到文本oled显示出来
            oled.show()
            oled.fill_rect(0,48,128,16,0)                                   # 局部清屏
            conn.send(data)                                                 # 返回数据给客户端

# 当捕获异常,关闭套接字、网络
except:
    if(listenSocket):
        listenSocket.close()
    mywifi.disconnectWiFi()