.. _music.py:

.. module:: music

music 模块
=======

music模块与microbit的music使用方法相同。

要使用music模块，你需要::

    import music

音符
++++

以下是音符格式::

    NOTE[octave][:duration]


例如，``A1:4`` 指的是八度音程中的音符"A"，持续四个节拍（节拍可以由 ``set_tempo`` 函数设定 - 见下文）。
如果使用音符 ``R`` ，则将其视为休息（静音）。

在音调符号中，“#”表示将基本音级升高半音；“b”表示将基本音级降低半音；例如，Ab是A-升半音并且C#是C-降半音。

octave默认状态下等于4，为中音阶；duration默认状态是4节拍；


贝多芬第五交响曲的开头::

    ['r4:2', 'g', 'g', 'g', 'eb:8', 'r:2', 'f', 'f', 'f', 'd:8']

八度音阶的定义和范围符合本页列出的关于科学音高表示法的表格 `on this
page about scientific pitch notation`_.  例如，middle "C"是 ``c4`` 和concert “A”（440）是 ``a4`` 。八度音符从音符"C"开始。

.. _on this page about scientific pitch notation: https://en.wikipedia.org/wiki/Scientific_pitch_notation#Table_of_note_frequencies


函数
++++++++

.. function:: set_tempo(ticks=4, bpm=120)

    设置播放节拍

    一定数量的ticks(整数)构成单个节拍。每个节拍以每分钟特定频率播放（每分钟节拍 - 也是整数）。

    可参考以下设置播放节拍:

    * ``music.set_tempo()`` - 将节拍设置恢复为 ticks = 4, bpm = 120
    * ``music.set_tempo(ticks=8)`` - 只改变单节拍速度
    * ``music.set_tempo(bpm=180)`` - 只改变节拍频率

    计算滴答的长度（以毫秒为单位）是非常简单的算术： ``60000/bpm/ticks_per_beat`` 。
    对于那些是默认的值或。 ``60000/120/4 = 125 milliseconds`` or ``1 beat = 500 milliseconds``。

.. function:: get_tempo()

    获取当前速度作为整数元组: ``(ticks, bpm)``.

.. function:: play(music, pin=6, wait=True, loop=False)

    - ``music`` 

        - 播放 ``music`` 包含上面定义的音乐DSL。

        - 如果 ``music`` 是一个字符串，则应该是单个音符，例如 ``'c1:4'``。

        - 如果 ``music`` 被指定为音符列表（如上面音乐DSL部分中所定义），则它们一个接一个地播放以执行旋律。

    - ``pin`` 默认是掌控板的P6引脚

    - ``wait`` 阻塞：如果 ``wait`` 设置为 ``True``, 为阻塞,否则未不。

    - ``loop`` ：如果 ``loop`` 设置为 ``True`` ，则重复调整直到stop被调用（见下文）或阻塞调用被中断。
   

.. function:: pitch(frequency, duration=-1, pin=6, wait=True)

    - ``frequency``, ``duration``:以给定指定毫秒数的整数频率播放频率。例如，如果频率设置为440并且长度设置为1000，那么我们会听到标准A调一秒钟。

        如果 ``duration`` 为负，则连续播放频率，直到阻塞或者被中断，或者在后台呼叫的情况下，设置或调用新频率stop（见下文）。

    - ``pin`` 默认是掌控板的P6引脚。

        请注意，您一次只能在一个引脚上播放频率。

    - ``wait`` 阻塞：如果 ``wait`` 设置为 ``True``, 为阻塞,否则未不。


.. function:: stop(pin=6)
    
   停止给定引脚上的所有音乐播放。

    - ``pin`` 默认是掌控板的P6引脚。

.. function:: reset()

    以下列方式重置以下属性的状态

        * ``ticks = 4``
        * ``bpm = 120``
        * ``duration = 4``
        * ``octave = 4``

内置旋律
++++++++

出于教育和娱乐的目的，该模块包含几个以Python列表表示的示例曲调。它们可以像这样使用：

    >>> import music
    >>> music.play(music.NYAN)

所有音乐都不受版权保护，由Nicholas H.Tollervey撰写并发布到公共领域或者有一位不知名的作曲家，并受到公平（教育）使用条款的保护。

它们是:

    * ``DADADADUM`` - 贝多芬第五交响曲C小调开幕式。
    * ``ENTERTAINER`` - 斯科特乔普林的Ragtime经典作品“The Entertainer”的开场片段。
    * ``PRELUDE`` - JSBach的48首前奏曲和赋格曲的第一首C大调前奏曲的开篇。
    * ``ODE`` - 贝多芬第七交响曲D小调的“欢乐颂”主题。
    * ``NYAN`` - Nyan Cat主题 (http://www.nyan.cat/). 作曲家不详。
    * ``RINGTONE`` - 听起来像手机铃声的东西。用于指示传入消息。
    * ``FUNK`` - 为秘密特工和犯罪主谋提供的时髦低音系列。
    * ``BLUES`` - 一个boogie-woogie 12杆蓝调步行低音。
    * ``BIRTHDAY`` - “生日快乐" 版权状态见: http://www.bbc.co.uk/news/world-us-canada-34332853
    * ``WEDDING`` - 来自瓦格纳歌剧“Lohengrin”的新娘合唱。.
    * ``FUNERAL`` -  “葬礼进行曲”，也被称为FrédéricChopin的钢琴奏鸣曲第2号B-minor,Op 35。
    * ``PUNCHLINE`` -一个有趣的片段表明一个笑话已经被创造出来了。
    * ``PYTHON`` - John Philip Sousa的游行“Liberty Bell”又名“Monty Python's Flying Circus”的主题（之后以Python编程语言命名）。
    * ``BADDY`` - 沉默的电影时代入口的一个坏人。
    * ``CHASE`` - 无声电影时代的追逐场景。
    * ``BA_DING`` - 表示发生了某些事情的短信号
    * ``WAWAWAWAA`` - 一个非常悲伤的长号。
    * ``JUMP_UP`` - 用于游戏，表示向上移动。
    * ``JUMP_DOWN`` - 用于游戏，表示向下移动。
    * ``POWER_UP`` - 一种炫耀，表明一项成就被释放。
    * ``POWER_DOWN`` - 一种悲伤，表示一项成就已经失去。

示例::

    """
        music.py
        ~~~~~~~~

        Plays a simple tune using the Micropython music module.
        This example requires a speaker/buzzer/headphones connected to P0 and GND.
    """
    from microbit import *
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