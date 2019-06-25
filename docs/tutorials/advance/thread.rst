线程
=======

.. admonition:: 什么是线程？

    线程是程序中一个单一的顺序控制流程。进程内一个相对独立的、可调度的执行单元，是系统独立调度和分派CPU的基本单位指运行中的程序的调度单位。
    在单个程序中同时运行多个线程完成不同的工作，称为多线程。

  

线程的创建
---------

首先我们要先导入 ``_thread`` 线程模块，它将提供启动线程thread所需的功能。请注意，该模块名称为 ``_thread`` （这里的下划线不是打错了）。
我们还会导入 ``time`` 模块，因此我们可以使用 ``sleep`` 函数，以此在我们的程序中引入一些延迟。

::

    import _thread
    import time


接下来，我们将定义在线程中执行的函数。简单地循环的迭代5次打印所在的当前运行的时间，每次循环都会一定的延时。
我们将使用上面提到的 ``time`` 模块的 ``sleep`` 方面来引入延时，``time`` 模块接收作为输入的延迟秒数。参数 ``delay`` 为单次迭代循环延时秒数。

::

    def print_time( threadName, delay):  
        count = 0
        while count < 5:
            time.sleep(delay)
            count += 1
            print ("%s: %s sec" % ( threadName, time.localtime()[5] ))

        print("%s:End" %threadName)
        # 结束线程
        _thread.exit()

启动我们的线程，我们只需调用 _thread 模块的 start_new_thread 函数，将第一个参数指定为我们先前定义的 ``print_time`` 函数，并将其指定为对应于线程函数参数的2元组。

::

    _thread.start_new_thread( print_time, ("Thread-1", 2, ) ) 
    _thread.start_new_thread( print_time, ("Thread-2", 4, ) )  

最后,使用 ``while`` 条件判断,使程序在死循环中,不执行任何指令::

    while True:
        pass


.. literalinclude:: /../examples/thread/thread_creat.py
    :caption: 完整代码如下,开启两线程并循环迭代打印输出:
    :linenos: 


程序执行,会产生以下结果::

    Thread-1: 4 sec
    Thread-1: 6 sec
    Thread-2: 6 sec
    Thread-1: 8 sec
    Thread-1: 10 sec
    Thread-2: 10 sec
    Thread-1: 12 sec
    Thread-1:End
    Thread-2: 14 sec
    Thread-2: 18 sec
    Thread-2: 22 sec
    Thread-2:End

.. Note:: 

    * 多线程看似线程间是并行同时运行的，其实在某一时刻，一个CPU内核只能进行一个进程的任务。

    * 现在的计算机所说的多进程/多任务其实是通过加快CPU的执行速度来实现的，因为一个CPU每秒能执行上亿次的计算，能够对进程进行很多次切换，所以在人为可以感知的时间里，看上去，确实是在同时执行。


线程的锁定
---------

多线程中，所有变量都由所有线程共享，所以，任何一个变量都可以被任何一个线程修改，因此，线程之间共享数据最大的危险在于多个线程同时改一个变量，把内容给改乱了。
我们将学习如何控制对共享资源的访问。控制是防止数据损坏所必需的。换句话说，为了防止同时访问对象，我们需要使用Lock对象。

线程锁有两种状态: `锁定` 和 `解锁` 。它是在 `解锁` 状态下创建的。它有两个基本方法，``acquire()`` 和 ``release()`` 。

当线程锁的状态为 `解锁` 时，``acquire()`` 将状态更改为 `锁定` 并立即返回。
当状态 `锁定` 时，``acquire()`` 阻塞，直到另一个线程中对 ``release()`` 的调用将其更改为 `解锁` ，然后 ``acquire()`` 调用将其重置为 `锁定` 并返回。

.. Attention:: ``release()`` 方法应只在 `锁定` 状态下被调用; 它将状态更改为 `已解锁` 并立即返回。如果尝试释放未锁定的锁，则会引发 `RuntimeError` 。


.. literalinclude:: /../examples/thread/thread_lock.py
    :caption: 我们将上文的示例改成线程的锁定,如下。只有一个线程能成功地获取锁，然后继续执行代码，其他线程就继续等待直到获得锁为止:
    :linenos: 

运行结果::

    Thread-1: 2 sec
    Thread-1: 4 sec
    Thread-1: 6 sec
    Thread-1: 8 sec
    Thread-1: 10 sec
    Thread-1:End
    Thread-2: 14 sec
    Thread-2: 18 sec
    Thread-2: 22 sec
    Thread-2: 26 sec
    Thread-2: 30 sec
    Thread-2:End


锁的好处就是确保了某段关键代码只能由一个线程从头到尾完整地执行，坏处当然也很多，首先是阻止了多线程并发执行，包含锁的某段代码实际上只能以单线程模式执行，效率就大大地下降了。