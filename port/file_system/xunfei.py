# -*- coding:utf-8 -*-
#
#   author: zhaohuijiang
#
#  错误码链接：https://www.xfyun.cn/document/error-code （code返回错误码时必看）
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
import hashlib
import ujson
import ussl
from machine import RTC
import ubinascii
import uhashlib
from urllib.parse import *
from uwebsockets.client import *
from mpython import *
import network
import time
import os

STATUS_FIRST_FRAME = 0  # 第一帧的标识
STATUS_CONTINUE_FRAME = 1  # 中间帧标识
STATUS_LAST_FRAME = 2  # 最后一帧的标识

MODE_IAT = 1
MODE_TTS = 2

def trans(s):
    return "b'%s'" % ''.join('\\x%.2x' % x for x in s)

def get_date():
    week_tup = ('Mon,', 'Tues,', 'Wed,', 'Thur,','Fri,', 'Sat,','Sun,')
    month_tup = ('', 'Jan', 'Feb', 'Mar', 'Apr','May', 'Jun','Jul', 'Aug', 'Sept', 'Oct','Nov', 'Dec')
    rtc = RTC()
    date_tuple = rtc.datetime()
    date = week_tup[date_tuple[3]] + " " + "%02d"%(date_tuple[2]) + " " + str(month_tup[date_tuple[1]]) + " " + "%02d"%(date_tuple[0]) + " " + \
           "%02d"%(date_tuple[4]) + ":" + "%02d"%(date_tuple[5]) + ":" + "%02d"%(date_tuple[6]) + " GMT"
    # print(date)
    return date

def hmac_sha256(msg, key):
    trans_5C = bytes((x ^ 0x5C) for x in range(256))
    trans_36 = bytes((x ^ 0x36) for x in range(256))
    _k_ipad = [54]*64
    _k_opad = [92]*64
    _msg = msg.encode()
    for i in range(len(key)): 
        _k_ipad[i] = trans_36[ord(key[i])]
        _k_opad[i] = trans_5C[ord(key[i])]
    k_ipad = bytes(_k_ipad)
    k_opad = bytes(_k_opad)
    uhash = uhashlib.sha256()
    uhash.update(k_ipad)
    uhash.update(_msg)
    m = uhash.digest()
    # print(trans(m))
    uhash1 = uhashlib.sha256()
    uhash1.update(k_opad)
    uhash1.update(m)
    # m1 = ubinascii.hexlify(uhash1.digest())
    # print(m1)
    m1 = uhash1.digest()
    # print(trans(m1))
    return m1

class Ws_Param(object):
    # 初始化
    def __init__(self, APPID, APIKey, APISecret, mode, AudioFile='', Text=''):
        self.APPID = APPID
        self.APIKey = APIKey
        self.APISecret = APISecret
        self.AudioFile = AudioFile
        self.Text = Text
        self.mode = mode 

        # 公共参数(common)
        self.CommonArgs = {"app_id": self.APPID}
        # 业务参数(business)，更多个性化参数可在官网查看
        if self.mode == MODE_IAT:
            self.BusinessArgs = {"domain": "iat", "language": "zh_cn", "accent": "mandarin", "vinfo":1,"vad_eos":10000, "nbest":1}
        elif self.mode == MODE_TTS:
            self.BusinessArgs = {"aue": "raw", "auf": "audio/L16;rate=16000", "vcn": "xiaoyan", "tte": "utf8"}
            self.Data = {"status": 2, "text": ubinascii.b2a_base64(self.Text).decode().strip()}
        # print(ubinascii.b2a_base64(self.Text).decode().strip())            

    # 生成url
    def create_url(self):
        if self.mode == MODE_IAT:
            url = 'wss://ws-api.xfyun.cn/v2/iat'
        elif self.mode == MODE_TTS:
            url = 'wss://tts-api.xfyun.cn/v2/tts'
            files = os.listdir()
            if self.AudioFile in files:
                os.remove(self.AudioFile)
        # 生成RFC1123格式的时间戳 
        date = get_date()

        # 拼接字符串
        signature_origin = "host: " + "ws-api.xfyun.cn" + "\n"
        signature_origin += "date: " + date + "\n"  # date: Tue, 15 Oct 2019 07:00:50 GMT 
        # signature_origin += "date: " + "Tue, 15 Oct 2019 07:00:50 GMT" + "\n"   
        if self.mode == MODE_IAT:
            signature_origin += "GET " + "/v2/iat " + "HTTP/1.1"
        elif self.mode == MODE_TTS:
            signature_origin += "GET " + "/v2/tts " + "HTTP/1.1"
        # 进行hmac-sha256进行加密
        signature_sha = hmac_sha256(signature_origin, self.APISecret)
        signature_sha = ubinascii.b2a_base64(signature_sha).decode().strip()
        # print(signature_sha)

        authorization_origin = "api_key=\"%s\", algorithm=\"%s\", headers=\"%s\", signature=\"%s\"" % ( \
            self.APIKey, "hmac-sha256", "host date request-line", signature_sha)
        authorization = ubinascii.b2a_base64(authorization_origin.encode()).decode().strip()
        # print(authorization)

        # 将请求的鉴权参数组合为字典
        v = {
            "authorization": authorization,
            "date": date,
            "host": "ws-api.xfyun.cn"
        }
        # print(urlencode(v))
        # 拼接鉴权参数，生成url
        # url = url + '?' + urlencode(v)
        # print("date: ",date)
        # print("v: ",v)
        # 此处打印出建立连接时候的url
        # print('websocket url :', url)
        if self.mode == MODE_IAT:
            path = "/v2/iat?" + urlencode(v)
        elif self.mode == MODE_TTS:
            path = "/v2/tts?" + urlencode(v)
        return url,path

class Xunfei_speech(Ws_Param):
    # 音频数据发送
    def send_audio(self, ws):
        frameSize = 4000  # 每一帧的音频大小
        intervel = 0.1  # 发送音频间隔(单位:s)
        status = STATUS_FIRST_FRAME  # 音频的状态信息，标识音频是第一帧，还是中间帧、最后一帧

        with open(self.AudioFile, "rb") as fp:
            while True:
                buf = fp.read(frameSize)
                # 文件结束
                if not buf:
                    status = STATUS_LAST_FRAME
                # 第一帧处理
                # 发送第一帧音频，带business 参数
                # appid 必须带上，只需第一帧发送
                if status == STATUS_FIRST_FRAME:

                    d = {"common": self.CommonArgs,
                            "business": self.BusinessArgs,
                            "data": {"status": 0, "format": "audio/L16;rate=8000", 
                                    "audio": ubinascii.b2a_base64(buf).decode().strip(), 
                                    "encoding": "raw"}}
                    d = ujson.dumps(d)
                    ws.send(d)
                    status = STATUS_CONTINUE_FRAME
                # 中间帧处理
                elif status == STATUS_CONTINUE_FRAME:
                    d = {"data": {"status": 1, "format": "audio/L16;rate=8000",
                                    "audio": ubinascii.b2a_base64(buf).decode().strip(),
                                    "encoding": "raw"}}
                    ws.send(ujson.dumps(d))
                # 最后一帧处理
                elif status == STATUS_LAST_FRAME:
                    d = {"data": {"status": 2, "format": "audio/L16;rate=8000",
                                    "audio": ubinascii.b2a_base64(buf).decode().strip(),
                                    "encoding": "raw"}}
                    ws.send(ujson.dumps(d))
                    time.sleep(1)
                    break
                # 模拟音频采样间隔
                time.sleep(intervel)
            # ws.close()

    # 语音识别
    def iat(self):
        wsUrl,uri_path = self.create_url()
        # print(wsUrl)
        # print(uri_path)
        websocket = connect(wsUrl, uri_path)

        self.send_audio(websocket)
        message = websocket.recv()
        # print(message)
        result = ""
        try:
            code = ujson.loads(message)["code"]
            sid = ujson.loads(message)["sid"]
            if code != 0:
                errMsg = ujson.loads(message)["message"]
                # print("sid:%s call error:%s code is:%s" % (sid, errMsg, code))

            else:
                data = ujson.loads(message)["data"]["result"]["ws"]
                # print(ujson.loads(message))
                for i in data:
                    for w in i["cw"]:
                        result += w["w"]
                # print(result)
                # print("sid:%s call success!,data is:%s" % (sid, ujson.dumps(data, ensure_ascii=False)))
        except Exception as e:
            print("receive msg,but parse exception:", e)

        websocket.close()
        return result

    # 语音合成
    def tts(self):
        wsUrl,uri_path = self.create_url()
        # print(wsUrl)
        websocket = connect(wsUrl, uri_path, self.AudioFile)
        intervel = 2  # 等待结果间隔(单位:s)
        d = {"common": self.CommonArgs,
            "business": self.BusinessArgs,
            "data": self.Data,
            }
        d = ujson.dumps(d)
        websocket.send(d)
        # sleep等待服务端返回结果
        time.sleep(intervel)
        while True:
            message = websocket.recv()
            if message == None:
                break
        websocket.close()
