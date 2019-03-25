.. _speed_python:
最大化MicroPython速度
============================

.. contents::

本教程介绍了改进MicroPython代码的方法。最优化及其他语言在另外章节中介绍（即使用C语言和MicroPython内联汇编编写的模块）。

开发高性能的代码包括以下两个阶段，我们将依次介绍。

* 速度设计
* 代码和排错

优化步骤:

* 识别代码的最慢段
* 改进Python代码的效率
* 使用本地代码发射器
* 使用Viper代码发射器
* 使用特定于硬件的优化

速度设计
-------------------

应该从开始就考虑性能问题。这涉及到对性能至关重要的代码部分，应特别关注代码的设计。
优化过程从检测代码开始：若设计从开始就没有差错，那优化就很轻松了，实际上可能没有优化的必要。

算法
~~~~~~~~~~

设计性能程序的最重要的部分就是确保使用最佳算法。这应是教科书上的议题而非出现在MicroPython指南中。
但是有时可通过使用已知效率的算法来实现可观的性能收益。

RAM分配
~~~~~~~~~~~~~~

设计高效的MicroPython代码，则有必要理解解释器分配RAM的方式。当创建某一对象或该对象大小增长时（例如将一个项附加到列表），
RAM即从名为堆的块中分配出来。这一过程需耗费很长时间，而且有时会触发垃圾收集的过程，此过程将耗时数毫秒。

因此，若对象仅允许创建一次且其大小不可增长，则函数或方法的性能得以改进。这意味着对象在其使用期间持续存在：
通常对象在类构造函数中实例化，并在各种方法中使用。

更多详细信息，请参见下面的 :ref:`Controlling garbage collection <controlling_gc>` below.

缓冲区
~~~~~~~

上述示例是需要缓冲区的常见情况，例如用于与设备通信的缓冲区。典型的驱动器将在构造函数中创建缓冲区，
并在其I/O方法中使用，该方法将重复调用。

MicroPython库通常为预分配的缓冲区提供支持。例如，支持流接口（例如：文件或UART）的对象提供为
读取数据分配新的缓冲区的 `read()` 方法，以及将数据读取入现存缓冲区的 `readinto()` 方法。

浮点数
~~~~~~~~~~~~~~

某些MicroPython端口在堆上分配浮点数。其他端口可能缺少专用的浮点协处理器，且在"软件"上以低于在整数上的速度对它们执行算术运算。
性能事关重要的情况下，使用整数运算；性能无关紧要的情况下，限制浮点数用于代码的部分。例如，将ADC读数作为整数值捕捉到数组中，
然后将其转换为浮点数进行信号处理。

数组
~~~~~~

考虑使用各种类型的数组来替代列表。 `array` 模块支持不同的项类型，8位项由的内置 `bytes` 和 `bytearray` 类支持。
这些数据结构将项储存在连续内存位置中。为避免在临界区代码中分配内存，内存应进行预分配并作为参数或限定性对象传递。

在传递诸如 `bytearray` 实例之类的对象片段时，Python会创建一个副本，该副本涉及与片段大小成比例的大小分配。
这可以使用 `memoryview` 对象缓解。 `memoryview` 本身在堆上分配，但其为一个较小且固定大小的对象。

.. code:: python

    ba = bytearray(10000)  # big array
    func(ba[30:2000])      # a copy is passed, ~2K new allocation 传递一个副本，~2K新分配
    mv = memoryview(ba)    # small object is allocated 分配小对象
    func(mv[30:2000])      # a pointer to memory is passed 传递指向内存的指针

`memoryview` 仅可应用于支持缓冲区协议的对象-这包括数组但不包括列表。小提示：memoryview对象是有用的，
它保留了原始的缓冲区对象。因此，memoryview并非万能的灵丹妙药。例如，在上述示例中，若您用10K缓冲区完成，
只需其中的30：2000字节，那么最好做一个片段，不使用10K缓冲区（垃圾收集准备就绪），而不是做一个长时间的内存视图，
并保持10K阻塞的GC。

尽管如此， `memoryview` 对于高级预分配缓冲区管理而言必不可少。上述 `readinto()` 方法将数据放在缓冲区的开始处，
并填充整个缓冲区。 若您需要将数据放进现有缓冲区中，应如何操作？ 只需在缓冲区的所需部分创建一个内存视图，
并将其传递给 `readinto()` 。

识别代码的最慢段
---------------------------------------

此过程也称为profiling，教科书中对其进行了介绍，此过程由不同的软件工具支持（对于标准Python而言）。
对于可能在MicroPython平台上运行的较小型嵌入式应用程序，最慢的函数或方法通常可通过正确
使用 `utime` 中记录的时序 ``ticks`` 函数来建立。代码执行时长可用毫秒、微秒和CPU周期来计算。

以下代码可以通过添加 ``@timed_function`` 装饰器使任何函数或方法计时:

.. code:: python

    def timed_function(f, *args, **kwargs):
        myname = str(f).split(' ')[1]
        def new_func(*args, **kwargs):
            t = utime.ticks_us()
            result = f(*args, **kwargs)
            delta = utime.ticks_diff(utime.ticks_us(), t)
            print('Function {} Time = {:6.3f}ms'.format(myname, delta/1000))
            return result
        return new_func

MicroPython代码改进
-----------------------------

const()声明
~~~~~~~~~~~~~~~~~~~~~~~

MicroPython提供了一个 ``const()`` 声明。 其运行方式与C语言中的 ``#define`` 类似，因为当代码被编译为字节码时，
编译器会将数字值替换为标识符。这可以避免在运行时查找字典。 ``const()`` 的参数可为任何可在编译时计算为整数的数值，
例如 ``0x100`` 或 ``1 << 8`` 。

.. _Caching:

缓存对象引用
~~~~~~~~~~~~~~~~~~~~~~~~~~

在函数或方法重复访问对象的情况下，通过将对象缓存在局部变量中可以提高性能:

.. code:: python

    class foo(object):
        def __init__(self):
            ba = bytearray(100)
        def bar(self, obj_display):
            ba_ref = self.ba
            fb = obj_display.framebuffer
            # iterative code using these two objects 使用这两个对象的代码

这就避免了在方法 ``bar()`` 中重复查找 ``self.ba`` 和 ``obj_display.framebuffer`` 。

.. _controlling_gc:

控制垃圾回收
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

当需要内存分配时，MicroPython会尝试在堆上寻找适当大小的块。寻找可能会失败，通常是因为堆中堆满了代码不再引用的对象。
若发生故障，垃圾回收将回收冗余对象所占用的内存，然后再次尝试分配。此过程可能需要数毫秒。

周期性地发布 ``gc.collect()`` 可能对预防有帮助。首先，在真正需要回收之前进行回收速度会更快，
若经常回收，则耗时约1毫秒。其次，您可在代码中确定此时间的使用点，而非在随机点上发生较长的延迟，
可能在速度临界区。最后，经常进行回收可减少堆中的碎片化。严重的碎片化会导致无法修复的分配故障。

本地密码发射器
-----------------------

这使得MicroPython编译器发送本地CPU操作码，而非字节码。它涵盖了MicroPython的大部分功能，
所以大部分功能无需适应（见下文）。它是通过一个函数装饰器调用的:

.. code:: python

    @micropython.native
    def foo(self, arg):
        buf = self.linebuf # Cached object 缓存对象
        # code

目前本地代码发送器仍然存在一些局限性。

* 不支持上下文管理器（ ``with`` 语句）。
* 不支持生成器。
* 若使用 ``raise`` ，则必须应用一个参数。

性能提高的代价（约为字节码的两倍）是编译代码大小的增加。

Viper代码发送器
----------------------

上面讨论的优化包含符合标准的Python代码。 Viper代码发射器并不完全兼容。为实现高性能，它支持特殊的Viper本地数据类型。
整数处理并不兼容，因其使用机器字：32位硬件上的算法是执行模块2**32。

与本地发送器相似，Viper生成机器指令，但进行了进一步优化，大大提高了性能，尤其是在整数算法和位操作方面。其使用装饰器调用:

.. code:: python

    @micropython.viper
    def foo(self, arg: int) -> int:
        # code

如上所述，使用Python提示类型来辅助Viper优化器大有益处。类型提示提供参数的数据类型和返回值的信息；
这些是在此正式定义的标准Python语言特性 `PEP0484 <https://www.python.org/dev/peps/pep-0484/>`_.
Viper支持名为 ``int`` 、 ``uint`` （无符号整数）、 ``ptr`` 、 ``ptr8`` 、 ``ptr16`` 和 ``ptr32`` 的其自身的类型组。 ``ptrX``类型在下面进行介绍。
目前类型仅作一种用途：作为函数返回值的类型提示。若函数返回 ``0xffffffff`` ，Python将结果解释为2**32 -1而非-1。

除了本地发送器施加的限制之外，以下限制也适用:

* 函数可能有多达4个参数。
* 不许可默认参数值。
* 浮点数可能被使用但未优化。

Viper提供指针类型以协助优化器。这些包括

* ``ptr`` 指向对象的指针。
* ``ptr8`` 指向一个字节的指针。
* ``ptr16`` 指向一个16位半字的指针。
* ``ptr32`` 指向一个32位机器字的指针。

Python程序员可能不熟悉指针的概念。 它与Python `memoryview` 对象有相似之处，它可以直接访问存储在内存中的数据。
使用下标符号访问项目，但不支持片段：指针只能返回单个项目。其目的是提供快速随机访问存储在连续存储位置的数据--
例如存储在支持缓冲协议的对象中的数据，以及微控制器中存储器映射的外设寄存器。应该指出的是，使用指针编程很危险：
边界检查不会执行，编译器不会阻止缓冲区的超限错误。

典型的用法是缓存变量:

.. code:: python

    @micropython.viper
    def foo(self, arg: int) -> int:
        buf = ptr8(self.linebuf) # self.linebuf is a bytearray or bytes object 是一个字节数组或一个字节对象
        for x in range(20, 30):
            bar = buf[x] # Access a data item through the pointer 通过指针访问数据项目
            # code omitted 省略的代码

在此示例中，编译器"知道" ``buf`` 为字节组的地址；其可发送代码，以在运行时快速计算 ``buf[x]`` 的地址。
在使用转换将对象转换为Viper本机类型时，应在函数启动时执行，而不是在关键计时回路中执行，因为转换操作可能需要数微秒。转换要求如下:

* 转换操作符当前为: ``int``, ``bool``, ``uint``, ``ptr``, ``ptr8``, ``ptr16`` 和 ``ptr32``.
* 转换结果为本地Viper变量。
* 转换的参数可为Python对象或本地Viper变量。
* 若参数为本地Viper变量，则转换为仅改变类型（例如：从 ``uint`` 到 ``ptr8`` ）的空操作，所以您可使用此指针来储存/加载。
* 若参数为Python对象，且转换为 ``int`` 或 ``uint`` ，则Python对象须为整数类型，且返回该整数对象的值。
* 布尔转换的参数须为整数类型（布尔值或整数）；当用作返回类型时，Viper函数将返回True或False对象。
* 若参数为Python对象，转换为 ``ptr``、 ``ptr``、 ``ptr16`` 或 ``ptr32``，则Python对象须具有读写功能的缓冲区协议
 （在此情况下，返回指向缓冲区开始的指针）或为整数类型（在此情况下，返回整数对象的值）。

以下示例说明了使用 ``ptr16`` 转换来切换引脚X1 ``n`` 次:

.. code:: python

    BIT0 = const(1)
    @micropython.viper
    def toggle_n(n: int):
        odr = ptr16(stm.GPIOA + stm.GPIO_ODR)
        for _ in range(n):
            odr[0] ^= BIT0

这三个代码发送器的详细技术说明，请参见Kickstarter的 `Note 1 <https://www.kickstarter.com/projects/214379695/micro-python-python-for-microcontrollers/posts/664832>`_
和 `Note 2 <https://www.kickstarter.com/projects/214379695/micro-python-python-for-microcontrollers/posts/665145>`_

直接访问硬件
---------------------------

.. note::

    本节给出了Pyboard的代码示例。 不过，此处介绍的技术也可能适用于其他MicroPython端口。

这属于更高级的编程范畴，涉及目标MCU的一些知识。考虑切换Pyboard上的输出引脚的例子。标准方法是写入

.. code:: python

    mypin.value(mypin.value() ^ 1) # mypin was instantiated as an output pin实例化为输出引脚

这涉及两次调用 `Pin` 实例的 `value()` 方法的开销。通过对芯片的GPIO端口输出数据寄存器（odr）的相关位执行读/写操作，
可消除此开销。为实现这一点， ``stm`` 模块提供了一组提供相关寄存器地址的常量。引脚 ``P4`` （CPU引脚 ``A14`` ）的快速切换
（对应绿色LED）可按如下方式执行:

.. code:: python

    import machine
    import stm

    BIT14 = const(1 << 14)
    machine.mem16[stm.GPIOA + stm.GPIO_ODR] ^= BIT14