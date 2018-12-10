音乐
=========

掌控板板载无源蜂鸣器，其声音主要是通过高低不同的脉冲信号来控制而产生。声音频率可控，频率不同，发出的音调就不一样，从而可以发出不同的声音，还可以做出“多来米发索拉西”的效果。 

内置旋律
+++++++

掌控板有很多内置的旋律，完整的清单如下：
 
* ``music.DADADADUM``  
* ``music.ENTERTAINER``  
* ``music.PRELUDE`` 
* ``music.ODE`` 
* ``music.NYAN`` 
* ``music.RINGTONE`` 
* ``music.FUNK`` 
* ``music.BLUES`` 
* ``music.BIRTHDAY`` 
* ``music.WEDDING`` 
* ``music.FUNERAL`` 
* ``music.PUNCHLINE`` 
* ``music.PYTHON`` 
* ``music.BADDY`` 
* ``music.CHASE`` 
* ``music.BA_DING`` 
* ``music.WAWAWAWAA`` 
* ``music.JUMP_UP`` 
* ``music.JUMP_DOWN`` 
* ``music.POWER_UP`` 
* ``music.POWER_DOWN`` 

我们可以播放一些内置旋律:: 

    import music
   
    music.play(music.BIRTHDAY)

.. admonition:: 提示

    music.BIRTHDAY指内置旋律的名称，如若播放其它旋律，只需把music.BIRTHDAY更换为想要播放的旋律即可。
除了播放内置旋律，我们还可以自编乐谱。

自编乐谱
+++++++

我们可以通过设置音调来自编乐谱。

:: 

    import music

    tune = ["C4:4", "D4:4", "E4:4", "C4:4", "C4:4", "D4:4", "E4:4", "C4:4",
            "E4:4", "F4:4", "G4:8", "E4:4", "F4:4", "G4:8"]
    music.play(tune)

每个音符都有一个名字（比如C＃或F），一个八度和一个持续时间。八度用数字表示〜0表示最低八度，4表示中央C，8表示您需要的高度。持续时间也表示为数字。 持续时间的值越高，持续时间越长。例如，持续时间4将持续两倍于持续时间2（依此类推）。
每个音符都表示为一串字符，如下所示：
:: 
   
    NOTE[octave][:duration]

例如，C4：4指的是八度音阶4中的音符“C”，持续4个音阶。如果使用音符名称R，则将其视为休息（静音）。

    
频率
+++++++

您还可以通过频率设置来制作一些非音符的音调。 例如，创建警笛效果：
:: 

    import music

    while True:
        for freq in range(880, 1760, 16):
            music.pitch(freq, 20)
        for freq in range(1760, 880, -16):
            music.pitch(freq,20)


在这个实例中是如何使用 ``music.pitch`` 方法，它需要一个频率。
其中range函数用于生成数值范围。这些数字用于定义音调的高低。
range函数有三个参数，分别是起始值，结束值和步长。因此，range的第一次使用是“以16的步长创建880到1760之间的数字范围”；
第二个次是“以-16”的步长创建1760到880之间的一系列值，持续频率为20毫秒。因此获得像警报器一样在频率上升和下降的频率范围而制作出警笛效果。