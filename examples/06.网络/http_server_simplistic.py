import socket
import network,time
from mpython import *

# 实例化wifi类
mywifi=wifi() 
# WiFi连接，设置ssid 和password                          		
mywifi.connectWiFi("ssid","psw")   


def main():
    s = socket.socket()
    ai = socket.getaddrinfo(mywifi.sta.ifconfig()[0], 80)
    print("Bind address info:", ai)
    addr = ai[0][-1]
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(addr)
    s.listen(5)
    print("Listening, connect your browser to http://%s:80/" %addr[0])
	# oled显示掌控板ip地址
    oled.DispChar('Connect your browser',0,0,)                           
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
		# 状态行
		client_s.send(b'HTTP/1.0 200 OK\r\n')	
		# 响应类型						
		client_s.send(b'Content-Type: text/html; charset=utf-8\r\n')
		# CRLF 回车换行
		client_s.send(b'\r\n')
		# 响应内容
		content = '欢迎使用掌控板mPython！你的光线传感器值是:%d' % light.read()
		client_s.send(content)
		# 关闭socket
		client_s.close()
