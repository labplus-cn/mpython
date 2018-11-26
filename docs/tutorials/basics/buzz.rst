音乐
=========

掌控板板载无源蜂鸣器，其声音主要是通过高低不同的脉冲信号来控制而产生。声音频率可控，频率不同，发出的音调就不一样，从而可以发出不同的声音，还可以做出“多来米发索拉西”的效果。 

例：自定义乐谱:: 

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

**音符** :: 

C4：1指的是八度音阶中的音符“C”，持续一个音阶。如果使用音符名称R，则将其视为休息（静音）。在音调符号中，“#”表示将基本音级升高半音升；“b”表示将基本音级降低半音；“×”表示将基本音级升高两个半音（一个全音）；“bb”表示将基本音级降低两个半音（一个全音）；“ヰ”表示将已经升高或降低的音还原。

**内置旋律（音乐）** 

mPython2有很多内置的旋律，完整的清单如下：
 
* ``music.DADADADUM``  
* ``music.ENTERTAINER``  
* ``music.PRELUDE`` 
* ``music.ODE`` 
* ``music.NYAN`` 
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
