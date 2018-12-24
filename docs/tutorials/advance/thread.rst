线程
=======

.. admonition:: 什么是线程？

    线程是程序中一个单一的顺序控制流程。进程内一个相对独立的、可调度的执行单元，是系统独立调度和分派CPU的基本单位指运行中的程序的调度单位。
    在单个程序中同时运行多个线程完成不同的工作，称为多线程。

  

线程的使用
---------

首先我们要先导入 ``_thread`` 线程模块，它将提供启动线程thread所需的功能。请注意，该模块名称为 ``_thread`` （这里的下划线不是打错了）。
我们还会导入 ``time`` 模块，因此我们可以使用 ``sleep`` 函数，以此在我们的程序中引入一些延迟。

::

    import _thread
    import time


接下来，我们将定义在线程中执行的函数。简单地循环的迭代5次打印所在的当前运行的时间，每次循环都会一定的延时。
我们将使用上面提到的 ``time`` 模块的 ``sleep ``方面来引入延时，``time`` 模块接收作为输入的延迟秒数。参数 ``delay`` 为单次迭代循环延时秒数。

::

    def print_time( threadName, delay):
    count = 0
    while count < 5:
        time.sleep(delay)
        count += 1
        print ("%s: %s sec" % ( threadName, time.localtime()[5] ))

启动我们的线程，我们只需调用 _thread 模块的 start_new_thread 函数，将第一个参数指定为我们先前定义的 ``print_time`` 函数，并将其指定为对应于线程函数参数的2元组。

::

    _thread.start_new_thread( print_time, ("Thread-1", 2, ) ) 
    _thread.start_new_thread( print_time, ("Thread-2", 4, ) )  

最后,使用 ``while`` 条件判断,使程序在死循环中,不执行任何指令::

    while True:
        pass


完成代码如下,开启两线程并循环迭代打印输出::

    import _thread   # 导入线程模块
    import time      # 导入时间模块 

    def print_time( threadName, delay):  # 定义线程函数,打印线程编号和运行时间
        count = 0
        while count < 5:
            time.sleep(delay)
            count += 1
            print ("%s: %s sec" % ( threadName, time.localtime()[5] ))

    # Create two threads as follows
    try:
        _thread.start_new_thread( print_time, ("Thread-1", 2, ) )  # 启动线程1
        _thread.start_new_thread( print_time, ("Thread-2", 4, ) )  # 启动线程2
    except:
        print ("Error: unable to start thread")

    while True:  # 主体循环
        pass     # 空指令


程序执行,会产生以下结果::

    Thread-1: 10 sec
    Thread-2: 12 sec
    Thread-1: 12 sec
    Thread-1: 14 sec
    Thread-2: 16 sec
    Thread-1: 16 sec
    Thread-1: 18 sec
    Thread-2: 20 sec
    Thread-2: 24 sec
    Thread-2: 28 sec

.. Note:: 

    * 多线程看似线程间是并行同时运行的，其实在某一时刻，一个CPU内核只能进行一个进程的任务。

    * 现在的计算机所说的多进程/多任务其实是通过加快CPU的执行速度来实现的，因为一个CPU每秒能执行上亿次的计算，能够对进程进行很多次切换，所以在人为可以感知的时间里，看上去，确实是在同时执行。
