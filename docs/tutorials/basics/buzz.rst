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

::

from mpython import *
import music

# play Prelude in C.
notes = [
    'c4:1', 'e', 'g', 'c5', 'e5', 'g4', 'c5', 'e5', 'c4', 'e', 'g', 'c5', 'e5', 'g4', 'c5', 'e5',
    'c4', 'd', 'a', 'd5', 'f5', 'a4', 'd5', 'f5', 'c4', 'd', 'a', 'd5', 'f5', 'a4', 'd5', 'f5',
    'b3', 'd4', 'g', 'd5', 'f5', 'g4', 'd5', 'f5', 'b3', 'd4', 'g', 'd5', 'f5', 'g4', 'd5', 'f5',
    'c4', 'e', 'g', 'c5', 'e5', 'g4', 'c5', 'e5', 'c4', 'e', 'g', 'c5', 'e5', 'g4', 'c5', 'e5',
    'c4', 'e', 'a', 'e5', 'a5', 'a4', 'e5', 'a5', 'c4', 'e', 'a', 'e5', 'a5', 'a4', 'e5', 'a5',
    'c4', 'd', 'f#', 'a', 'd5', 'f#4', 'a', 'd5', 'c4', 'd', 'f#', 'a', 'd5', 'f#4', 'a', 'd5',
    'b3', 'd4', 'g', 'd5', 'g5', 'g4', 'd5', 'g5', 'b3', 'd4', 'g', 'd5', 'g5', 'g4', 'd5', 'g5',
    'b3', 'c4', 'e', 'g', 'c5', 'e4', 'g', 'c5', 'b3', 'c4', 'e', 'g', 'c5', 'e4', 'g', 'c5',
    'a3', 'c4', 'e', 'g', 'c5', 'e4', 'g', 'c5', 'a3', 'c4', 'e', 'g', 'c5', 'e4', 'g', 'c5',
    'd3', 'a', 'd4', 'f#', 'c5', 'd4', 'f#', 'c5', 'd3', 'a', 'd4', 'f#', 'c5', 'd4', 'f#', 'c5',
    'g3', 'b', 'd4', 'g', 'b', 'd', 'g', 'b', 'g3', 'b3', 'd4', 'g', 'b', 'd', 'g', 'b'
]

music.play(notes)