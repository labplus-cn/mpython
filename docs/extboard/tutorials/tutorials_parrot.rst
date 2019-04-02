.. _extboard_tutorials:

拓展板入门教程
============

本章节将讲解掌控拓展板parrot基本的使用,如电机驱动、语音播放、TTS语音合成等功能。有关,掌控拓展板技术参数详细说明,请查阅 :ref:`掌控拓展板介绍 <extboard_introduce>` 章节。  

.. image:: /images/extboard/extboard_back.png

准备
-------

首先,需要先将拓展板的 ``parrot`` 模块,你可以到 https://github.com/labplus-cn/mPython_parrot 获取。
将 ``parrot.py`` 上传到文件系统中。
或者你也可以用 ``upip.install("mPython-parrot")`` 的方法获取pypi包。


电机驱动
-------

拓展板支持2路的PWM电机驱动,你可以使用直流电机马达,如TT马达,N20等。

下面讲解,使用电机如何编程

首先导入parrot模块::

    import parrot

M1、M2,正转速度设为80::

    import parrot                           # 导入parrot 模块

    parrot.set_speed(parrot.MOTOR_1,80)       #  设置M1正转,速度为80
    parrot.set_speed(parrot.MOTOR_2,80)       #  设置M2正转,速度为80

反转::

    parrot.set_speed(parrot.MOTOR_1,-80)      #  设置M1反转,速度为80
    parrot.set_speed(parrot.MOTOR_2,-80)      #  设置M2反转,速度为80

停止::

    parrot.set_speed(parrot.MOTOR_1,0)        # 停止
    parrot.set_speed(parrot.MOTOR_2,0)        # 停止


控制电机速度使用到函数 ``set_speed(motor_no, speed)`` 。``motor_no`` 参数为电机编号,可选编号常量有 ``MOTOR_1`` 、``MOTOR_2`` 。 ``speed`` 参数为速度,范围-100~100,正值表示正转,负值时表示负转。
当某些时候你需要知道当前设置的速度值,你可以用 ``get_speed(motor_no)`` 返回当前电机速度。


音频播放
-------

拓展板内置扬声器,支持MP3格式为音频播放。可以播放掌控板文件系统的MP3音频,或者网络的MP3音频资源。


播放本地音频
+++++++

.. Attention:: 

    播放本地mp3音频由于受micropython文件系统限制和RAM大小限制,当文件大于1M基本很难下载下去。所以对音频文件的大小有所限制,应尽可能的小。

首先,将 :download:`音频素材</../examples/extboad_audio.rar>` 上传至掌控板的文件系统。


首先导入audio模块::

    import audio


播放本地mp3音频::

    import audio                            # 导入audio对象

    audio.play("music_1.mp3")               # 播放"music_1.mp3"音频

.. Hint:: 

    可在以下网站获取自己需要的音频。注意，最终上传至文件系统上的音频还需要压缩下，减低文件大小！

    * 音效素材：http://www.aigei.com/sound/
    * 音频压缩：https://online-audio-converter.com/cn/


播放本网络音频
++++++++++++

要播放网络上mp3音频文件，需要知道音频的URL地址。目前，大部分的音乐网受版权保护，并不直接提供音乐的URL，你可以通过一些插件爬取音频的URL地址。

播放网络MP3音频::

    import audio                                    # 导入audio
    from mpython import wifi                        # 导入wifi

    mywifi=wifi()                                   # 实例wifi类
    mywifi.connectWiFi('ssid','password')           # 连接 WiFi 网络
    
    audio.player_init()                                   # 播放初始化
    audio.play("http://wiki.labplus.cn/images/4/4e/Music_test.mp3")          # 播放网络音频url

.. Note:: 

    掌控板需要确保连接网络通畅。URL必须是完整的网络地址，否则无法解析。

音频解码功能使用到 ``audio`` 模块的 ``audio.play(url)`` 函数, ``url`` 参数可以为音源的本地文件系统的路径或网络URL地址。有关 ``audio`` 模块更详细使用,请查阅
:ref:`audio章节<audio>` 。

语音合成(TTS)
------------

TTS是Text To Speech的缩写，即“从文本到语音”，是人机对话的一部分，将文本转化问文字，让机器能够说话。

准备
+++++

掌控拓展板的在线语音合成功能是使用 `讯飞在线语音合成API <https://www.xfyun.cn/services/online_tts>`_  ，用户在使用该功能前，需要在讯飞开放平台注册并做相应的配置。

- 步骤1.在讯飞 https://www.xfyun.cn 注册账号。

.. image:: /images/extboard/xfyun_1.png
    :scale: 80 %


- 步骤2.创建新应用，应用平台选择"WebAPI"

.. image:: /images/extboard/xfyun_2.gif


- 步骤3.添加"在线语音合成"服务，且在程序中传入APPID、APIKey实例 ``TTS`` ，获取自己的公网IP(http://www.ip138.com)并添加到IP白名单。

.. image:: /images/extboard/xfyun_3.gif


文字转语音
++++++++

.. Attention:: TTS功能依赖网络，使用是注意先连接网络并保持网络通畅！

::

    from mpython import *                                       # 导入mpython模块
    import audio                                                # 导入audio模块
    import ntptime                                              # 导入授时模块

    my_wifi=wifi()                                              # 实例wifi
    my_wifi.connectWiFi('','')                                  # 连接 WiFi 网络

    APPID = ""                                                  # 讯飞应用ID
    API_KEY = ""                                                # 讯飞应用的api key

    while True:                                                 # 授时,并校准RTC
        try:
            ntptime.settime()
        except OSError :
            pass
        else:
            break


    # 沁园春·长沙 诗词
    poem=   "独立寒秋，湘江北去，橘子洲头。  \
            看万山红遍，层林尽染；漫江碧透，百舸争流。\
            鹰击长空，鱼翔浅底，万类霜天竞自由。\
            怅寥廓，问苍茫大地，谁主沉浮？\
            携来百侣曾游。忆往昔峥嵘岁月稠。\
            恰同学少年，风华正茂；书生意气，挥斥方遒。\
            指点江山，激扬文字，粪土当年万户侯。\
            曾记否，到中流击水，浪遏飞舟？" 


    audio.player_init()                                   # 播放初始化

    audio.xunfei_tts_config(API_KEY ,APPID)               # 讯飞配置
    audio.xunfei_tts(poem)                                # TTS转换


首先使用 ``ntptime.settime()`` 校准RTC时钟。然后 ``player_init()`` 初始化。用 ``xunfei_tts_config(api_key, appid )`` , ``appid`` , ``api_key`` 为必选参数,在讯飞平台的应用的APPID、API_KET 。然后使用 ``xunfei_tts(text)``
将文本转为语音并播放。



TTS支持中英文的文本转换。你可以将你想要说话的内容，通过文本的形式转化为语音。这样你就可以给你掌控板添上“人嘴”，模拟人机对话场景。
