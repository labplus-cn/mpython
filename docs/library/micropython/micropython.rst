:mod:`micropython` -- 访问和控制MicroPython内部
==============================================================

.. module:: micropython
   :synopsis: 访问和控制MicroPython内部


函数
---------

.. function:: const(expr)

  用于声明表达式是常量，以便编译可以优化它。该功能的使用应如下::

    from micropython import const

    CONST_X = const(123)
    CONST_Y = const(2 * CONST_X + 1)
    print(CONST_X)
    print(CONST_Y)

  运行结果::

    >>>123
    >>>247



  以这种方式声明的常量仍可作为全局变量从它们声明的模块外部访问。另一方面，如果常量以下划线开头，则它被隐藏，
  它不可用作全局变量，并且不会占用执行期间的任何内存。

  此 ``const`` 函数由MicroPython解析器直接识别，并作为  :mod:`micropython`  模块的一部分提供，主要是通过遵循上述模式可以编写在
  CPython和MicroPython下运行的脚本。



.. function:: opt_level([level])

  如果水平给出那么这个函数设置脚本，并返回的后续编译优化级别 ``None`` 。否则返回当前优化级别。

  优化级别控制以下编译功能:

    * 断言:在0级断言语句被启用并编译成字节码; 在级别1和更高级别的断言未编译。
    * 内置 ``__debug__`` 变量:在0级，此变量扩展为 ``True``; 在1级和更高级别，它扩展到 ``False``。
    * 源代码行号:在0,1和2级源代码行号与字节码一起存储，以便异常可以报告它们出现的行号; 在级别3和更高的行号不存储。

  默认优化级别通常为0级。

.. function:: alloc_emergency_exception_buf(size)

  设置紧急情况下的（栈溢出，普通RAM不足等）保险RAM分配，使在紧急情况下仍有RAM可用。

    - ``size``:保险剩余RAM的大小，一般为100


  使用此函数的一种好方法是将它放在主脚本的开头（例如 ``boot.py`` 或 ``main.py`` ），
  然后紧急异常缓冲区将对其后的所有代码生效。


.. function:: mem_info([verbose])

  函数说明： 打印当前内存使用的情况（包括栈和堆的使用量）。

  .. 注意::

      如果给出参数level（任何数据类型），则打印出更加详细的信息，它会打印整个堆，指示哪些内存块被使用，哪些内存是空闲的。 

  不给参数::

    >>>micropython.mem_info()
    stack: 736 out of 15360
    GC: total: 48000, used: 7984, free: 40016
    No. of 1-blocks: 72, 2-blocks: 31, max blk sz: 264, max free sz: 2492
    >>>

  给定参数::

      >>>micropython.mem_info("level")
    stack: 752 out of 15360
    GC: total: 48000, used: 8400, free: 39600
    No. of 1-blocks: 82, 2-blocks: 36, max blk sz: 264, max free sz: 2466
    GC memory layout; from 3ffc4930:
    00000: h=ShhBMh=DhBhDBBBBhAh===h===Ahh==h==============================
    00400: ================================================================
    00800: ================================================================
    00c00: ================================================================
    01000: =========================================hBh==Ah=ShShhThhAh=BhBh
    01400: hhBhTShh=h==h=hh=Bh=BDhhh=hh=Bh=hh=Bh=BhBh=hh=hh=h===h=Bhh=h=BhB
    01800: h=hh=h=Bh=hBh=h=hBh=h=hBh=h=h=hh=======h========================
    01c00: ============================================Bh=hBhTh==hh=hh=Sh=h
    02000: h==Bh=B..h...h==....h=..........................................
          (37 lines all free)
    0b800: ........................................................
    >>>

.. function:: qstr_info([verbose])

  打印当前所有已使用的字符串在内存中的个数，占用内存大小等信息。

  .. 注意::

    如果给出参数，则打印出具体的字符串信息。打印的信息是依赖于实际情况的，包括被录入的字符串数量和它们使用的RAM的数量。
    在详细模式中，它打印出所有字符串的名称。 

  不给参数::

    >>>micropython.qstr_info()  
    qstr pool: n_pool=1, n_qstr=4, n_str_data_bytes=31, n_total_bytes=1135
    >>>
    
  给定参数::

    >>>micropython.qstr_info("level")  
    qstr pool: n_pool=1, n_qstr=4, n_str_data_bytes=31, n_total_bytes=1135
    Q(b)
    Q(2)
    Q(asdfa222)
    Q(level)
    >>>

.. function:: stack_use()

  返回一个整数，表示当前正在使用的堆栈量。这个绝对值并不是特别有用，而应该用它来计算不同点的堆栈使用差异。

  示例::

    >>>micropython.stack_use()
    720

.. function:: heap_lock()

  锁定堆，当堆被锁定时，任何操作都不会分配内存 。如果尝试内存分配操作，则会产生MemoryError错误。。

  

.. function:: heap_unlock()

  解锁堆

.. function:: kbd_intr(chr)

  设置将引发KeyboardInterrupt异常的字符。默认情况下，在脚本执行期间将其设置为3，对应于Ctrl-C。
  将-1传递给此函数将禁用Ctrl-C的捕获，传递3将恢复它。

  如果该流用于其他目的，此函数可用于防止在通常用于REPL的传入字符流上捕获Ctrl-C。

.. function:: schedule(func, arg)

  安排函数func “很快”执行。该函数传递值arg作为其单个参数。“很快”意味着MicroPython运行时将尽最大努力在尽可能早的时间执行该功能，
  因为它也试图提高效率，并且以下条件成立：

  - 预定的功能永远不会抢占另一个预定的功能。
  - 计划函数总是在“操作码之间”执行，这意味着所有基本的Python操作（例如附加到列表）都保证是原子的。
  - 给定端口可以定义“关键区域”，在该区域内永远不会执行调度函数。可以在关键区域内安排功能，但在退出该区域之前不会执行这些功能。关键区域的示例是抢占中断处理程序（IRQ）。

  此功能的用途是从抢占IRQ安排回调。这样的IRQ限制了在IRQ中运行的代码（例如，堆可能被锁定），并且调度稍后调用的函数将解除这些限制。

  注意：如果 ``schedule()`` 从抢占IRQ调用，则当不允许内存分配并且要传递的回调 ``schedule()`` 是绑定方法时，直接传递它将失败。这是因为创建对绑定方法的引用会导致内存分配。解决方案是在类构建对象中创建对方法的引用并将该引用传递给 ``schedule()`` 。
  这里将在“创建Python对象”下的参考文档中详细讨论 。

  有一个有限的堆栈来保存预定的函数，如果堆栈已满，``schedule()`` 则会引发一个 ``RuntimeError`` 。

