import _thread   # 导入线程模块
import time      # 导入时间模块

# 创建锁
lock=_thread.allocate_lock()

# 定义线程函数,打印线程编号和运行时间
def print_time( threadName, delay):  
    count = 0
    # 获取锁
    if lock.acquire():
        while count < 5:
            time.sleep(delay)
            count += 1
            print ("%s: %s sec" % ( threadName, time.localtime()[5] ))
        # 释放锁
        lock.release()
        print("%s:End" %threadName)
        # 结束线程
        _thread.exit()

# 启动线程1
_thread.start_new_thread( print_time, ("Thread-1", 2, ) )  
# 启动线程2
_thread.start_new_thread( print_time, ("Thread-2", 4, ) )  


while True:  # 主体循环
    pass     # 空指令


