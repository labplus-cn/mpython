 提示与技巧
==============

以下为使用内联汇编程序的示例以及有关解决其局限性的信息。在此文件中，术语"汇编程序函数"是
指在Python中用 ``@micropython.asm_thumb`` 装饰器声明的函数，而"子程序"是指从汇编程序函数中调用的汇编程序代码。

代码分支和子程序
-----------------------------

知道标记相对汇编函数为本地，这一信息十分重要。目前尚无法实现在某函数中定义的子程序从另一个函数中调用。

调用子程序，则发送指令 ``bl(LABEL)`` 。这会将控制转移到 ``label(LABEL)`` 指令后的指令，并将返回地址存储在链接寄存器（ ``lr`` 或 ``r14`` ）中。
为返回指令，需发送 ``bx(lr)`` ，这会使子程序调用后的指令继续执行。这种机制意味着，若子程序要调用另一子程序，则须在调用前保存链接寄存器并在终止前将其恢复。

以下示例对函数调用进行说明。请注意：开始时需分支所有子程序调用：子程序以 ``bx(lr)`` 结束执行，而外部函数只是以Python函数样式"下降"结束。

::

    @micropython.asm_thumb
    def quad(r0):
        b(START)
        label(DOUBLE)
        add(r0, r0, r0)
        bx(lr)
        label(START)
        bl(DOUBLE)
        bl(DOUBLE)

    print(quad(10))

以下代码示例演示了嵌套（递归）调用：经典的斐波那契数列。此处，在递归调用前，链接寄存器与其他寄存器一起保存，程序逻辑需保存该寄存器。

::

    @micropython.asm_thumb
    def fib(r0):
        b(START)
        label(DOFIB)
        push({r1, r2, lr})
        cmp(r0, 1)
        ble(FIBDONE)
        sub(r0, 1)
        mov(r2, r0) # r2 = n -1
        bl(DOFIB)
        mov(r1, r0) # r1 = fib(n -1)
        sub(r0, r2, 1)
        bl(DOFIB)   # r0 = fib(n -2)
        add(r0, r0, r1)
        label(FIBDONE)
        pop({r1, r2, lr})
        bx(lr)
        label(START)
        bl(DOFIB)

    for n in range(10):
        print(fib(n))

传输和返回参数
---------------------------

本教程详细介绍了汇编程序函数可以支持0到3个参数这一特性，这三个参数须（若使用）命名为 ``r0`` 、 ``r1`` 和 ``r2`` 。执行代码时，寄存器将被初始化为该值。

可用此种方式传输的数据类型为整数和内存地址。使用当前固件，所有可能的32位值都可传输并返回。若返回值可能设置了最高有效位，
则应使用Python类型提示来启用MicroPython以确定值是否应解释为有符号或无符号整数：类型 ``int`` 或 ``uint`` 。

::

    @micropython.asm_thumb
    def uadd(r0, r1) -> uint:
        add(r0, r0, r1)

``hex(uadd(0x40000000,0x40000000))`` 将返回0x80000000，证明30位和31位不同的整数的传输和返回。

参数和返回值数量的限制可通过 ``array`` 模块方式克服，此方式允许访问任何类型的任何数量的值。

多个参数
~~~~~~~~~~~~~~~~~~

若将一个Python整数数组作为参数传输给汇编函数，则该函数将接收一组连续的整数地址。因此可将多个参数作为单个数组的元素传递。
同样，一个函数可通过将多个值赋值给数组元素来返回多个值。汇编函数尚无法确定数组的长度：这需要传输给函数。

数组的这种用法可进行拓展，以使用三个以上的数组。这是间接完成的： ``uctypes`` 模块支持 ``addressof()`` ，
其将返回作为参数传递的数组地址。因此，您可使用其他数组的地址填充整数数组:

::

    from uctypes import addressof
    @micropython.asm_thumb
    def getindirect(r0):
        ldr(r0, [r0, 0]) # Address of array loaded from passed array 从传输数组中加载的数组地址
        ldr(r0, [r0, 4]) # Return element 1 of indirect array (24) 返回间接数组（24）的元素1

    def testindirect():
        a = array.array('i',[23, 24])
        b = array.array('i',[0,0])
        b[0] = addressof(a)
        print(getindirect(b))

非整数数据类型
~~~~~~~~~~~~~~~~~~~~~~

这些可以通过适当数据类型的数组来处理。例如，可按照如下方法处理单精度浮点数据。这段代码示例需一个浮点数组，并用其平方替换其内容。

::

    from array import array

    @micropython.asm_thumb
    def square(r0, r1):
        label(LOOP)
        vldr(s0, [r0, 0])
        vmul(s0, s0, s0)
        vstr(s0, [r0, 0])
        add(r0, 4)
        sub(r1, 1)
        bgt(LOOP)

    a = array('f', (x for x in range(10)))
    square(a, len(a))
    print(a)

uctypes模块支持使用超出简单数组范围的数据结构。它使Python数据结构能够映射到字节数组实例，然后可将其传输给汇编程序函数。

命名常量
---------------

通过使用命名常量而非用数字随意命名代码，可以使汇编代码变得更具可读性和可维护性。可通过如下方式实现:

::

    MYDATA = const(33)

    @micropython.asm_thumb
    def foo():
        mov(r0, MYDATA)

const()构造使得MicroPython在编译时用其值替换变量名。若常量在外部Python作用域中声明，则其可在多个汇编函数和Python代码间共享。

汇编代码作为类方法
-------------------------------

MicroPython将对象实例的地址作为第一个参数传输给类方法。通常，这对汇编函数没有多大用处。通过将函数声明为静态类函数可避免这种情况:

::

    class foo:
      @staticmethod
      @micropython.asm_thumb
      def bar(r0):
        add(r0, r0, r0)

使用不支持的指令
-------------------------------

这些指令可使用数据语句进行编码，如下所示。尽管支持 ``push()`` 和 ``pop()`` ，以下示例说明其原理。
必要的机器代码可在ARM v7-M体系结构参考手册中查找。请注意：数据调用的第一个参数如

::

    data(2, 0xe92d, 0x0f00) # push r8,r9,r10,r11

表示每个后续参数为2字节值。

克服MicroPython的整数限制
--------------------------------------------

Pyboard芯片包含一个CRC发生器。其使用在MicroPython中提出了一个问题，由于返回值覆盖了32位的完整色域，
而MicroPython中的小整数在位30和31中不能存在不同值。使用以下代码可以克服此限制：使用汇编程序将结果放入数组和Python代码中，
以将结果强制转换为任意精度无符号整数。

::

    from array import array
    import stm

    def enable_crc():
        stm.mem32[stm.RCC + stm.RCC_AHB1ENR] |= 0x1000

    def reset_crc():
        stm.mem32[stm.CRC+stm.CRC_CR] = 1

    @micropython.asm_thumb
    def getval(r0, r1):
        movwt(r3, stm.CRC + stm.CRC_DR)
        str(r1, [r3, 0])
        ldr(r2, [r3, 0])
        str(r2, [r0, 0])

    def getcrc(value):
        a = array('i', [0])
        getval(a, value)
        return a[0] & 0xffffffff # coerce to arbitrary precision

    enable_crc()
    reset_crc()
    for x in range(20):
        print(hex(getcrc(0)))