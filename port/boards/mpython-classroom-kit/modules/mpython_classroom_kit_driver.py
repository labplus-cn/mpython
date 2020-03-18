# labplus mPython-box library
# MIT license; Copyright (c) 2018 labplus

# mpython-box buildin periphers drivers

# history:
# V1.0 zhaohuijiang

from machine import Pin, UART
import time
import ujson
from time import sleep_ms, sleep_us, sleep

# touchpad


class BS8112A(object):
   """  """

   def __init__(self, i2c):
      self.addr = 80
      # config
      self._i2c = i2c
      self.config = [0xB0, 0x00, 0x00, 0x83, 0xf3, 0x98, 0x0f, 0x0f,
                     0x0f, 0x0f, 0x0f, 0x0f, 0x0f, 0x0f, 0x0f, 0x0f, 0x0f, 0x0f, 0x00]
      checksum = 0
      for i in range(1, 19):
         checksum += self.config[i]
      checksum &= 0xff
      self.config[18] = checksum
      # print(self.config[18])
      retry = 0
      if (retry < 5):
         try:
            self._i2c.writeto(self.addr, bytearray(self.config), True)
            return
         except:
               retry = retry + 1
      else:
         raise Exception("bs8112a i2c read/write error!")

       # i2c.writeto(self.addr, b'\xB0', False)
       # time.sleep_ms(10)
       # print(i2c.readfrom(self.addr, 17, True))

   # key map:
   # value       bit7 bit6 bit5 bit4 bit3 bit2 bit1 bit0
   # bs8112a key Key8 Key7 Key6 Key5 Key4 Key3 Key2 Key1
   # mpython key       N    O    H    T    Y    P
   def key_value(self):
      retry = 0
      if (retry < 5):
         try:
            self._i2c.writeto(self.addr, b'\x08', False)
            time.sleep_ms(10)
            value = self._i2c.readfrom(self.addr, 1, True)
            time.sleep_ms(10)
            return value
         except:
               retry = retry + 1
      else:
         raise Exception("bs8112a i2c read/write error!")


class Codec_mode():
   ES_MODULE_ADC_DAC = 0x00
   ES_MODULE_DAC = 0x01
   ES_MODULE_ADC = 0x02


class Es8388():
   """  """

   def __init__(self, i2c, adc_volume=0, dac_volume=0, volume=65):
      self._i2c = i2c
      self.addr = 16
      self.adc_volume = adc_volume
      self.dac_volume = dac_volume
      self.volume = volume
      self.set_voice_mute(1)
      retry = 0
      if (retry < 5):
         try:
            # i2c.writeto(self.addr, bytearray([0x19, 0x04])) # ES8388_DACCONTROL3 0x04 mute/0x00 unmute&ramp;DAC unmute and  disabled digital volume control soft ramp
            #  Chip Control and Power Management
            self._i2c.writeto(self.addr, bytearray(
                [0x01, 0x50]))  # ES8388_CONTROL2 0x40?
            # ES8388_CHIPPOWER normal all and power up all
            self._i2c.writeto(self.addr, bytearray([0x02, 0x00]))
            # ES8388_MASTERMODE CODEC IN I2S SLAVE MODE 0x00: slave
            self._i2c.writeto(self.addr, bytearray([0x08, 0x00]))
            # dac setup
            # ES8388_DACPOWER . disable DAC and disable Lout/Rout/1/2
            self._i2c.writeto(self.addr, bytearray([0x04, 0xC0]))
            # ES8388_CONTROL1. Enfr=0,Play&Record Mode,(0x17-both of mic&paly)
            self._i2c.writeto(self.addr, bytearray([0x00, 0x12]))
            # ES8388_DACCONTROL1 1a 0x18:16bit iis , 0x00:24
            self._i2c.writeto(self.addr, bytearray([0x17, 0x18]))
            # ES8388_DACCONTROL2 DACFsMode,SINGLE SPEED; DACFsRatio,256
            self._i2c.writeto(self.addr, bytearray([0x18, 0x02]))
            # ES8388_DACCONTROL16 0x00 audio on LIN1&RIN1,  0x09 LIN2&RIN2
            self._i2c.writeto(self.addr, bytearray([0x26, 0x00]))
            # ES8388_DACCONTROL17 only left DAC to left mixer enable 0db
            self._i2c.writeto(self.addr, bytearray([0x27, 0x90]))
            # ES8388_DACCONTROL20 only right DAC to right mixer enable 0db
            self._i2c.writeto(self.addr, bytearray([0x2a, 0x90]))
            # ES8388_DACCONTROL21 set internal ADC and DAC use the same LRCK clock, ADC LRCK as internal LRCK
            self._i2c.writeto(self.addr, bytearray([0x2b, 0x80]))
            # ES8388_DACCONTROL23 vroi=0
            self._i2c.writeto(self.addr, bytearray([0x2d, 0x00]))
            self.set_adc_dac_volume(
                Codec_mode.ES_MODULE_DAC, self.dac_volume, 0)  # 0db
            # ES8388_DACPOWER 0x3c Enable DAC and Enable Lout/Rout/1/2
            self._i2c.writeto(self.addr, bytearray([0x04, 0x3c]))
            # adc setup
            self._i2c.writeto(self.addr, bytearray(
                [0x03, 0xff]))  # ES8388_ADCPOWER
            # ES8388_ADCCONTROL1 MIC Left and Right channel PGA gain
            self._i2c.writeto(self.addr, bytearray([0x09, 0xbb]))
            # ES8388_ADCCONTROL2 0x00 LINSEL & RINSEL, LIN1/RIN1 as ADC Input; DSSEL,use one DS Reg11; DSR, LINPUT1-RINPUT1
            self._i2c.writeto(self.addr, bytearray([0x0a, 0x00]))
            # ES8388_ADCCONTROL3 clock input
            self._i2c.writeto(self.addr, bytearray([0x0b, 0x02]))
            # ES8388_ADCCONTROL4 Left/Right data, Left/Right justified mode, Bits length 16bit, I2S format 0x0c?
            self._i2c.writeto(self.addr, bytearray([0x0c, 0x0c]))
            # ES8388_ADCCONTROL5 ADCFsMode,singel SPEED,RATIO=256
            self._i2c.writeto(self.addr, bytearray([0x0d, 0x02]))
            # ALC for Microphone
            self.set_adc_dac_volume(
                Codec_mode.ES_MODULE_ADC, self.adc_volume, 0)  # 0db
            # ES8388_ADCPOWER Power on ADC, Enable LIN&RIN, Power off MICBIAS, set int1lp to low power mode
            self._i2c.writeto(self.addr, bytearray([0x03, 0x09]))
            # set volume
            self.set_volume(self.volume)
            self.set_voice_mute(0)
            # test
            # for i in range(0, 52):
            #     i2c.writeto(self.addr, bytearray([i]))
            #     print("%d: %d" % (i, i2c.readfrom(self.addr, 1)[0]))
            return
         except:
               retry = retry + 1
      else:
         raise Exception("es8388 i2c read/write error!")

   def deinit(self):
      retry = 0
      if (retry < 5):
         try:
            # ES8388_CHIPPOWER reset and stop es838
            self._i2c.writeto(self.addr, bytearray([0x02, 0xff]))
            return
         except:
               retry = retry + 1
      else:
         raise Exception("bs8112a i2c read/write error!")

   def set_adc_dac_volume(self, mode, volume, dot):
      _volume = volume
      if (_volume < -96):
         _volume = -96
      else:
         _volume = 0
      _dot = 0
      if dot >= 5:
         _dot = 1

      _volume = (-_volume << 1) + _dot
      retry = 0
      if (retry < 5):
         try:
            if (mode == Codec_mode.ES_MODULE_ADC or mode == Codec_mode.ES_MODULE_ADC_DAC):
               self._i2c.writeto(self.addr, bytearray(
                   [0x10, _volume]))  # ES8388_ADCCONTROL8
               self._i2c.writeto(self.addr, bytearray(
                   [0x11, _volume]))  # ES8388_ADCCONTROL9
            if (mode == Codec_mode.ES_MODULE_DAC or mode == Codec_mode.ES_MODULE_ADC_DAC):
               self._i2c.writeto(self.addr, bytearray(
                   [0x1b, _volume]))  # ES8388_DACCONTROL5
               self._i2c.writeto(self.addr, bytearray(
                   [0x1a, _volume]))  # ES8388_DACCONTROL4
            return
         except:
               retry = retry + 1
      else:
         raise Exception("bs8112a i2c read/write error!")

   def set_volume(self, volume):
      self.volume = volume
      if (self.volume < 0):
         self.volume = 0
      elif (self.volume > 100):
         self.volume = 100

      retry = 0
      if (retry < 5):
         try:
            self._i2c.writeto(self.addr, bytearray(
                [0x2e, self.volume//3]))  # ES8388_DACCONTROL24
            self._i2c.writeto(self.addr, bytearray(
                [0x2f, self.volume//3]))  # ES8388_DACCONTROL25
            self._i2c.writeto(self.addr, bytearray(
                [0x30, 0]))  # ES8388_DACCONTROL26
            self._i2c.writeto(self.addr, bytearray(
                [0x31, 0]))  # ES8388_DACCONTROL27
            # print("volume L: %d" % (self.volume//3))
            return
         except:
               retry = retry + 1
      else:
         raise Exception("bs8112a i2c read/write error!")

   def get_volume(self):
         return self.volume

   def set_voice_mute(self, mute):
      retry = 0
      if (retry < 5):
         try:
            self._i2c.writeto(self.addr, b'\x19')
            dac_ctr3 = self._i2c.readfrom(self.addr, 1)[0]
            if(mute):
               dac_ctr3 |= 0x04
            else:
               dac_ctr3 &= 0xFB
            self._i2c.writeto(self.addr, bytearray([0x19, dac_ctr3]))
         except:
               retry = retry + 1
      else:
         raise Exception("bs8112a i2c read/write error!")


uart2 = UART(2, baudrate=1152000, rx=Pin.P8, tx=Pin.P23,
             timeout=50, timeout_char=1024, rxbuf=2048, txbuf=2048)


class K210Error(Exception):
   """K210异常类"""
   pass

class blob():
   
   def __init__(self,*args):
      self.dict = args[0]

   def __repr__(self):
      return  self.dict

   def x(self):
      return self.dict['x']

   def y(self):
      return self.dict['y']

   def w(self):
      return self.dict['w']

   def h(self):
      return self.dict['h']

   def rect(self):
      return(self.dict['x'], self.dict['y'], self.dict['w'], self.dict['h'])

   def pixels(self):
      return self.dict['pixels']

   def cx(self):
      return self.dict['cx']

   def cy(self):
      return self.dict['cy']
      
   def rotation(self):
      return self.dict['rotation']

   def code(self):
      return self.dict['code']

   def count(self):
      return self.dict['count']

class K210():
   def __init__(self):
        t1 = time.ticks_ms()
        while (time.ticks_diff(time.ticks_ms(), t1) < 10000):
            rsp = self.send_cmd({'GET_KEYS': 0})  # 通过发获取按键指令测试K210是否初始化成功
            if  rsp is not None: 
               return
        raise K210Error("K210 init failed!")

   def send_cmd(self, command, wait=True, timeout=200):
      json_stream = ujson.dumps(command)
      uart2.write(json_stream + '\n')
      # print("UART_Send:%s" % (json_stream + '\n'))
      t1 = time.ticks_ms()
      while wait:
         if uart2.any() > 0:
               r=None
               r = uart2.readline()
               r= r.strip()
               while uart2.readline():
                  pass
               # print("UART_Recv:%s" % r)
               try:
                  rsp = ujson.loads(r)
               except Exception as e:
                  print(e)
                  break
               else:
                  if rsp and isinstance(rsp, dict):
                     for key, value in rsp.items():
                        if key == 'ERROR':
                           raise K210Error(value)
                        if key == 'RESP':
                           return value
         if time.ticks_diff(time.ticks_ms(), t1) > timeout:
            # raise K210Error("k210 not respone!")
            return None

   def get_key(self):
      return self.send_cmd({'GET_KEYS': 0})

   def get_distance(self):
      resp =  self.send_cmd({'GET_DISTANCE': 0})
      if resp is None:
         resp = 340
      return resp

   def set_motor(self, speed):
      return self.send_cmd({'SET_MOTOR': speed})

   def file_open(self, *args):
      return self.send_cmd({'FILE_OPEN': args})

   def file_read(self, *args):
      return self.send_cmd({'FILE_READ': args[0]},timeout=300)

   def file_write(self, *args):
      return self.send_cmd({'FILE_WRITE': args[0]},timeout=300)

   def file_close(self):
      return self.send_cmd({'FILE_CLOSE': 0})

   def reset(self):
      self.send_cmd({'RESET': 0},False)

   def select_model(self, *args):
      self.send_cmd({'SELE_MOD': args[0]}, timeout=3000)

   def load_model(self, **kws):
      self.send_cmd({'LOD_MOD': kws}, timeout=3000)

   def detect_yolo(self):
      return self.send_cmd({'DET_YO': 0})
   def predict_net(self):
      return self.send_cmd({'PRE_NET': 0})


   def deinit_yolo(self):
      return self.send_cmd({'DINT_YO': 0})

   def deinit_net(self):
      return self.send_cmd({'DINT_NET': 0})

   def camera_snapshot(self):
      return self.send_cmd({'SNAPSHOT': 0})

   def camera_reset(self):
      return self.send_cmd({'CAM_RST': 0},timeout=3000)

   def camera_run(self, *arg):
      return self.send_cmd({'CAM_RUN': arg[0]})

   def camera_set_pixformat(self, *arg):
      return self.send_cmd({'CAM_SET_PF': arg[0]})

   def camera_set_contrast(self, *arg):
      return self.send_cmd({'CAM_SET_CRA': arg[0]})

   def camera_set_brightness(self, *arg):
      return self.send_cmd({'CAM_SET_BRG': arg[0]})

   def camera_set_saturation(self, *arg):
      return self.send_cmd({'CAM_SET_SAT': arg[0]})

   def camera_set_auto_gain(self, *arg, **kw):
      return self.send_cmd({'CAM_AUTO_GAIN': [arg, kw]})

   def camera_set_auto_whitebal(self, *arg):
      return self.send_cmd({'CAM_AUTO_WBAL': arg[0]})

   def camera_set_windowing(self, *arg):
      return self.send_cmd({'CAM_SET_WIN': arg[0]})

   def camera_set_hmirror(self, *arg):
      return self.send_cmd({'CAM_SET_HM': arg[0]})

   def camera_set_vflip(self, *arg):
      return self.send_cmd({'CAM_SET_VF': arg[0]})

   def camera_skip_frames(self, *arg, **kw):
      return self.send_cmd({'CAM_SKIP_FRM': [arg, kw]})

   def lcd_init(self, *args, **kws):
      return self.send_cmd({'LCD_INT': [args, kws]},timeout=5000)

   def lcd_display(self, **kws):
      return self.send_cmd({'LCD_DISP': kws})

   def lcd_clear(self, **kws):
      return self.send_cmd({'LCD_CLR': kws})

   def lcd_draw_string(self, *args):
      return self.send_cmd({'LCD_STR': args})

   def image_load(self, *args, **kws):
      self.send_cmd({'IMG_LOD': [args, kws]})
      time.sleep_ms(200)

   def image_width(self):
      return self.send_cmd({'IMG_WID': 0})

   def image_hight(self):
      return self.send_cmd({'IMG_HIG': 0})


   def image_format(self):
      return self.send_cmd({'IMG_FRM': 0})

   def image_size(self):
      return self.send_cmd({'IMG_SIZE': 0})

   def image_get_pixel(self, *args, **kws):
      return self.send_cmd({'IMG_GET_PIX': [args, kws]})

   def image_set_pixel(self, *args, **kws):
      self.send_cmd({'IMG_SET_PIX': [args, kws]})

   def image_mean_pool(self, *args, **kws):
      self.send_cmd({'IMG_MEAN_P': [args, kws]})

   def image_to_grayscale(self):
      self.send_cmd({'IMG_TO_GRAY': 0})

   def image_to_rainbow(self):
      self.send_cmd({'IMG_TO_RB': 0})

   def image_copy(self, *args, **kws):
      self.send_cmd({'IMG_CPY': [args, kws]})

   def image_save(self, *args, **kws):
      self.send_cmd({'IMG_SAVE': [args, kws]})
      time.sleep_ms(200)

   def image_clear(self):
      self.send_cmd({'IMG_CLR': 0})

   def image_draw_line(self, *args, **kws):
      self.send_cmd({'IMG_DRW_LN': [args, kws]})

   def image_draw_rectangle(self, *args, **kws):
      self.send_cmd({'IMG_DRW_RECTANG': [args, kws]})

   def image_draw_circle(self, *args, **kws):
      self.send_cmd({'IMG_DRW_CIR': [args, kws]})

   def image_draw_string(self, *args, **kws):
      self.send_cmd({'IMG_DRW_STR': [args, kws]})

   def image_draw_cross(self, *args, **kws):
      self.send_cmd({'IMG_DRW_CRS': [args, kws]})

   def image_draw_arrow(self, *args, **kws):
      self.send_cmd({'IMG_DRW_ARR': [args, kws]})

   def image_draw_image(self, *args, **kws):
      self.send_cmd({'IMG_DRW_IMG': [args, kws]})

   def image_binary(self, *args, **kws):
      self.send_cmd({'IMG_BINARY': [args, kws]})

   def image_invert(self):
      self.send_cmd({'IMG_INVERT': 0})

   def image_erode(self, *args, **kws):
      self.send_cmd({'IMG_ERODE': [args, kws]})
      
   def image_dilate(self, *args, **kws):
      self.send_cmd({'IMG_DIL': [args, kws]})

   def image_negate(self, *args, **kws):
      self.send_cmd({'IMG_NEG': [args, kws]})

   def image_mean(self, *args, **kws):
      self.send_cmd({'IMG_MEAN': [args, kws]})

   def image_mode(self, *args, **kws):
      self.send_cmd({'IMG_MODE': [args, kws]})

   def image_median(self, *args, **kws):
      self.send_cmd({'IMG_MEDIAN': [args, kws]})

   def image_midpoint(self, *args, **kws):
      self.send_cmd({'IMG_MIDP': [args, kws]})

   def image_cartoon(self, *args, **kws):
      self.send_cmd({'IMG_CART': [args, kws]})

   def image_conv3(self, *args, **kws):
      self.send_cmd({'IMG_CONV': [args, kws]})

   def image_gaussian(self, *args, **kws):
      self.send_cmd({'IMG_GAUS': [args, kws]})

   def image_bilateral(self, *args, **kws):
      self.send_cmd({'IMG_BIL': [args, kws]})

   def image_linpolar(self, *args, **kws):
      self.send_cmd({'IMG_LINP': [args, kws]})

   def image_logpolar(self, *args, **kws):
      self.send_cmd({'IMG_LOGP': [args, kws]})

   def image_rotation_corr(self, *args, **kws):
      self.send_cmd({'IMG_ROT_COR': [args, kws]})

   def image_find_blobs(self, *args, **kws):
      return [blob(i) for i in self.send_cmd({'IMG_FID_BLOB': [args, kws]})]
