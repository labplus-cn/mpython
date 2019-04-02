.. _audio:
audio 模块
==========

该模块提供音频录音播放功能,使用P8和P9引脚作为音频解码输出。

.. Attention:: 目前只实现音频播放功能

函数
----------

基础音频函数
++++++++++++

.. py:method:: audio.player_init()

音频播放初始化,为音频解码开辟缓存

.. py:method:: audio.play(url)

本地或网络音频播放,目前只支持mp3格式音频。

可以播放文件系统的MP3音频,或者网络的MP3音频资源。播放本地mp3音频由于受micropython文件系统限制和RAM大小限制,当文件大于1M基本很难下载下去。所以对音频文件的大小有所限制,应尽可能的小。
当播放网络MP3音频,须先连接网络,URL必须是完整地址,如"http://wiki.labplus.cn/images/4/4e/Music_test.mp3" 。返回解码状态,当为0,说明可接受音频解码指令;当为1,说明当前正处解码状态,不能响应。


    - ``url`` (str): 音频文件路径,类型为字符串。可以是本地路径地址,也可以是网络上的URL地址。 

::


    from mpython import wifi                    # 导入wifi类
    import audio                                # 导入音频播放

    mywifi=wifi()                               # 实例wifi
    mywifi.connectWiFi('ssid','password')       # 连接wifi网络到互联网

    player_init()                               # 音频初始化

    play('music.mp3')                           # 本地音频解码
    play('http://wiki.labplus.cn/images/4/4e/Music_test.mp3')   # 网络音频解码

.. py:method:: audio.set_volume(vol)

设置音频音量

    - ``vol`` : 音量设置,范围0~100

.. py:method:: audio.stop()

音频播放停止

.. py:method:: audio.pause()

音频播放暂停

.. py:method:: audio.resume()

音频播放恢复,用于暂停后的重新播放


.. py:method:: audio.player_status()

用于获取系统是否处于音频播放状态,返回1,说明正处于播放中,返回0,说明播放结束,处于空闲。


.. py:method:: audio.player_deinit()

音频播放结束后,释放缓存

----------------------------------------------


.. _tts:

TTS
++++++++

基于讯飞TTS语音合成API的文字转语音功能,将文字信息转化为声音信息，给掌控板配上“嘴巴”。其合成音在音色、自然度等方面的表现均接近甚至超过了人声。目前应用于掌控拓展板。



.. py:method:: audio.xunfei_tts_config( api_key,appid, voice_name="aisxping")

| 讯飞tts配置。由于该功能依赖讯飞API,在使用前需要先将掌控板连接至互联网,并设置RTC时钟至准确时间。
| 讯飞文字转语音功能,使用该功能前需要在讯飞开发平台 https://www.xfyun.cn/ 注册账号,步骤如下：
|     
| 1. 注册账号
| 2. 新建产品,选择“在线语音合成”服务。
| 3. 在IP白名单中添加网络的公网IP。

    - ``api_key`` (str): 讯飞应用的APIKey
    - ``appid`` (str): 讯飞应用的APPID
    - ``voice_name`` (str): 发音人,默认"aisxping";可选有"xiaoyan","aisjiuxu","aisjinger","aisbabyxu"
    


.. py:method:: audio.xunfei_tts(text)

 文字转语音

    - ``text`` (str): 转换的文本,支持中英文。


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
