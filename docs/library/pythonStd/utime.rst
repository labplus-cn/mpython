:mod:`time` -- 时间相关函数
======================================

.. module:: time
   :synopsis: 时间相关函数

这个模块实现了相应 :term:`CPython` 模块的一个子集，如下所述。有关更多信息，请参阅原始CPython文档: `time <https://docs.python.org/3.5/library/time.html#module-time>`_

``time`` 模块提供用于获取当前时间和日期、测量时间间隔和延迟的函数。

**Time Epoch**: Unix端口使用1970-01-01 00:00-00:00 UTC的POSIX系统时间的标准。但是，内嵌端口使用2000-01-01 00:00:00 UTC的时间。


**维护实际日历日期/时间**: 这需要实时通信（RTC）。在具备底层OS的系统中，RTC可能是隐式的。设置和维护实际日历时间应是OS/RTOS的职能，
且在MicroPython之外完成，只使用OS API查询日期/时间。在baremetal端口中，系统时间取决于 ``machine.RTC()`` 对象。
当前日历时间可能使用 ``machine.RTC().datetime(tuple)`` 函数来设置，并通过以下方式维护:

* 由一个备用电池（对于特定板而言，可能是一个额外的可选组件）。
* 使用网络时间协议（需要通过一个端口/用户安装）。
* 每次开启电源都进行手动设置（许多板通过硬复位维护RTC时间，尽管有些可能需要在此情况下重新设置）。

若实际日历时间未使用系统/MicroPython RTC 维护，需引用当前绝对时间的函数可能与预期不符。

函数
---------

.. function:: localtime([secs])

   将一个以秒计的时间转换为一个包含下列内容的8元组：（年、月、日、小时、分钟、秒、一周中某日、一年中某日）。若未提供秒或为None，则使用RTC时间。

   * 年包括世纪（例如2014）
   * 月为 1-12
   * 日为 1-31
   * 小时为 0-23
   * 分钟为 0-59
   * 秒钟 0-59
   * 周中某日为 0-6 （对应周一到周日）
   * 年中某日为 1-366

.. function:: mktime()

   此为 ``localtime()`` 的逆函数，其参数为一个表示本地时间的8元组。返回一个表示2000年1月1日以来的秒钟的整数。

.. function:: sleep(seconds)

   休眠给定秒数的时间。秒钟数可为一个表示休眠时间的浮点数。注意：其他端口可能不接受浮点参数，为满足兼容性，使用 `sleep_ms()` 和 `sleep_us()` 函数。 

.. function:: sleep_ms(ms)

   延迟给定毫秒数，应为Positive或0。

.. function:: sleep_us(us)

   延迟给定的微秒数，应为Positive或0。

.. function:: ticks_ms()

    用在某些值（未指定）后结束后的任意引用点返回一个递增的毫秒计数器。该值应被视为不透明的，且仅适用于ticks_diff()。

    自动换行值未显式显示，但为简化讨论，我们将其称为 *TICKS_MAX* 。 该值的周期为  *TICKS_PERIOD = TICKS_MAX + 1* 。
     *TICKS_PERIOD* 须为2的幂，但也会因端口不同而不同。同一周期值用于 `ticks_ms()` 、 `ticks_us()` 、
      `ticks_cpu()` 函数（为简单起见）。因此，这些函数将返回一个介于 *[0 .. TICKS_MAX]* 的值，包括 *TICKS_PERIOD* 值。
    注意：仅使用非负值。多数情况下，您应将这些函数返回的值视为透明。对之唯一可用的操作为下述的 `ticks_diff()` 和 `ticks_add()` 函数。

    注意：在这些值上直接执行标准的数学操作(+, -)或关系运算符(<, <=, >, >=)将导致无效的结果。
    执行数字操作，并将结果作为参数传递给 ``ticks_diff()`` 或 ``ticks_add()`` 将导致后一个函数的无效结果。

.. function:: ticks_us()

   正如上述的 ``ticks_ms`` ，但以微秒为单位。

.. function:: ticks_cpu()

   与 ``ticks_ms`` 和 ``ticks_us`` 相似，但有更高的分辨率（通常CPU时钟）。
   
   这通常是CPU时钟，这也就是该函数如此命名的原因。但是并非必须为CPU时钟，系统中其他可用的定时源
   （例如高分辨率计时器）也可作为替代。该函数确切的定时单元（分辨率）未在 ``time`` 模块层指定，
   但是特定端口的文档可能提供更多具体信息。此函数设计用于非常精细的基准测试或非常紧凑的实时循环。请避免在可移植的程序编码中使用。

   可用性：并非每个端口都可以实现该函数。


.. function:: ticks_add(ticks, delta)

   用一个给定数字来抵消ticks值，该数字可为正或负。给定一个 *ticks* 值，该函数允许计算之前或之后的ticks value  *delta*  ticks，
   并遵循ticks值的模块化算术定义（见上 `ticks_ms()` ）。Ticks参数须为调用 `ticks_ms()` 、 `ticks_us()` 、 `ticks_cpu()` 函数
   （或先前调用的 `ticks_add()` ）的直接结果。但是，delta可为一个任意整数或一个数字表达。 `ticks_add()` 对计算事件/任务的截止时间非常有用。
   （注意：您必须使用 `ticks_diff()` 函数来处理截止时间。） 

   Examples::

        # Find out what ticks value there was 100ms ago 找到100ms前的ticks值
        print(ticks_add(time.ticks_ms(), -100))

        # Calculate deadline for operation and test for it 计算操作和测试的截止时间
        deadline = ticks_add(time.ticks_ms(), 200)
        while ticks_diff(deadline, time.ticks_ms()) > 0:
            do_a_little_of_something()

        # Find out TICKS_MAX used by this port 找到该端口使用的TICKS_MAX
        print(ticks_add(0, -1))


.. function:: ticks_diff(ticks1, ticks2)

   测量连续调用ticks_ms()、ticks_us()、icks_cpu()间的周期。
   由这些函数返回的值可能在任何时间停止，因此并不支持直接减去这些值，应使用ticks_diff()。 
   “旧”值实际上应及时覆盖“新”值，否则结果将未定义。该函数不应用于测量任意周期长的时间（因为ticks_*()函数包括且通常有短周期）。
   预期使用模式是使用超时实现事件轮询：


   参数顺序与减法操作符相同， ``ticks_diff(ticks1, ticks2)`` 与 ``ticks1 - ticks2`` 意义相同。
   但是，函数可能会围绕由 `ticks_ms()` 返回的值，因此在此使用减法将会产生错误结果。于是 `ticks_diff()` 应运而生，
   即使在环绕值情况下，它也能实现模块化（或者更确切地说，ring）算法生成正确值（只要它们之间的距离不太远，见下）。
   该函数返回介于[ *-TICKS_PERIOD/2 ..TICKS_PERIOD/2-1* ]的有符号整数值（这是两个互补的二进制整数的典型范围定义）。
   若该结果为负，则意味着 *ticks1* 发生在 *ticks2* 之前。否则，则意味着 *ticks1* 发生在 *ticks2* 之后。
   这只在距离彼此不超过 *TICKS_PERIOD/2-1*  ticks时成立。若未成立，则将返回错误结果。特别地，
   若两个tick值距离 *TICKS_PERIOD/2-1 ticks* ，则该值将由此函数返回。但是，若在其之间传递实时ticks的 *TICKS_PERIOD/2* ，
   该函数会返回 *TICKS_PERIOD/2* ，也就是说，结果值将会绕到可能值的负范围内。

   上述限制的常用原理：假设您被锁在一个房间里，只有一个标准12级时钟来记录时间进程。若您现在看一下表，
   并在接下来的13个小时中不再查看时间（例如您可能睡了很久），然后当您再次看表时，对您来说只过了1小时。
   为避免这种错误，请定时查看时间。您的应用程序也应如此。“睡太久”的比喻直接影射应用程序的行为：
   请勿让您的应用程序运行单一程序过久。按步骤运行任务，并在步骤进行时计时。

   `ticks_diff()` 设计适用于各种使用模式，其中包括:

   * 使用超时轮询。在此种情况下，事件顺序已知，您只需处理 `ticks_diff()` 的正结果::

        # Wait for GPIO pin to be asserted, but at most 500us 等待GPIO注脚确认，单最多等待500us
        start = time.ticks_us()
        while pin.value() == 0:
            if time.ticks_diff(time.ticks_us(), start) > 500:
                raise TimeoutError

   * 安排事件。在此种情况下，若某一事件超期，则 `ticks_diff()` 的结果可能为负::

        # This code snippet is not optimized 这一代码片段没有经过优化
        now = time.ticks_ms()
        scheduled_time = task.scheduled_time()
        if ticks_diff(now, scheduled_time) > 0:
            print("Too early, let's nap")
            sleep_ms(ticks_diff(now, scheduled_time))
            task.run()
        elif ticks_diff(now, scheduled_time) == 0:
            print("Right at time!")
            task.run()
        elif ticks_diff(now, scheduled_time) < 0:
            print("Oops, running late, tell task to run faster!")
            task.run(run_faster=true)

   注意：请勿将 `time()` 值传递给 `ticks_diff()` ，您应在此使用正常的数学运算。但是请注意 `time()` 可能（且将会）溢出。这被称为 https://en.wikipedia.org/wiki/Year_2038_problem .


.. function:: time()

   假设底层RTC是按照上述设置和维护的，则返回整数形式的秒钟数。若RTC未设定，该函数将返回一个特定于端口的引用点的秒数
   （对无电池支持的RTC的嵌入式电路板而言，通常在电源启动或复位后）。若您想开发可移植的MicroPython应用程序，
   您不应依赖该函数来提供高于第二精度的结果。若您需要更高精度，请使用 ``ticks_ms()`` 和 ``ticks_us()`` 函数。
   若您需要日历时间，无参数的 ``localtime()`` 不失为佳选。

   .. admonition:: Difference to CPython
      :class: attention

      在CPython中，该函数返回自Unix时刻，即1970-01-01 00:00 UTC始的浮点数形式的秒数，
      其精度通常可达微秒。使用MicroPython时，只有Unix端口使用相同时刻，若浮点精度允许，
      则返回次秒级精度。嵌入式硬件通常不具有浮点精度，可表示长时间范围和次秒级秒精度，
      因此它们使用具有第二精度的整数值。某些嵌入式硬件也缺乏电池供电的RTC，
      因此，返回自上次接通电源后或其他相关的制定硬件点的秒数（例：重置）。