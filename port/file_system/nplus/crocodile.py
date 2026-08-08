from mpython import i2c, sleep_ms, MPythonPin, PinMode
from machine import UART,Pin
import math
import time

#MP3模块
class JQ6500_MP3(object):
    def __init__(self, uart2_rx0=18, uart2_tx0=19): 
        self.uart = UART(2, baudrate=9600, rx=uart2_rx0,tx=uart2_tx0,timeout=300)
        self.ai_read_data = []  
        
    def mp3_Uart_CMD(self,cmd,cmd_data=[]):   
        cmd_temp = [0x7E,cmd[0],cmd[1]]
        cmd_temp.extend(cmd_data)
        cmd_temp.append(0xEF)
        self.uart.write(bytes(cmd_temp))
        
    def MP3_WaitForARP(self,cmd,data=[]): 
        if self.uart.any():
            self.uart.read()
        self.mp3_Uart_CMD(cmd,data)
        wait_time = 0
        if cmd[1] > 0x40:
            while (not self.uart.any()):
                wait_time = wait_time+1
                time.sleep_ms(10)
                if wait_time>100:
                    print("UART_NO_ACK_ERR")
                    break
            else:
                return self.uart.read()   
        
    def print_x16(self,date):
        for i in range(len(date)):
            print('{:2x}'.format(date[i]),end=' ')
        print('')
        
    def sd_device_set(self):    
        self.mp3_Uart_CMD([3,9],[1])
    
    def music_file_select(self,folder=1,file=1):    
        self.mp3_Uart_CMD([4,18],[folder,file])
        
    def music_golbal_select(self,num=0):    
        self.mp3_Uart_CMD([4,3],[num>>8,num&0xFF])
        
    def music_next(self):    
        self.mp3_Uart_CMD([2,1])
        
    def music_prev(self):    
        self.mp3_Uart_CMD([2,2])
        
    def music_sound_vol(self,data):  
        self.mp3_Uart_CMD([3,6],[data])
        
    def music_eq_set(self,mode=0):    
        self.mp3_Uart_CMD([3,7],[mode])
    
    def music_play_mode(self,mode=0):    
        self.mp3_Uart_CMD([3,17],[mode])
        
    def music_play(self):    
        self.mp3_Uart_CMD([2,13])
        
    def music_pause(self):    
        self.mp3_Uart_CMD([2,14])
        
    def music_mode_change(self,mode):
        p16 = MPythonPin(16, PinMode.OUT)
        p16.write_digital(mode)
