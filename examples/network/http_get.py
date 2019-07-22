import socket

# 定义http get函数
def http_get(url):
    # 解析url
    _, _, host, path = url.split('/', 3)
    # 将网站的域名解析成IP地址
    addr = socket.getaddrinfo(host, 80)[0][-1]
    # 构建socket
    s = socket.socket()
    # 连接IP地址
    s.connect(addr)
    # 以http get 请求格式发送
    s.send(bytes('GET /%s HTTP/1.0\r\nHost: %s\r\n\r\n' % (path, host), 'utf8'))
    while True:
        # socket接收
        data = s.recv(100)
        if data:
            print(str(data, 'utf8'), end='')
        else:
            break
    s.close()

# 访问 http://micropython.org/ks/test.html
http_get('http://micropython.org/ks/test.html')