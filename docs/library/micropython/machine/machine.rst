:mod:`machine` --- 与硬件相关的功能
====================================================

.. module:: machine
   :synopsis: 与硬件相关的功能

该 ``machine`` 模块包含与特定电路板上的硬件相关的特定功能。该模块中的大多数功能允许直接和不受限制地访问和控制系统上的硬件块（如CPU，定时器，总线等）。
使用不当，可能导致故障，锁定，电路板崩溃，以及在极端情况下硬件损坏。

.. _machine_callbacks:

关于 :mod:`machine` 模块的函数和类方法使用的回调的注释：所有这些回调应被视为在中断上下文中执行。
这对于ID> = 0的物理设备和具有负ID（例如-1）的“虚拟”设备都是如此（这些“虚拟”设备在真实硬件和实际硬件中断之上仍然是薄的垫片）。
请参见 :ref:`中断处理程序 <isr_rules>`



 .. toctree::
   :maxdepth: 1

   machine.Pin.rst
   machine.ADC.rst 
   machine.TouchPad.rst
   machine.PWM.rst
   machine.UART.rst
   machine.I2C.rst
   machine.SPI.rst
   machine.Timer.rst
   machine.RTC.rst
   machine.WDT.rst






复位相关函数
-----------------------

.. function:: reset()

    与按下外部 RESET复位按键效果一样.

.. function:: reset_cause()

    获得重启原因。

    ==================== ======  ====================================  
     重启原因              数值    定义
    ==================== ======  ====================================  
     PWRON_RESET          1      上电重启 
     HARD_RESET           2      硬重启
     WDT_RESET            3      看门狗计时器重启 
     DEEPSLEEP_RESET      4      从休眠重启 
     SOFT_RESET           5      软重启 
    ==================== ======  ====================================  



中断相关函数
---------------------------

.. function:: disable_irq()

    禁用中断请求。返回先前的IRQ状态，该状态应被视为不透明值。 :func:`enable_irq()` 在 :func:`disable_irq()` 调用之前，
    应将此返回值传递给函数以将中断恢复到其原始状态。


.. function:: enable_irq(state)

    重新启用中断请求。 :func:`state` 参数应该是最近一次调用  :func:`disable_irq()` 函数时返回的值。

电源相关函数
-----------------------

.. function:: freq()

    返回 CPU 频率,单位Hz

.. function:: idle()

   为CPU提供时钟，有助于在短期或长期内随时降低功耗。一旦触发任何中断，外设继续工作并继续执行
   （在许多端口上，这包括以毫秒级的规则间隔发生的系统定时器中断）。

.. function:: sleep()

   .. note:: 不推荐使用此函数，可用lightsleep()不带参数。

.. function:: deepsleep()

    停止执行以尝试进入低功率状态。

    如果指定了time_ms，那么这将是睡眠将持续的最长时间（以毫秒为单位）。否则睡眠可以无限期地持续。

    无论有没有时间，如果有需要处理的事件，执行可以随时恢复。应该在休眠之前配置此类事件或唤醒源，如 `Pin` 更改或 `RTC` 超时。

    ``lightsleep`` 和 ``deepsleep`` 的精确行为和省电功能在很大程度上取决于底层硬件，但一般属性是：

        - lightsleep具有完整的RAM和状态保留。唤醒后，从请求睡眠的点恢复执行，所有子系统都可以运行。
        - 深度睡眠可能不会保留RAM或系统的任何其他状态（例如外围设备或网络接口）。唤醒后，从主脚本恢复执行，类似于硬复位或上电复位。该 `reset_cause()` 函数将返回 `machine.DEEPSLEEP` ，这可用于区分深度睡眠唤醒与其他重置。
    


.. function:: wake_reason()

    返回唤醒原因。
        
    ==================== ======  ====================================  
    唤醒原因              数值    定义
    ==================== ======  ====================================  
    PIN_WAKE/EXT0_WAKE     2      单个RTC_GPIO唤醒
    EXT1_WAKE              3      多RTC_GPIO唤醒
    TIMER_WAKE             4      定时器唤醒
    TOUCHPAD_WAKE          5      触摸唤醒
    ULP_WAKE               6      协处理器唤醒
    ==================== ======  ====================================  



其他函数
-----------------------



.. function:: unique_id()

    返回 board/ SoC的唯一标识符的字节字符串。如果底层硬件允许，它将从board/ SoC实例变化到另一个实例。
    长度因硬件而异（如果您需要短ID，请使用完整值的子字符串）。在某些MicroPython端口中，ID对应于网络MAC地址。

    >>> machine.unique_id()
    b'\xccP\xe3\x90\xeb\xd4'

.. function:: time_pulse_us(pin, pulse_level, timeout_us=1000000)

    在给定的引脚上测试外部脉冲电平持续时间，并以微秒为单位返回外部脉冲电平的持续时间。 ``pulse_level`` =1测试高电平持续时间，pulse_level=0测试低电平持续时间。
    当设置电平和现在脉冲的电平不一致时，则会等到输入电平和设置的电平一致时开始计时，如果设置的电平和现在脉冲的电平一致时，那么就会立即开始计时。
    当引脚电平和设置电平一直相反时，则会等待超时，超时返回-2。当引脚电平和设置电平一直相同时，也会等待超时，超时返回-1， ``timeout_us`` 即为超时时间。

.. function:: rng()

    返回一个24 bit软件生成的随机数.

.. _machine_constants:

常量
---------

IRQ唤醒值
^^^^^^^^

.. data:: machine.SLEEP

    2

.. data:: machine.DEEPSLEEP

    4

重启原因
^^^^^^^

.. data:: machine.PWRON_RESET
          machine.HARD_RESET
          machine.WDT_RESET
          machine.DEEPSLEEP_RESET
          machine.SOFT_RESET


唤醒原因
^^^^^^^^

.. data:: machine.PIN_WAKE
          machine.EXT0_WAKE
          machine.EXT1_WAKE
          machine.TIMER_WAKE
          machine.TOUCHPAD_WAKE
          machine.ULP_WAKE


