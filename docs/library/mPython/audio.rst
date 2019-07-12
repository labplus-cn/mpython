.. _audio:

.. module:: audio
   :synopsis: 提供音频播放录音的相关功能

:mod:`audio` --- 提供音频播放录音的相关功能
==========

该模块提供音频录音播放功能,使用P8和P9引脚作为音频解码输出。


函数
----------

基础音频函数
++++++++++++

播放
~~~~~~~~~

.. py:method:: audio.player_init()

音频播放初始化,为音频解码开辟缓存

.. py:method:: audio.play(url)

本地或网络音频播放,目前只支持mp3格式音频。

可以播放文件系统的MP3音频,或者网络的MP3音频资源。播放本地mp3音频由于受micropython文件系统限制和RAM大小限制,当文件大于1M基本很难下载下去。所以对音频文件的大小有所限制,应尽可能的小。
当播放网络MP3音频,须先连接网络,URL必须是完整地址,如"http://wiki.labplus.cn/images/4/4e/Music_test.mp3" 。返回解码状态,当为0,说明可接受音频解码指令;当为1,说明当前正处解码状态,不能响应。


    - ``url`` (str): 音频文件路径,类型为字符串。可以是本地路径地址,也可以是网络上的URL地址。 

.. literalinclude:: /../examples/audio/audio_play.py
    :caption: 播放MP3音频
    :linenos:


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


录音
~~~~~~~~~

.. py:method:: audio.recorder_init()

录音初始化

.. py:method:: audio.record(file_name, record_time = 5)

录制音频,并以 `wav` 格式存储。

- ``file_name`` - wav文件存储路径
- ``record_time`` - 录音时长,默认5秒。录音时长受文件系统空间限制,最大时长依实际情况而定。

.. py:method:: audio.recorder_deinit()

录音结束后释放资源

示例-录音::

    import audio

    audio.recorder_init()
    rgb[0] = (255, 0, 0)  # 用LED指示录音开始结束 
    rgb.write()
    audio.xunfei_iat_record('test.wav',5)
    rgb[0] = (0, 0, 0)  
    rgb.write()
    audio.recorder_deinit()

----------------------------------------------

.. _tts:

语音合成(TTS)
+++++++++++++

基于讯飞TTS语音合成API的文字转语音功能,将文字信息转化为声音信息，给掌控板配上“嘴巴”。其合成音在音色、自然度等方面的表现均接近甚至超过了人声。目前应用于掌控拓展板。



.. py:method:: audio.xunfei_tts_config( api_key,app_id, voice_name="aisxping")

| 讯飞tts配置,使用前须要用 ``audio.player_init()`` 播放初始化。 由于该功能依赖讯飞API,在使用前需要先将掌控板连接至互联网,并设置RTC时钟至准确时间。
| 讯飞文字转语音功能,使用该功能前需要在讯飞开发平台 https://www.xfyun.cn/ 注册账号,步骤如下：
|     
| 1. 注册账号
| 2. 在产品中,选择“在线语音合成”服务。
| 3. 在IP白名单中添加网络的公网IP。

    - ``api_key`` (str): 讯飞应用的APIKey
    - ``app_id`` (str): 讯飞应用的APPID
    - ``voice_name`` (str): 发音人,默认"aisxping";可选有"xiaoyan","aisjiuxu","aisjinger","aisbabyxu"
    


.. py:method:: audio.xunfei_tts(text)

 文字转语音

    - ``text`` (str): 转换的文本,支持中英文。

.. literalinclude:: /../examples/audio/tts.py
    :caption: TTS文字转语音示例
    :linenos:


语音听写(IAT)
+++++++++++

基于 `讯飞TTS语音听写 <https://www.xfyun.cn/services/voicedictation>`_ ,将语音(≤60秒)转换成对应的文字信息，让机器能够“听懂”人类语言，相当于给机器安装上“耳朵”，使其具备“能听”的功能。


.. py:method:: audio.xunfei_iat_config(api_key, app_id)

| 讯飞iat配置,使用前须要用 ``audio.recorder_init()`` 录音初始化。由于该功能依赖讯飞API,在使用前需要先将掌控板连接至互联网,并设置RTC时钟至准确时间。
| 讯飞语音听写功能,使用该功能前需要在讯飞开发平台 https://www.xfyun.cn/ 注册账号,步骤如下：
|     
| 1. 注册账号(已有账号,略过)
| 2. 在产品中,选择“语音听写”服务。
| 3. 在IP白名单中添加网络的公网IP。

    - ``api_key`` (str): 讯飞应用的APIKey
    - ``app_id`` (str): 讯飞应用的APPID
   
.. py:method:: audio.xunfei_iat_record()

IAT录音,如要设置录音时长,带参数传入,单位为秒。不带参数默认为录音5秒。该函数为阻塞型,当录音结束后才释放,执行后续的命令。

.. py:method:: audio.xunfei_iat()

将iat录音传至讯飞平台处理,处理结束后,将返回语音转文字的json内容。


