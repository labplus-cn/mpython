.. currentmodule:: machine
.. _machine.Pin:

.. module:: machine.Pin

类 Pin -- 控制 I/O 引脚
=============================

引脚对象用于控制I / O引脚（也称为GPIO - 通用输入/输出）。引脚对象通常与可以驱动输出电压和读取输入电压的物理引脚相关联。
引脚类具有设置引脚模式（IN，OUT等）的方法以及获取和设置数字逻辑电平的方法。有关引脚的模拟控制, 请参阅 :class:`ADC` 类.

通过使用明确指定某个I / O引脚的标识符来构造引脚对象。允许的标识符形式和标识符映射到的物理引脚是特定于端口的。
标识符的可能性是整数，字符串或具有端口和引脚号的元组。

示例::

    from machine import Pin

    # create an output pin on pin #32
    p0 = Pin(32, Pin.OUT)

    # set the value low then high
    p0.value(0)
    p0.value(1)

    # create an input pin on pin #33, with a pull up resistor
    p2 = Pin(33, Pin.IN, Pin.PULL_UP)


    # configure an irq callback
    p2.irq(trigger=Pin.IRQ_FALLING, handler=lambda t:print("IRQ"))

构建对象
------------

.. class:: Pin(id, mode=1, pull=1, value, drive, alt)

  访问与给定相关的引脚外设（GPIO引脚） ``id`` 。如果在构建对象中给出了其他参数，则它们用于初始化引脚。
  未指定的任何设置将保持其先前的状态。

   参数:

     - ``id`` 是强制性的，可以是任意对象。可能的值类型包括：int（内部引脚标识符），str（引脚名称）和元组（[port，pin]对）。

     - ``mode`` 指定引脚模式，可以是以下之一：

       - ``Pin.IN`` - 引脚配置为输入。如果将其视为输出，则引脚处于高阻态。

       - ``Pin.OUT`` - 引脚配置为（正常）输出。

       - ``Pin.OPEN_DRAIN`` -引脚配置为开漏输出。开漏输出以下列方式工作：如果输出值设置为0，则引脚处于低电平有效; 如果输出值为1，则引脚处于高阻态。并非所有端口都实现此模式，或某些端口可能仅在某些引脚上实现。


       - ``Pin.ALT`` - 引脚配置为执行替代功能，该功能是端口特定的。对于以这种方式配置的引脚，任何其他Pin方法（除外 :meth:`Pin.init` ）都不适用
         （调用它们将导致未定义或特定于硬件的结果）。并非所有端口都实现此模式。


       - ``Pin.ALT_OPEN_DRAIN`` - 和 ``Pin.ALT`` 相同，但引脚配置为漏极开路。并非所有端口都实现此模式。

     - ``pull`` 指定引脚是否连接了（弱）拉电阻，可以是以下之一：

       - ``None`` - 无上拉或下拉电阻
       - ``Pin.PULL_UP`` - 上拉电阻使能
       - ``Pin.PULL_DOWN`` - 下拉电阻使能

     - ``value`` 仅对Pin.OUT和Pin.OPEN_DRAIN模式有效，并指定初始输出引脚值，否则引脚外设的状态保持不变。

     - ``drive`` 指定引脚的输出功率，可以是：Pin.LOW_POWER， Pin.MED_POWER或Pin.HIGH_POWER。实际的电流驱动能力取决于端口。并非所有端口都实现此参数。

     - ``alt`` 指定引脚的复用功能，它可以采用的值取决于端口。此参数仅对Pin.ALT和Pin.ALT_OPEN_DRAIN 模式有效。当引脚支持多个复用功能时，可以使用它。如果仅支持一个引脚复用功能，则不需要此参数。并非所有端口都实现此参数。


   如上所述，Pin类允许为特定引脚设置复用功能，但它不在此类引脚上指定任何进一步的操作。
   在复用功能模式下配置的引脚通常不用作GPIO，而是由其他硬件外设驱动。
   这种引脚支持的唯一操作是通过调用构建对象或 :meth:`Pin.init` 方法重新初始化。
   如果引脚在复用功能模式下配置 ``Pin.IN`` ， ``Pin.OUT`` 或者  ``Pin.OPEN_DRAIN`` 将重新初始化  ，复用功能将从pin中删除。

方法
-------

.. method:: Pin.init(mode=1, pull=1, value, drive, alt)

   使用给定参数重新初始化引脚。只会设置指定的参数。引脚外围状态的其余部分将保持不变。
   有关参数的详细信息，请参阅构建对象文档。

   返回 ``None``.


.. method:: Pin.value([x])

   此方法允许设置和获取引脚的值，具体取决于是否 ``x`` 提供参数。

   如果省略该参数，则该方法获得引脚的数字逻辑电平，分别返回对应于低电压信号和高电压信号的0或1。
   此方法的行为取决于引脚的模式：

     - ``Pin.IN`` -  该方法返回引脚上当前存在的实际输入值.
     - ``Pin.OUT`` - 该方法的行为和返回值未定义.
     - ``Pin.OPEN_DRAIN`` - 如果引脚处于状态“0”，则方法的行为和返回值未定义。否则，如果引脚处于状态“1”，则该方法返回引脚上当前存在的实际输入值。.

   
如果提供了参数，则此方法设置引脚的数字逻辑电平。参数x可以是转换为布尔值的任意值。
如果转换为True，则将引脚设置为状态“1”，否则将其设置为“0”状态。此方法的行为取决于引脚的模式：



     - ``Pin.IN`` - 该值存储在引脚的输出缓冲区中。引脚状态不会改变，它仍然处于高阻态。一旦更改为 ``Pin.OUT`` 或 ``Pin.OPEN_DRAIN`` 模式，存储的值将在引脚上激活。
     - ``Pin.OUT`` -  输出缓冲区立即设置为给定值。
     - ``Pin.OPEN_DRAIN`` - 如果值为“0”，则引脚设置为低电压状态。否则，引脚被设置为高阻态。

   设置此方法返回的值时 ``None``.

.. _Pin.irq:

.. method:: Pin.irq(handler=None, trigger=(Pin.IRQ_FALLING | Pin.IRQ_RISING), priority=1, wake=None)

   配置在引脚的触发源处于活动状态时调用的中断处理程序。如果引脚模式是， ``Pin.IN`` 则触发源是引脚上的外部值。
   如果引脚模式是， ``Pin.OUT`` 则触发源是引脚的输出缓冲器。
   否则，如果引脚模式是， ``Pin.OPEN_DRAIN`` 那么触发源是状态'0'的输出缓冲器和状态'1'的外部引脚值。

参数:

     - ``handler`` 是一个可选的函数，在中断触发时调用。

     - ``trigger`` 配置可以触发中断的事件。可能的值是：

       - ``Pin.IRQ_FALLING`` 下降沿中断
       - ``Pin.IRQ_RISING`` 上升沿中断
       - ``Pin.IRQ_LOW_LEVEL`` 低电平中断
       - ``Pin.IRQ_HIGH_LEVEL`` 高电平中断

       这些值可以一起进行 ``OR`` 运算以触发多个事件。

     - ``priority`` 设置中断的优先级。它可以采用的值是特定于端口的，但是更高的值总是代表更高的优先级。

     - ``wake`` 选择此中断可唤醒系统的电源模式。它可以是 ``machine.IDLE`` ， ``machine.SLEEP`` 或 ``machine.DEEPSLEEP`` 。
     这些值也可以进行 ``OR`` 运算，使引脚在多种功耗模式下产生中断。

  此方法返回一个回调对象。

常量
---------

以下常量用于配置引脚对象。请注意，并非所有端口都可以使用所有常量。

.. data:: Pin.IN
          Pin.OUT
          Pin.OPEN_DRAIN
          Pin.ALT
          Pin.ALT_OPEN_DRAIN

  选择引脚模式。

.. data:: Pin.PULL_UP
          Pin.PULL_DOWN

   选择是否有上拉/下拉电阻。使用None无拉的值 。
   ``None`` for no pull.

.. data:: Pin.LOW_POWER
          Pin.MED_POWER
          Pin.HIGH_POWER

   选择引脚驱动强度。

.. data:: Pin.IRQ_FALLING
          Pin.IRQ_RISING
          Pin.IRQ_LOW_LEVEL
          Pin.IRQ_HIGH_LEVEL

  选择IRQ触发类型。
