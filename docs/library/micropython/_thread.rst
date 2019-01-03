
:mod:`_thread` --- 线程
==========================

该模块提供了用于处理多个线程（也称为轻量级进程或任务）的低级原语 - 多个控制线程共享其全局数据空间。为
了同步，提供了简单的锁（也称为互斥锁或二进制信号量）。

发生线程特定错误时，会RuntimeError引发异常。

快速使用示例::

    import _thread
    import time

    def th_func(delay, id):
        while True:
            time.sleep(delay)
            print('Running thread %d' % id)

    for i in range(2):
        _thread.start_new_thread(th_func, (i + 1, i))

方法
~~~~~~~

.. method:: _thread.start_new_thread（function，args [，kwargs]）

启动一个新线程并返回其标识符。线程使用参数列表args（必须是元组）执行函数。可选kwargs参数指定关键字参数的字典。
当函数返回时，线程将以静默方式退出。当函数以未处理的异常终止时，将打印堆栈跟踪，然后线程退出（但其他线程继续运行）。

.. method:: _thread.exit()

引发 SystemExit 异常。如果未捕获时，这将导致线程以静默方式退出。

.. method:: _thread.allocate_lock()

返回一个新的锁定对象。锁的方法如下所述。锁最初是解锁的。

.. method:: _thread.get_ident()

返回thread identifier当前线程。这是一个非零整数。它的价值没有直接意义; 
它旨在用作例如索引线程特定数据的字典的魔术cookie。当线程退出并创建另一个线程时，可以回收线程标识符。

.. method:: _thread.stack_size([size])

返回创建新线程时使用的线程堆栈大小（以字节为单位）。可选的size参数指定用于后续创建的线程的堆栈大小，并且必须是0（使用平台或配置的默认值）或至少为4096（4KiB）的正整数值。
4KiB是目前支持的最小堆栈大小值，以保证解释器本身有足够的堆栈空间。

对象
~~~~~~~

.. object:: _thread.LockType

这是锁定对象的类型。

.. Class:: Lock

用于线程之间的同步

方法
-----

锁定对象具有以下方法：

.. method::  lock.acquire(waitflag = 1，timeout = -1)

在没有任何可选参数的情况下，此方法无条件地获取锁定，如果有必要，等待它被另一个线程释放（一次只有一个线程可以获取锁定 - 这就是它们存在的原因）。

如果存在整数 ``waitflag`` 参数，则操作取决于其值：如果它为零，则仅在不等待的情况下立即获取锁定时获取锁定，而如果它非零，则如上所述无条件地获取锁定。

如果浮点超时参数存在且为正，则它指定返回之前的最长等待时间（以秒为单位）。负超时参数指定无限制等待。如果 ``waitflag`` 为零，则无法指定超时。

``True`` 如果成功获取锁定则返回值，否则返回值 ``False`` 。

.. method::  lock.release()

释放锁定。必须先获取锁，但不一定是同一个线程。

.. method::  lock.locked()

返回锁的状态：True如果已被某个线程获取，False如果没有。

除了这些方法之外，还可以通过with语句使用锁定对象，例如::

    import _thread

    a_lock = _thread.allocate_lock()
    with a_lock:
        print("a_lock is locked while this executes")
