MicroPython的交互式解释器模式 （又称REPL）
=======================================================

此部分介绍了MicroPython的交互式解释器模式的特性，其常用术语为REPL（读取read-评估eval-打印print-循环loop），用于指代此交互式提示符。

自动-缩进
-----------

当键入以冒号（例如：if、for、while）结尾的python语句时，提示符将变为三个点（...），光标将缩进4个空格。
当您点击返回键，下一行将继续在正常语句缩进的同一级别，或在适当的情况下继续添加缩进级别。若您点击退格键，则将撤销一个缩进级别。

若您的光标一直停在开始时，点击返回键将执行您输入的代码。以下演示了您在输入for语句后将看到的（下划线显示光标的位置）:

    >>> for i in range(3):
    ...     _

若您输入if语句，则将提供额外的缩进级别:

    >>> for i in range(30):
    ...     if i > 3:
    ...         _

现在输入 ``break`` ，然后点击回车键，再点击退格键:

    >>> for i in range(30):
    ...     if i > 3:
    ...         break
    ...     _

最后，键入 ``print(i)`` ，依次点击回车键、退格键和回车键:

    >>> for i in range(30):
    ...     if i > 3:
    ...         break
    ...     print(i)
    ...
    0
    1
    2
    3
    >>>

若前两行都为空格，则不会应用自动缩进。这意味着您可以通过点击两次返回来完成复合语句输入，然后第三次按键结束并执行。

自动-完成
---------------

当在REPL中输入指令时，如果输入的行对应某物名称的开头，点击TAB键将显示您可能输入的内容。
例如，键入 ``m`` 并点击TAB，则其将扩展为 ``machine`` 。键入一个点 ``.`` 并点击TAB，您将看到如下:

    >>> machine.
    __name__        info            unique_id       reset
    bootloader      freq            rng             idle
    sleep           deepsleep       disable_irq     enable_irq
    Pin

该词将尽可能扩展，直至出现多种可能性。例如：键入 ``machine.Pin.AF3`` 并点击TAB键，
则其将扩展为 ``machine.Pin.AF3_TIM`` 。长按TAB一秒，则显示可能的扩展:

    >>> machine.Pin.AF3_TIM
    AF3_TIM10       AF3_TIM11       AF3_TIM8        AF3_TIM9
    >>> machine.Pin.AF3_TIM

中断一个运行程序
------------------------------

您可通过点击Ctrl-C来中断一个运行程序。这将引发键盘中断，使您返回REPL，前提是您的程序不会阻截键盘中断故障。

例如:

    >>> for i in range(1000000):
    ...     print(i)
    ...
    0
    1
    2
    3
    ...
    6466
    6467
    6468
    Traceback (most recent call last):
      File "<stdin>", line 2, in <module>
    KeyboardInterrupt:
    >>>

粘贴模式
----------

若您想将某些代码粘贴到您的终端窗口中，自动缩进特性将会成为障碍。例如，若您有以下python代码: ::

   def foo():
       print('This is a test to show paste mode')
       print('Here is a second line')
   foo()

您试图将此代码粘贴到常规REPL中，那么您将会看到以下内容:

    >>> def foo():
    ...         print('This is a test to show paste mode')
    ...             print('Here is a second line')
    ...             foo()
    ...
    Traceback (most recent call last):
      File "<stdin>", line 3
    IndentationError: unexpected indent

若您点击Ctrl-E，则将进入粘贴模式，即关闭自动缩进特性，并将提示符从 ``>>>`` 更改为 ``===`` 。例如:

    >>>
    paste mode; Ctrl-C to cancel, Ctrl-D to finish
    === def foo():
    ===     print('This is a test to show paste mode')
    ===     print('Here is a second line')
    === foo()
    ===
    This is a test to show paste mode
    Here is a second line
    >>>

粘贴模式允许粘贴空白行，将被粘贴文本作为文件编译。点击Ctrl-D退出粘贴模式，并启动编译。

软复位
----------

软复位将重置python的解释器，但不会重置您连接到MicroPython板的方法（USB-串口或WiFi）。

您可点击Ctrl-D从REPL进行软复位，或从您的python代码中执行: ::

    raise SystemExit

例如：若您重置您的MicroPython板，并执行dir()指令，您将看到如下内容:

    >>> dir()
    ['__name__', 'pyb']

现在创建一些变量，并重复dir()指令:

    >>> i = 1
    >>> j = 23
    >>> x = 'abc'
    >>> dir()
    ['j', 'x', '__name__', 'pyb', 'i']
    >>>

现在，若您点击Ctrl-D，并重复dir()指令，您将发现变量不复存在:

.. code-block:: python

    PYB: sync filesystems
    PYB: soft reboot
    MicroPython v1.5-51-g6f70283-dirty on 2015-10-30; PYBv1.0 with STM32F405RG
    Type "help()" for more information.
    >>> dir()
    ['__name__', 'pyb']
    >>>

特殊变量 _ (下划线)
-----------------------------------

使用REPL时，进行计算并得到结果。MicroPython将之前语句的结果储存到变量_（下划线）中。您可使用下划线将结果储存到变量中。例如:

    >>> 1 + 2 + 3 + 4 + 5
    15
    >>> x = _
    >>> x
    15
    >>>

原始模式
--------

原始模式并非用于日常使用，而是用于编程。其运行类似于关闭回应的粘贴模式。

点击Ctrl-A进入原始模式。发送您的python代码，然后点击Ctrl-D。Ctrl-D键将识别为"确定"，然后编译并执行python 代码。
所有输出（或故障）都会发送回去。点击Ctrl-B将会推出原始模式，并返回常规（又称友好型）REPL。

``tools/pyboard.py`` 程序使用原始REPL来在MicroPython板上执行python文件。