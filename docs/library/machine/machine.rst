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

   与按下外部 RESET按键效果一样.

.. function:: reset_cause()

   获得重置原因。请参阅  :ref:`常数 <machine_constants>`  以了解可能的返回值。


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

   停止CPU并禁用除WLAN之外的所有外围设备。从请求睡眠的位置恢复执行。为了唤醒实际发生，应首先配置唤醒源。

.. function:: deepsleep()

    停止CPU和所有外围设备（包括网络接口，如果有）。执行从主脚本恢复，就像重置一样。
    可以检查重置原因以了解我们来自哪里 :data:`machine.DEEPSLEEP` 。为了唤醒实际发生，应首先配置唤醒源，如 :class:`Pin` 更改或 :class:`RTC` 超时。


.. function:: wake_reason()

    得到唤醒原因。请参阅  :ref:`常数 <machine_constants>` 以了解可能的返回值。

其他函数
-----------------------

.. function:: rng()

    返回一个24 bit软件生成的随机数.

.. function:: unique_id()

    返回 board/ SoC的唯一标识符的字节字符串。如果底层硬件允许，它将从board/ SoC实例变化到另一个实例。
    长度因硬件而异（如果您需要短ID，请使用完整值的子字符串）。在某些MicroPython端口中，ID对应于网络MAC地址。

.. function:: time_pulse_us(pin, pulse_level, timeout_us=1000000)

    在给定的引脚上测试外部脉冲电平持续时间，并以微秒为单位返回外部脉冲电平的持续时间。 ``pulse_level`` =1测试高电平持续时间，pulse_level=0测试低电平持续时间。
    当设置电平和现在脉冲的电平不一致时，则会等到输入电平和设置的电平一致时开始计时，如果设置的电平和现在脉冲的电平一致时，那么就会立即开始计时。
    当引脚电平和设置电平一直相反时，则会等待超时，超时返回-2。当引脚电平和设置电平一直相同时，也会等待超时，超时返回-1， ``timeout_us`` 即为超时时间。

.. _machine_constants:

常量
---------

.. data:: machine.IDLE
          machine.SLEEP
          machine.DEEPSLEEP

    IRQ 唤醒值. 

.. data:: machine.PWRON_RESET
          machine.HARD_RESET
          machine.WDT_RESET
          machine.DEEPSLEEP_RESET
          machine.SOFT_RESET

    重置原因.

.. data:: machine.WLAN_WAKE
          machine.PIN_WAKE
          machine.RTC_WAKE

    唤醒原因.
