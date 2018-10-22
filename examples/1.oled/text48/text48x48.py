from mpython import *

def hex2bin(l):
    '''
    把'0xff'等十六进制转换成
    二进制10数字序列
    '''
    rst = ''
    for h in l:
        # int 把十六进制字符串如'0xff'
        # 换换为整数，参数16
        # bin把整数转换为10序列
        # [2:]切片运算
        # 去掉数组前两个元素
        s = bin(int(h, 16))[2:]
        rst += '0'*(8-len(s))+s
    return rst
# 读取文件并替换其中的换行符
f = open('lang.txt').read().replace("\r\n","")
l = f.split(",") # 把都好分隔的字符串转换成数组
l = l[:len(l)-1] # 去掉最后一个空白元素
rst = hex2bin(l) # 得到10序列
display.fill(0)
length = len(rst)



def text(s,x,y):
    display.DispChar(s,x,y)
text("人人都能编程", 50,0)
text("我为卡搭带盐", 50,13)
text("感谢盛思提供", 50,26)
text("的掌控板！", 50,39)
text("学Python用极客战记", 0,51)


for i in range(length):
    if rst[i] =="1":
        display.pixel(i%48,i//48,1)
    else:
        display.pixel(i%48,i//48,0)
    

display.show()
        

