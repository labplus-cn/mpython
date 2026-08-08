import usocket
import gc

DEFAULT_TIMEOUT = 10 # sec
LOCAL_DOMAIN = '127.0.0.1'
CMD_EHLO = 'EHLO'
CMD_STARTTLS = 'STARTTLS'
CMD_AUTH = 'AUTH'
CMD_MAIL = 'MAIL'
AUTH_PLAIN = 'PLAIN'
AUTH_LOGIN = 'LOGIN'

# 加密过程
def encrypt_string(message):
    encode_result = ""
    for char in message:
        char_int = ord(char)
        if char.isalpha():  # 判断是否为字母
            if 64 < char_int < 78 or 96 < char_int < 110:  # 针对其中的部分字母进行加密
                encode_result += "00" + str((char_int + 13) * 2) + "|"
            else:  # 对剩下字母进行加密
                encode_result += "01" + str(char_int - 23) + "|"

        elif '\u4e00' <= char <= '\u9fff':  # 单个汉字可以这么判断
            encode_result += "02" + str(char_int + 24) + "|"
        else:  # 对数字、特殊字符进行加密
            encode_result += "03" + str(char_int) + "|"

    # print("Encode result: {}".format(encode_result))

    return encode_result


# 解密过程
def decrypt_string(message):
    decode_result = ""

    # 将message转换为list
    message_list = message.split("|")
    message_list.remove("")  # 移除list中的空元素

    for i in message_list:
        type_ = i[:2]
        char_number = int(i[2:])
        if type_ == "00":
            char_number = int(char_number / 2 - 13)
        elif type_ == "01":
            char_number = char_number + 23
        elif type_ == "02":
            char_number = char_number - 24
        else:
            char_number = char_number

        decode_result += chr(char_number)

    # print("Decode result: {}".format(decode_result))
    return decode_result

DEFAULT_EMAIL = 'zhangkongban@163.com'
DEFAULT_PASSWORD = encrypt_string('NTJTTHERKCSJFEXM')

class SMTP:
    def cmd(self, cmd_str):
        sock = self._sock;
        sock.write('%s\r\n' % cmd_str)
        resp = []
        next = True
        while next:
            code = sock.read(3)
            next = sock.read(1) == b'-'
            resp.append(sock.readline().strip().decode())
        try:
            return int(code), resp
        except:
            return code, resp


    def __init__(self, host, port, ssl=False, username=None, password=None):
        import ussl
        self.username = username
        addr = usocket.getaddrinfo(host, port)[0][-1]
        sock = usocket.socket(usocket.AF_INET, usocket.SOCK_STREAM)
        sock.settimeout(DEFAULT_TIMEOUT)
        sock.connect(addr)
        if ssl:
            sock = ussl.wrap_socket(sock)
        code = int(sock.read(3))
        sock.readline()
        assert code==220, 'cant connect to server %d, %s' % (code, resp)
        self._sock = sock

        code, resp = self.cmd(CMD_EHLO + ' ' + LOCAL_DOMAIN)
        assert code==250, '%d' % code
        if CMD_STARTTLS in resp:
            code, resp = self.cmd(CMD_STARTTLS)
            assert code==220, 'start tls failed %d, %s' % (code, resp)
            self._sock = ussl.wrap_socket(sock)

        if username and password:
            self.login(username, password)

    def login(self, username, password):
        self.username = username
        code, resp = self.cmd(CMD_EHLO + ' ' + LOCAL_DOMAIN)
        assert code==250, '%d, %s' % (code, resp)

        auths = None
        for feature in resp:
            if feature[:4].upper() == CMD_AUTH:
                auths = feature[4:].strip('=').upper().split()
        assert auths!=None, "no auth method"

        from ubinascii import b2a_base64 as b64
        if AUTH_PLAIN in auths:
            cren = b64("\0%s\0%s" % (username, password))[:-1].decode()
            code, resp = self.cmd('%s %s %s' % (CMD_AUTH, AUTH_PLAIN, cren))
        elif AUTH_LOGIN in auths:
            code, resp = self.cmd("%s %s %s" % (CMD_AUTH, AUTH_LOGIN, b64(username)[:-1].decode()))
            assert code==334, 'wrong username %d, %s' % (code, resp)
            code, resp = self.cmd(b64(password)[:-1].decode())
        else:
            raise Exception("auth(%s) not supported " % ', '.join(auths))

        assert code==235 or code==503, 'auth error %d, %s' % (code, resp)
        return code, resp

    def to(self, addrs, mail_from=None):
        mail_from = self.username if mail_from==None else mail_from
        code, resp = self.cmd(CMD_EHLO + ' ' + LOCAL_DOMAIN)
        assert code==250, '%d' % code
        code, resp = self.cmd('MAIL FROM: <%s>' % mail_from)
        assert code==250, 'sender refused %d, %s' % (code, resp)

        if isinstance(addrs, str):
            addrs = [addrs]
        count = 0
        for addr in addrs:
            code, resp = self.cmd('RCPT TO: <%s>' % addr)
            if code!=250 and code!=251:
                print('%s refused, %s' % (addr, resp))
                count += 1
        assert count!=len(addrs), 'recipient refused, %d, %s' % (code, resp)

        code, resp = self.cmd('DATA')
        assert code==354, 'data refused, %d, %s' % (code, resp)
        return code, resp

    def write(self, content):
        self._sock.write(content)

    def send(self, content=''):
        if content:
            self.write(content)
        self._sock.write('\r\n.\r\n') # the five letter sequence marked for ending
        line = self._sock.readline()
        return (int(line[:3]), line[4:].strip().decode())

    def quit(self):
        self.cmd("QUIT")
        self._sock.close()


def send_email(myusername,mypassword,target_email,SMTP_SERVER,subject,text):
    if(SMTP_SERVER==1):
        SMTP_SERVER = 'smtp.office365.com'
        SMTP_SERVER_PORT = 587
    elif(SMTP_SERVER==2):
        SMTP_SERVER = 'smtp.qq.com'
        SMTP_SERVER_PORT = 587
    elif(SMTP_SERVER==3):
        SMTP_SERVER = 'smtp.126.com'
        SMTP_SERVER_PORT = 25
    elif(SMTP_SERVER==4):
        SMTP_SERVER = 'smtp.163.com'
        SMTP_SERVER_PORT = 25
    
    if(myusername == DEFAULT_EMAIL):
        mypassword = decrypt_string(mypassword)

    try:
        gc.collect()
        smtp = SMTP(SMTP_SERVER, SMTP_SERVER_PORT)
        smtp.login(myusername, mypassword)
        smtp.to(target_email)
        smtp.write("From: 掌控板：<{}>\r\n".format(myusername))  # windows服务器不能单独识别\n  所以加上\r 发送端邮箱地址
        smtp.write("To: You<{}>\r\n".format(target_email))      # 如果出现报错可以尝试把\r\n换成\n  接收端邮箱地址
        smtp.write("Subject:{}\r\n\n".format(subject))   # 邮件主题
        smtp.write("{}\r\n".format(text)) # 邮件内容
        smtp.send()
        smtp.quit()
        print("Email was sent successfully!")
    except Exception as e:
        print("ERROR!!!")
        print("Email sending failed!")
        raise e
