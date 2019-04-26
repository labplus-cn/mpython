import radio
import _thread

channel=2

radio.on()
radio.config(channel=channel)               # radio通道设置

def rec_loop():                             # radio接收循环
    while True:
        temp=radio.receive(True)           # radio 接收数据,返回(msg,mac)
        # temp=radio.receive()             # radio 接收数据,返回msg
        if temp:                           # 当接收到数据时打印
            print(temp)

_thread.start_new_thread(rec_loop, ())      # radio接收线程

radio.send("hello mPython!")
