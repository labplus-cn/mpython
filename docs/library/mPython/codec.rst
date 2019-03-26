.. _codec:

codec 模块
==========

该模块提供音频编解码功能

.. Attention:: 目前只实现音频解码功能

函数
----------

.. py:method:: codec.audio_play(dir)

本地或网络音频解码,目前只支持mp3格式音频。

可以播放文件系统的MP3音频,或者网络的MP3音频资源。播放本地mp3音频由于受micropython文件系统限制和RAM大小限制,当文件大于1M基本很难下载下去。所以对音频文件的大小有所限制,应尽可能的小。
当播放网络MP3音频,须先连接网络,URL必须是完整地址,如"http://wiki.labplus.cn/images/4/4e/Music_test.mp3" 。返回解码状态,当为0,说明可接受音频解码指令;当为1,说明当前正处解码状态,不能响应。


    - ``dir`` (str): 音频文件路径,类型为字符串。可以是本地路径地址,也可以是网络上的URL地址。 

::


    from mpython import wifi            # 导入wifi类
    import codec                        # 导入音频解码

    mywifi=wifi()                       # 实例wifi
    mywifi.connectWiFi('ssid','password')        # 连接wifi网络到互联网


    codec.audio_play('music.mp3')           # 本地音频解码
    codec.audio_play('http://wiki.labplus.cn/images/4/4e/Music_test.mp3') # 网络音频解码

.. py:method:: codec.audio_volume(vol)

设置音频音量

    - ``vol`` : 音量设置,范围0~100

.. py:method:: codec.audio_stop()

音频解码停止

.. py:method:: codec.audio_pause()

音频解码暂停

.. py:method:: codec.audio_resume()

音频解码恢复,用于暂停后的重新播放


.. py:method:: codec.audio_status()

用于获取系统是否处于音频解码状态,返回0,说明正处于解码中,返回1,说明解码结束,处于空闲。
