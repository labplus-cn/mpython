REPL-交互式解析
=================================

使用MicroPython的一个主要的优点是交互式的REPL。REPL（read-evaluate-print loop）代表读取﹣求值﹣输出循环。
REPL对于学习一门新的编程语言具有很大的帮助，因为它能立刻对初学者做出回应。这意味着你可以马上执行代码，查看结果，而无需先经过编译然后上传的繁琐步骤。
mPython掌控要让REPL在Windows上工作，您需要安装cp2104的串口驱动程序。


串口连接
-------------------------

要通过USB-serial访问，您需要使用串口终端软件。在Windows上如kitty、xshell、都是不错的选择。设置
波特率为115200，就可以开始玩micropython了。

通过串行端口建立连接后，您可以通过按几次输入来测试它是否正常工作。您应该看到Python REPL提示符，表示为 ``>>>`` 。

使用 REPL
--------------

一旦有提示，您就可以开始尝试了！按Enter键后，将在提示符处键入任何内容。
MicroPython将运行您输入的代码并打印结果（如果有的话）。如果输入的文本出错，则会打印出错误消息。

尝试在提示符下输入以下内容::

    >>> print('hello mPython')
    hello mPython


请注意，您不应键入 ``>>>`` 箭头，它们表示您应在提示符后键入文本。接下来的行是响应的内容。

如果您已经了解了一些python，现在可以在这里尝试一些基本命令。例如::

    >>> 1+2
    3
    >>> 1/2
    0.5
    >>> 12*34
    408


可以尝试下载mPython的oled显示屏上显示字符::

    >>> from mpython import display
    >>> display.DispChar('hello,world!',0,0)
    >>> display.show()
    >>> 

.. Note::

    ``display.DispChar(str,x,y)``   ``str`` 为要显示的字符串， ``x`` 、``y`` 为显示起点的xy坐标。
    然后用 ``display.show()`` 刷新屏幕后，字符串即可显示在oled上。现在你可以尝试下在其他位置显示任意字符串。



行编辑
~~~~~~~~~~~~

您可以使用向左和向右箭头键来编辑当前输入的行以移动光标，以及删除和退格键。
此外，按Home或ctrl-A将光标移动到行的开头，按End或ctrl-E移动到行的末尾。

输入历史记录
~~~~~~~~~~~~~

REPL会记住您输入的一定数量的前一行文本（ESP32上最多8行）。
要调用上一行，请使用向上和向下箭头键。

Tab键
~~~~~~~~~~~~~~

Tab键可以查看模块所有成员列表。这对于找出模块或对象具有的函数和方法非常有用。
假设你在上面的例子中导入了machine然后键入 ``.`` 再次按Tab键以查看machine模块所有成员列表::

    >>> machine.
    __class__       __name__        ADC             DAC
    DEEPSLEEP       DEEPSLEEP_RESET                 EXT0_WAKE
    EXT1_WAKE       HARD_RESET      I2C             PIN_WAKE
    PWM             PWRON_RESET     Pin             RTC
    SLEEP           SOFT_RESET      SPI             Signal
    TIMER_WAKE      TOUCHPAD_WAKE   Timer           TouchPad
    UART            ULP_WAKE        WDT             WDT_RESET
    deepsleep       disable_irq     enable_irq      freq
    idle            mem16           mem32           mem8
    reset           reset_cause     sleep           time_pulse_us
    unique_id       wake_reason
    >>> machine.


行继续和自动缩进
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

您键入的某些内容将需要“继续”，也就是说，需要更多行文本才能生成正确的Python语句。在这种情况下，
提示符将更改为，...并且光标将自动缩进正确的数量，以便您可以立即开始键入下一行。
通过定义以下函数来尝试此操作::


    >>> def toggle(p):
    ...    p.value(not p.value())
    ...    
    ...    
    ...    
    >>>

在上面，您需要连续按三次Enter键才能完成复合语句（即三条线上只有点）。
完成复合语句的另一种方法是按退格键到达行的开头，然后按Enter键。
（如果你输错了什么并且想要退出，那么按ctrl-C;所有行都将被忽略。）

您刚刚定义函数功能为翻转引脚电平。您之前创建的pin对象应该仍然存在
（如果没有，则重新创建它），您可以使用以下命令翻转LED::

    >>> toggle(pin)

现在让我们在一个循环中翻转LED（如果你没有LED，那么你可以打印一些文本而不是调用切换，看看效果）：

    >>> import time
    >>> while True:
    ...     toggle(pin)
    ...     time.sleep_ms(500)
    ...    
    ...    
    ...    
    >>>

这将以1Hz（半秒开，半秒关）翻转LED。要停止切换按 ``ctrl-C`` ，这将引发KeyboardInterrupt异常并退出循环


粘贴模式
~~~~~~~~~~

按 ``ctrl-E`` 将进入特殊粘贴模式。这允许您将一大块文本复制并粘贴到REPL中。如果按ctrl-E，您将看到粘贴模式提示::

    paste mode; Ctrl-C to cancel, Ctrl-D to finish
    === 

然后，您可以粘贴（或键入）您的文本。请注意，没有任何特殊键或命令在粘贴模式下工作（例如Tab或退格）
，它们只是按原样接受。按 ``ctrl-D`` 完成输入文本并执行。

其他控制命令
~~~~~~~~~~~~~~~~~~~~~~

还有其他四个控制命令：

* 空白行上的Ctrl-A将进入原始REPL模式。这类似于永久粘贴模式，除了不回显字符。

* 空白处的Ctrl-B转到正常的REPL模式。

* ``Ctrl-C`` 取消任何输入，或中断当前运行的代码。

* 空白行上的 ``Ctrl-D`` 将执行软重启。


