
import time
from .public import *

class Maix_asr(object):
    """ maix语音识别类"""
    def __init__(self, uart):
        self.uart = uart
        self.ai_key_name = []
        self.result = None
        self.lock = False
        AI_Uart_CMD(self.uart, 0x01, AI['asr'][0], AI['asr'][1])
        time.sleep(0.5)

    def addKeyword(self,key_name,num):
        if len(self.ai_key_name) > num:
            self.ai_key_name[num] = key_name
        if len(self.ai_key_name) == num:
            self.ai_key_name.append(key_name)
        if len(self.ai_key_name) < num:
            while len(self.ai_key_name) < num:
                self.ai_key_name.append("pou-jian")
            self.ai_key_name.append(key_name)

    def start(self): #
        str_buf = ",".join(self.ai_key_name)
        # print(str_buf)
        # AI_Uart_CMD_String(self.uart, 0x02, AI['asr'][0], AI['asr'][2], '中文')
        AI_Uart_CMD_String(uart=self.uart, cmd=AI['asr'][0], cmd_type=AI['asr'][2], str_buf=str_buf)
        time.sleep_ms(50)
        print('开始语音识别...')

    def recognize(self):
        time.sleep_ms(30)
        if(not self.lock):
            AI_Uart_CMD(self.uart, 0x01, AI['asr'][0], AI['asr'][3])
        # try:
        #     self.result = self.AI_WaitForK210(0x01, AI['asr'][0], AI['asr'][3])
        # except:
        #     self.result = None

    def release(self):
        pass    
    
    def AI_WaitForK210(self, data_type, cmd, cmd_type, cmd_data=[0, 0, 0, 0, 0, 0]):
        if(not self.lock):            
            AI_Uart_CMD(self.uart, data_type, cmd, cmd_type, cmd_data)