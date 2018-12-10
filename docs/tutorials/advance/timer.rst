定时器
=======

人类最早使用的定时工具是沙漏或水漏，但在钟表诞生发展成熟之后，人们开始尝试使用这种全新的计时工具来改进定时器，达到准确控制时间的目的。定时器让很多需要人控制时间的工作变得简单了许多，不少家用电器用定时器来控制开关或工作时间。

例：定时警报器
::

    from mpython import *
    from machine import Timer
    import music

    def playMusic(_):             #定义定时器回调函数，播放警报声
        music.play(music.BA_DING)

    tim1 = Timer(1)               #创建定时器1

    tim1.init(period=5000, mode=Timer.PERIODIC,callback=playMusic)        #配置定时器，模式为循环执行，循环周期为5秒

    while True:
        timerNum=tim1.value()
        oled.DispChar("定时器：%d ms" %timerNum,20,25)
        oled.show()
        oled.fill(0) 


使用前，导入mpython、Timer、music模块::

    from mpython import *
    from machine import Timer
    import music

定义定时器回调函数，播放警报声::

    def playMusic(_):             
        music.play(music.BA_DING,wait=False)

配置定时器，模式为循环执行，循环周期为5秒::

    tim1.init(period=5000, mode=Timer.PERIODIC,callback=playMusic)

.. Note::

    Timer.init(period=5000, mode=Timer.PERIODIC,callback=None)  用来初始化计时器，``mode`` 可以是以下之一：``Timer.ONE_SHOT`` 指计时器运行一次，直到配置完毕通道的期限到期；``Timer.PERIODIC`` 指定时器以通道的配置频率定期运行。

获取并返回计时器当前计数值，然后显示在OLED显示屏上::

    timerNum=tim1.value()
    oled.DispChar("定时器：%d ms" %timerNum,20,25)
    oled.show()

.. Note::

    timer.value() 函数为获取并返回当前计数值。

.. Attention:: 

    您可能会看到定时器没到5000ms整警报声就响了，这是因为定时数据传送到OLED显示屏上这个过程中有延时。