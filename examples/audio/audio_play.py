import audio                                    # 导入audio
from mpython import wifi                        # 导入wifi

mywifi=wifi()                                   # 实例wifi类
mywifi.connectWiFi('ssid','password')           # 连接 WiFi 网络

audio.player_init()                                   # 播放初始化
audio.play('music.mp3')                                      # 本地音频解码                   
audio.play("http://wiki.labplus.cn/images/4/4e/Music_test.mp3")          # 播放网络音频url
audio.player_deinit()                            # 播放结束,释放资源