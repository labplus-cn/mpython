from mpython import *
import socket 

mywifi=wifi()                                           # 创建wifi对象
mywifi.connectWiFi("ssid","password")                   # 连接网络

# 捕获异常，如果在"try" 代码块中意外中断，则停止关闭套接字
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)               # 创建UDP的套接字
    s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)              # 设置套接字属性
    ip=mywifi.sta.ifconfig()[0]                                        # 获取本机ip地址
    s.bind((ip,6000))                                                  # 绑定ip和端口号
    print('waiting...')
    oled.DispChar("%s:6000" %ip,0,0)
    oled.show()
    while True:
        data,addr=s.recvfrom(1024)                           # 接收对方发送过来的数据,读取字节设为1024字节,返回(data,addr)二元组
        print('received:',data,'from',addr)                  # 打印接收到数据                      
        oled.fill(0)                                         # 清屏
        oled.DispChar("%s" %data.decode(),0,15)              # oled显示接收内容
        oled.DispChar("from%s" %addr[0],0,31)
        oled.show()                 
        

# 当捕获异常,关闭套接字、网络
except:
    if (s):
        s.close()
    mywifi.disconnectWiFi()