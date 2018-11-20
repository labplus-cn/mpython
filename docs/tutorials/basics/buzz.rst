蜂鸣器
=========

buzz
----

我们可以使用 ``buzz`` 对象很容易的驱动蜂鸣器发出声音::

    >>> from mpython import *
    >>> buzz.on()
    >>> buzz.on(1000)
    >>> buzz.off()
    >>>

.. Note::

    ``buzz.on(freq=500)`` 是以设定的频率打开无源蜂鸣器。当不给定freq参数 ``buzz.on()`` ，默认以500Hz驱动蜂鸣器。``buzz.off()`` 为关闭蜂鸣器。


我们可以用 ``buzz.freq()`` 来切换频率，以下是播放七阶音符示例::

    from mpython import *
    import time
    
    tone = [262,294,330,349,392,440,494]     #七音阶
    
    def playMusic(tune,duration):
        buzz.on()
        for i in range(len(tune)):
            buzz.freq(int(tune[i]))
            time.sleep_ms(duration)
        buzz.off()
    

    playMusic(tone,500)

.. Note::

    不同的音调为特定的频率的声音。所以要发出某个音调可以该音调频率驱动蜂鸣器即可。


music
-----

music模块