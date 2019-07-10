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
poem =  "独立寒秋，湘江北去，橘子洲头。  \
        看万山红遍，层林尽染；漫江碧透，百舸争流。\
        鹰击长空，鱼翔浅底，万类霜天竞自由。\
        怅寥廓，问苍茫大地，谁主沉浮？\
        携来百侣曾游。忆往昔峥嵘岁月稠。\
        恰同学少年，风华正茂；书生意气，挥斥方遒。\
        指点江山，激扬文字，粪土当年万户侯。\
        曾记否，到中流击水，浪遏飞舟？" 


audio.player_init()                                   # 播放初始化

audio.xunfei_tts_config(API_KEY ,APPID)               # 讯飞配置
audio.xunfei_tts(poem)                                # TTS转换s