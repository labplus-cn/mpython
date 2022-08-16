from mpython import i2c
# from InnovaBit import i2c
from time import sleep

# APDS9960 i2c地址
APDS9960_I2C_ADDR = 0x39

# APDS9960 手势参数
APDS9960_GESTURE_THRESHOLD_OUT = 10
APDS9960_GESTURE_SENSITIVITY_1 = 50
APDS9960_GESTURE_SENSITIVITY_2 = 20

# APDS9960 device IDs
APDS9960_DEV_ID = [0xab, 0x9c, 0xa8, -0x55]

# APDS9960 等待时间
APDS9960_TIME_FIFO_PAUSE = 0.03

# APDS9960 寄存器地址
APDS9960_REG_ENABLE = 0x80
APDS9960_REG_ATIME = 0x81
APDS9960_REG_WTIME = 0x83
APDS9960_REG_AILTL = 0x84
APDS9960_REG_AILTH = 0x85
APDS9960_REG_AIHTL = 0x86
APDS9960_REG_AIHTH = 0x87
APDS9960_REG_PILT = 0x89
APDS9960_REG_PIHT = 0x8b
APDS9960_REG_PERS = 0x8c
APDS9960_REG_CONFIG1 = 0x8d
APDS9960_REG_PPULSE = 0x8e
APDS9960_REG_CONTROL = 0x8f
APDS9960_REG_CONFIG2 = 0x90
APDS9960_REG_ID = 0x92
APDS9960_REG_STATUS = 0x93
APDS9960_REG_CDATAL = 0x94
APDS9960_REG_CDATAH = 0x95
APDS9960_REG_RDATAL = 0x96
APDS9960_REG_RDATAH = 0x97
APDS9960_REG_GDATAL = 0x98
APDS9960_REG_GDATAH = 0x99
APDS9960_REG_BDATAL = 0x9a
APDS9960_REG_BDATAH = 0x9b
APDS9960_REG_PDATA = 0x9c
APDS9960_REG_POFFSET_UR = 0x9d
APDS9960_REG_POFFSET_DL = 0x9e
APDS9960_REG_CONFIG3 = 0x9f
APDS9960_REG_GPENTH = 0xa0
APDS9960_REG_GEXTH = 0xa1
APDS9960_REG_GCONF1 = 0xa2
APDS9960_REG_GCONF2 = 0xa3
APDS9960_REG_GOFFSET_U = 0xa4
APDS9960_REG_GOFFSET_D = 0xa5
APDS9960_REG_GOFFSET_L = 0xa7
APDS9960_REG_GOFFSET_R = 0xa9
APDS9960_REG_GPULSE = 0xa6
APDS9960_REG_GCONF3 = 0xaA
APDS9960_REG_GCONF4 = 0xaB
APDS9960_REG_GFLVL = 0xae
APDS9960_REG_GSTATUS = 0xaf
APDS9960_REG_IFORCE = 0xe4
APDS9960_REG_PICLEAR = 0xe5
APDS9960_REG_CICLEAR = 0xe6
APDS9960_REG_AICLEAR = 0xe7
APDS9960_REG_GFIFO_U = 0xfc
APDS9960_REG_GFIFO_D = 0xfd
APDS9960_REG_GFIFO_L = 0xfe
APDS9960_REG_GFIFO_R = 0xff

# APDS9960 bit位
APDS9960_BIT_PON = 0b00000001
APDS9960_BIT_AEN = 0b00000010
APDS9960_BIT_PEN = 0b00000100
APDS9960_BIT_WEN = 0b00001000
APSD9960_BIT_AIEN =0b00010000
APDS9960_BIT_PIEN = 0b00100000
APDS9960_BIT_GEN = 0b01000000
APDS9960_BIT_GVALID = 0b00000001

# APDS9960 模式值
APDS9960_MODE_POWER = 0
APDS9960_MODE_AMBIENT_LIGHT = 1
APDS9960_MODE_PROXIMITY = 2
APDS9960_MODE_WAIT = 3
APDS9960_MODE_AMBIENT_LIGHT_INT = 4
APDS9960_MODE_PROXIMITY_INT = 5
APDS9960_MODE_GESTURE = 6
APDS9960_MODE_ALL = 7

# LED驱动值
APDS9960_LED_DRIVE_100MA = 0
APDS9960_LED_DRIVE_50MA = 1
APDS9960_LED_DRIVE_25MA = 2
APDS9960_LED_DRIVE_12_5MA = 3

# proximity 增益(PGAIN)值
APDS9960_PGAIN_1X = 0
APDS9960_PGAIN_2X = 1
APDS9960_PGAIN_4X = 2
APDS9960_PGAIN_8X = 3

# ALS 增益(AGAIN)值
APDS9960_AGAIN_1X = 0
APDS9960_AGAIN_4X = 1
APDS9960_AGAIN_16X = 2
APDS9960_AGAIN_64X = 3

# Gesture 手势(GGAIN)值
APDS9960_GGAIN_1X = 0
APDS9960_GGAIN_2X = 1
APDS9960_GGAIN_4X = 2
APDS9960_GGAIN_8X = 3

# LED 提高值
APDS9960_LED_BOOST_100 = 0
APDS9960_LED_BOOST_150 = 1
APDS9960_LED_BOOST_200 = 2
APDS9960_LED_BOOST_300 = 3    

# Gesture 等待时间
APDS9960_GWTIME_0MS = 0
APDS9960_GWTIME_2_8MS = 1
APDS9960_GWTIME_5_6MS = 2
APDS9960_GWTIME_8_4MS = 3
APDS9960_GWTIME_14_0MS = 4
APDS9960_GWTIME_22_4MS = 5
APDS9960_GWTIME_30_8MS = 6
APDS9960_GWTIME_39_2MS = 7

# 默认值
APDS9960_DEFAULT_ATIME = 219                            # 103ms
APDS9960_DEFAULT_WTIME = 246                            # 27ms
APDS9960_DEFAULT_PROX_PPULSE = 0x87                     # 16us, 8 pulses
APDS9960_DEFAULT_GESTURE_PPULSE = 0x89                  # 16us, 10 pulses
APDS9960_DEFAULT_POFFSET_UR = 0                         # 0 offset
APDS9960_DEFAULT_POFFSET_DL = 0                         # 0 offset
APDS9960_DEFAULT_CONFIG1 = 0x60                         # No 12x wait (WTIME) factor
APDS9960_DEFAULT_LDRIVE = APDS9960_LED_DRIVE_50MA
APDS9960_DEFAULT_PGAIN = APDS9960_PGAIN_4X
APDS9960_DEFAULT_AGAIN = APDS9960_AGAIN_4X
APDS9960_DEFAULT_PILT = 0                               # Low proximity threshold
APDS9960_DEFAULT_PIHT = 50                              # High proximity threshold
APDS9960_DEFAULT_AILT = 0xffff                          # Force interrupt for calibration
APDS9960_DEFAULT_AIHT = 0
APDS9960_DEFAULT_PERS = 0x11                            # 2 consecutive prox or ALS for int.
APDS9960_DEFAULT_CONFIG2 = 0x01                         # No saturation interrupts or LED boost  
APDS9960_DEFAULT_CONFIG3 = 0                            # Enable all photodiodes, no SAI
APDS9960_DEFAULT_GPENTH = 40                            # Threshold for entering gesture mode
APDS9960_DEFAULT_GEXTH = 30                             # Threshold for exiting gesture mode    
APDS9960_DEFAULT_GCONF1 = 0x40                          # 4 gesture events for int., 1 for exit
APDS9960_DEFAULT_GGAIN = APDS9960_GGAIN_2X
APDS9960_DEFAULT_GLDRIVE = APDS9960_LED_DRIVE_50MA
APDS9960_DEFAULT_GWTIME = APDS9960_GWTIME_2_8MS
APDS9960_DEFAULT_GOFFSET = 0                            # No offset scaling for gesture mode
APDS9960_DEFAULT_GPULSE = 0xc9                          # 32us, 10 pulses
APDS9960_DEFAULT_GCONF3 = 0                             # All photodiodes active during gesture
APDS9960_DEFAULT_GIEN = 0                               # Disable gesture interrupts

# 手势方向
APDS9960_DIR_NONE = 0
APDS9960_DIR_LEFT = 1
APDS9960_DIR_RIGHT = 2
APDS9960_DIR_UP = 3
APDS9960_DIR_DOWN = 4
APDS9960_DIR_NEAR = 5
APDS9960_DIR_FAR = 6
APDS9960_DIR_ALL = 7

GESTURES = {
    0:"none",
    1:"left",
    2:"right",
    3:"up",
    4:"down"
}

# 状态定义
APDS9960_STATE_NA = 0
APDS9960_STATE_NEAR = 1
APDS9960_STATE_FAR = 2
APDS9960_STATE_ALL = 3


class ADPS9960InvalidDevId(ValueError):
    def __init__(self, id, valid_ids):
        Exception.__init__(self, "Device id 0x{} is not a valied one (valid: {})!".format(format(id, '02x'), ', '.join(["0x{}".format(format(i, '02x')) for i in valid_ids])))

class ADPS9960InvalidMode(ValueError):
    def __init__(self, mode):
        Exception.__init__(self, "Feature mode {} is invalid!".format(mode))


class _APDS9960:
    """乐动模块 手势传感器"""
    """APDS9960"""
    class GestureData:
        def __init__(self):
            self.u_data = [0] * 32
            self.d_data = [0] * 32
            self.l_data = [0] * 32
            self.r_data = [0] * 32
            self.index = 0
            self.total_gestures = 0
            self.in_threshold = 0
            self.out_threshold = 0

    def __init__(self, bus=i2c, address=APDS9960_I2C_ADDR, valid_id=APDS9960_DEV_ID):
        self.address = address
        self.bus = bus

        # 用于手势检测的实例变量
        self.gesture_ud_delta_ = 0
        self.gesture_lr_delta_ = 0

        self.gesture_ud_count_ = 0
        self.gesture_lr_count_ = 0

        self.gesture_near_count_ = 0
        self.gesture_far_count_ = 0

        self.gesture_state_ = 0
        self.gesture_motion_ = APDS9960_DIR_NONE

        self.gesture_data_ = _APDS9960.GestureData()

        addr = self.bus.scan()
        if 57 in addr:
            pass
        else:
            raise OSError("APDS9960 init error, not found device!!!")

        # 检查设备ID
        self.dev_id = self._read_byte_data(APDS9960_REG_ID)
        if not self.dev_id in valid_id:
            raise ADPS9960InvalidDevId(self.dev_id, valid_id)

        # 关闭所有功能
        self.setMode(APDS9960_MODE_ALL, False)

        # 设置环境光和靠近寄存器的默认值  
        self._write_byte_data(APDS9960_REG_ATIME, APDS9960_DEFAULT_ATIME)
        self._write_byte_data(APDS9960_REG_WTIME, APDS9960_DEFAULT_WTIME)
        self._write_byte_data(APDS9960_REG_PPULSE, APDS9960_DEFAULT_PROX_PPULSE)
        self._write_byte_data(APDS9960_REG_POFFSET_UR, APDS9960_DEFAULT_POFFSET_UR)
        self._write_byte_data(APDS9960_REG_POFFSET_DL, APDS9960_DEFAULT_POFFSET_DL)
        self._write_byte_data(APDS9960_REG_CONFIG1, APDS9960_DEFAULT_CONFIG1)
        self.setLEDDrive(APDS9960_DEFAULT_LDRIVE)
        self.setProximityGain(APDS9960_DEFAULT_PGAIN)
        self.setAmbientLightGain(APDS9960_DEFAULT_AGAIN)
        self.setProxIntLowThresh(APDS9960_DEFAULT_PILT)
        self.setProxIntHighThresh(APDS9960_DEFAULT_PIHT)
        self.setLightIntLowThreshold(APDS9960_DEFAULT_AILT)
        self.setLightIntHighThreshold(APDS9960_DEFAULT_AIHT)

        self._write_byte_data(APDS9960_REG_PERS, APDS9960_DEFAULT_PERS)
        self._write_byte_data(APDS9960_REG_CONFIG2, APDS9960_DEFAULT_CONFIG2)
        self._write_byte_data(APDS9960_REG_CONFIG3, APDS9960_DEFAULT_CONFIG3)

        # 设置手势传感器的默认值  
        self.setGestureEnterThresh(APDS9960_DEFAULT_GPENTH)
        self.setGestureExitThresh(APDS9960_DEFAULT_GEXTH)
        self._write_byte_data(APDS9960_REG_GCONF1, APDS9960_DEFAULT_GCONF1)

        self.setGestureGain(APDS9960_DEFAULT_GGAIN)
        self.setGestureLEDDrive(APDS9960_DEFAULT_GLDRIVE)
        self.setGestureWaitTime(APDS9960_DEFAULT_GWTIME)
        self._write_byte_data(APDS9960_REG_GOFFSET_U, APDS9960_DEFAULT_GOFFSET)
        self._write_byte_data(APDS9960_REG_GOFFSET_D, APDS9960_DEFAULT_GOFFSET)
        self._write_byte_data(APDS9960_REG_GOFFSET_L, APDS9960_DEFAULT_GOFFSET)
        self._write_byte_data(APDS9960_REG_GOFFSET_R, APDS9960_DEFAULT_GOFFSET)
        self._write_byte_data(APDS9960_REG_GPULSE, APDS9960_DEFAULT_GPULSE)
        self._write_byte_data(APDS9960_REG_GCONF3, APDS9960_DEFAULT_GCONF3)
        self.setGestureIntEnable(APDS9960_DEFAULT_GIEN)

        self.enableGestureSensor() # 开启手势识别传感器
        sleep(1)

    def _read_byte_data(self, cmd):
        return self.bus.read_byte_data(self.address, cmd)

    def _write_byte_data(self, cmd, val):
        return self.bus.write_byte_data(self.address, cmd, val)

    def _read_i2c_block_data(self, cmd, num):
        return self.bus.read_i2c_block_data(self.address, cmd, num)
    
    def getMode(self):
        return self._read_byte_data(APDS9960_REG_ENABLE)

    def setMode(self, mode, enable=True):
        reg_val = self.getMode()

        if mode < 0 or mode > APDS9960_MODE_ALL:
            raise ADPS9960InvalidMode(mode)

        # 更改启用寄存器中的位
        if mode == APDS9960_MODE_ALL:
            if enable:
                reg_val = 0x7f
            else:
                reg_val = 0x00
        else:
            if enable:
                reg_val |= (1 << mode)
            else:
                reg_val &= ~(1 << mode)

        self._write_byte_data(APDS9960_REG_ENABLE, reg_val)

    # 启动环境光(R/G/B/Ambient)传感器
    def enableLightSensor(self, interrupts=True):
        self.setAmbientLightGain(APDS9960_DEFAULT_AGAIN)
        self.setAmbientLightIntEnable(interrupts)
        self.enablePower()
        self.setMode(APDS9960_MODE_AMBIENT_LIGHT, True)

    # 停止光传感器
    def disableLightSensor(self):
        self.setAmbientLightIntEnable(False)
        self.setMode(APDS9960_MODE_AMBIENT_LIGHT, False)

    # 启动接近传感器
    def enableProximitySensor(self, interrupts=True):
        self.setProximityGain(APDS9960_DEFAULT_PGAIN)
        self.setLEDDrive(APDS9960_DEFAULT_LDRIVE)
        self.setProximityIntEnable(interrupts)
        self.enablePower()
        self.setMode(APDS9960_MODE_PROXIMITY, True)

    # 停止接近传感器
    def disableProximitySensor(self):
        self.setProximityIntEnable(False)
        self.setMode(APDS9960_MODE_PROXIMITY, False)

    # 启动手势识别传感器
    def enableGestureSensor(self, interrupts=True):
        self.resetGestureParameters()
        self._write_byte_data(APDS9960_REG_WTIME, 0xff)
        self._write_byte_data(APDS9960_REG_PPULSE, APDS9960_DEFAULT_GESTURE_PPULSE)
        self.setLEDBoost(APDS9960_LED_BOOST_300)
        self.setGestureIntEnable(interrupts)
        self.setGestureMode(True)
        self.enablePower()
        self.setMode(APDS9960_MODE_WAIT, True)
        self.setMode(APDS9960_MODE_PROXIMITY, True)
        self.setMode(APDS9960_MODE_GESTURE, True)

    # 停止手势识别传感器
    def disableGestureSensor(self):
        self.resetGestureParameters()
        self.setGestureIntEnable(False)
        self.setGestureMode(False)
        self.setMode(APDS9960_MODE_GESTURE, False)

    # 检查是否有可用的手势
    def isGestureAvailable(self):
        val = self._read_byte_data(APDS9960_REG_GSTATUS)
        val &= APDS9960_BIT_GVALID

        return (val == APDS9960_BIT_GVALID)

    # 处理一个手势事件并返回最佳的手势  
    def readGesture(self):
        fifo_level = 0
        fifo_data = []
        bytes_read = 0

        # 确保电源和手势是打开的，数据是有效的  
        if not (self.getMode() & 0b01000001) or not self.isGestureAvailable():
            # return APDS9960_DIR_NONE
            return "none"

        # 只要手势数据有效，就保持循环
        while(self.isGestureAvailable()):
            # 读取当前的FIFO级别
            fifo_level = self._read_byte_data(APDS9960_REG_GFLVL)

            # 如果有数据在FIFO，读入我们的数据块  
            if fifo_level > 0:
                fifo_data = []
                for i in range(0, fifo_level):
                    fifo_data += self._read_i2c_block_data(APDS9960_REG_GFIFO_U, 4)

                # 如果至少有一组数据，则将数据排序为U/D/L/R  
                if len(fifo_data) >= 4:
                    for i in range(0, len(fifo_data), 4):
                        self.gesture_data_.u_data[self.gesture_data_.index] = fifo_data[i + 0]
                        self.gesture_data_.d_data[self.gesture_data_.index] = fifo_data[i + 1]
                        self.gesture_data_.l_data[self.gesture_data_.index] = fifo_data[i + 2]
                        self.gesture_data_.r_data[self.gesture_data_.index] = fifo_data[i + 3]
                        self.gesture_data_.index += 1
                        self.gesture_data_.total_gestures += 1

                    # 过滤和处理手势数据，解码近/远状态  
                    if self.processGestureData():
                        if self.decodeGesture():
                            pass

                    # 重置数据
                    self.gesture_data_.index = 0
                    self.gesture_data_.total_gestures = 0

            # 等待一段时间以收集下一批FIFO数据 
            sleep(APDS9960_TIME_FIFO_PAUSE)

        # 确定最佳手势并清理数据 
        sleep(APDS9960_TIME_FIFO_PAUSE)
        self.decodeGesture()
        motion = self.gesture_motion_

        self.resetGestureParameters()
        # return motion 
        Gesture = GESTURES.get(motion,0)
        return Gesture


    # 打开APDS9960电源
    def enablePower(self):
        self.setMode(APDS9960_MODE_POWER, True)

    # 关闭APDS9960电源
    def disablePower(self):
        self.setMode(APDS9960_MODE_POWER, False)

    # *******************************************************************************
    # 环境光和颜色传感器
    # *******************************************************************************

    # reads the ambient (clear) light level as a 16-bit value
    def readAmbientLight(self):
        l = self._read_byte_data(APDS9960_REG_CDATAL)
        h = self._read_byte_data(APDS9960_REG_CDATAH)

        return l + (h << 8)

    # reads the red light level as a 16-bit value
    def readRedLight(self):
        l = self._read_byte_data(APDS9960_REG_RDATAL)
        h = self._read_byte_data(APDS9960_REG_RDATAH)

        return l + (h << 8)

    # reads the green light level as a 16-bit value
    def readGreenLight(self):
        l = self._read_byte_data(APDS9960_REG_GDATAL)
        h = self._read_byte_data(APDS9960_REG_GDATAH)

        return l + (h << 8)

    # reads the blue light level as a 16-bit value
    def readBlueLight(self):
        l = self._read_byte_data(APDS9960_REG_BDATAL)
        h = self._read_byte_data(APDS9960_REG_BDATAH)

        return l + (h << 8)


    # *******************************************************************************
    # Proximity sensor 接近传感器
    # *******************************************************************************

    # reads the proximity level as an 8-bit value
    def readProximity(self):
        return self._read_byte_data(APDS9960_REG_PDATA)


    # *******************************************************************************
    # High-level gesture controls
    # *******************************************************************************

    # 重置手势数据成员中的所有参数  
    def resetGestureParameters(self):
        self.gesture_data_.index = 0
        self.gesture_data_.total_gestures = 0

        self.gesture_ud_delta_ = 0
        self.gesture_lr_delta_ = 0

        self.gesture_ud_count_ = 0
        self.gesture_lr_count_ = 0

        self.gesture_near_count_ = 0
        self.gesture_far_count_ = 0

        self.gesture_state_ = 0
        self.gesture_motion_ = APDS9960_DIR_NONE

    def processGestureData(self):
        """ 
            处理原始手势数据以确定滑动方向  
            return: bool: 如果看到近或远的状态，则为真，否则为假。  
        """
        u_first = 0
        d_first = 0
        l_first = 0
        r_first = 0
        u_last = 0
        d_last = 0
        l_last = 0
        r_last = 0

        # 如果我们的手势总数少于4个，那是不够的  
        if self.gesture_data_.total_gestures <= 4:
            return False

        # 检查一下，确保我们的数据没有越界  
        if self.gesture_data_.total_gestures <= 32 and self.gesture_data_.total_gestures > 0:
            # 找到U/D/L/R中高于阈值的第一个值  
            for i in range(0, self.gesture_data_.total_gestures):
                if self.gesture_data_.u_data[i] > APDS9960_GESTURE_THRESHOLD_OUT and \
                   self.gesture_data_.d_data[i] > APDS9960_GESTURE_THRESHOLD_OUT and \
                   self.gesture_data_.l_data[i] > APDS9960_GESTURE_THRESHOLD_OUT and \
                   self.gesture_data_.r_data[i] > APDS9960_GESTURE_THRESHOLD_OUT:

                    u_first = self.gesture_data_.u_data[i]
                    d_first = self.gesture_data_.d_data[i]
                    l_first = self.gesture_data_.l_data[i]
                    r_first = self.gesture_data_.r_data[i]
                    break

            # 如果_first值中有一个为0，则不是好数据  
            if u_first == 0 or  d_first == 0 or l_first == 0 or r_first == 0:
                return False
  
            # 在U/D/L/R中找到高于阈值的最后一个值  
            # 反转迭代器 reversed
            for i in reversed(range(0, self.gesture_data_.total_gestures)):
                if self.gesture_data_.u_data[i] > APDS9960_GESTURE_THRESHOLD_OUT and \
                   self.gesture_data_.d_data[i] > APDS9960_GESTURE_THRESHOLD_OUT and \
                   self.gesture_data_.l_data[i] > APDS9960_GESTURE_THRESHOLD_OUT and \
                   self.gesture_data_.r_data[i] > APDS9960_GESTURE_THRESHOLD_OUT:

                    u_last = self.gesture_data_.u_data[i]
                    d_last = self.gesture_data_.d_data[i]
                    l_last = self.gesture_data_.l_data[i]
                    r_last = self.gesture_data_.r_data[i]
                    break

            # 计算上/下和左/右的第一个和最后一个比率  
            ud_ratio_first = ((u_first - d_first) * 100) / (u_first + d_first)
            lr_ratio_first = ((l_first - r_first) * 100) / (l_first + r_first)
            ud_ratio_last = ((u_last - d_last) * 100) / (u_last + d_last)
            lr_ratio_last = ((l_last - r_last) * 100) / (l_last + r_last)

            # 确定第一个和最后一个比率之间的差异  
            ud_delta = ud_ratio_last - ud_ratio_first
            lr_delta = lr_ratio_last - lr_ratio_first

            # 累积UD和LR delta值
            self.gesture_ud_delta_ += ud_delta
            self.gesture_lr_delta_ += lr_delta

            # 确定 U/D 手势
            if self.gesture_ud_delta_ >= APDS9960_GESTURE_SENSITIVITY_1:
                self.gesture_ud_count_ = 1
            elif self.gesture_ud_delta_ <= -APDS9960_GESTURE_SENSITIVITY_1:
                self.gesture_ud_count_ = -1
            else:
                self.gesture_ud_count_ = 0

            # 确定 L/R 手势
            if self.gesture_lr_delta_ >= APDS9960_GESTURE_SENSITIVITY_1:
                self.gesture_lr_count_ = 1
            elif self.gesture_lr_delta_ <= -APDS9960_GESTURE_SENSITIVITY_1:
                self.gesture_lr_count_ = -1
            else:
                self.gesture_lr_count_ = 0

            # 确定 Near/Far 
            if self.gesture_ud_count_ == 0 and self.gesture_lr_count_ == 0:
                if abs(ud_delta) < APDS9960_GESTURE_SENSITIVITY_2 and \
                    abs(lr_delta) < APDS9960_GESTURE_SENSITIVITY_2:

                    if ud_delta == 0 and lr_delta == 0:
                        self.gesture_near_count_ += 1
                    elif ud_delta != 0 or lr_delta != 0:
                        self.gesture_far_count_ += 1

                    if self.gesture_near_count_ >= 10 and self.gesture_far_count_ >= 2:
                        if ud_delta == 0 and lr_delta == 0:
                            self.gesture_state_ = APDS9960_STATE_NEAR
                        elif ud_delta != 0 and lr_delta != 0:
                            self.gesture_state_ = APDS9960_STATE_FAR
                        return True
            else:
                if abs(ud_delta) < APDS9960_GESTURE_SENSITIVITY_2 and \
                    abs(lr_delta) < APDS9960_GESTURE_SENSITIVITY_2:

                        if ud_delta == 0 and lr_delta == 0:
                            self.gesture_near_count_ += 1

                        if self.gesture_near_count_ >= 10:
                            self.gesture_ud_count_ = 0
                            self.gesture_lr_count_ = 0
                            self.gesture_ud_delta_ = 0
                            self.gesture_lr_delta_ = 0

        return False

    def decodeGesture(self):
        """
        确定滑动方向或近/远状态。
        """
        # 如果检测到近或远事件，则返回
        # if self.gesture_state_ == APDS9960_STATE_NEAR:
        #     self.gesture_motion_ = APDS9960_DIR_NEAR
        #     return True

        # if self.gesture_state_ == APDS9960_STATE_FAR:
        #     self.gesture_motion_ = APDS9960_DIR_FAR
        #     return True

        # 确定滑动方向
        if self.gesture_ud_count_ == -1 and self.gesture_lr_count_ == 0:
            self.gesture_motion_ = APDS9960_DIR_UP
        elif self.gesture_ud_count_ == 1 and self.gesture_lr_count_ == 0:
            self.gesture_motion_ = APDS9960_DIR_DOWN
        elif self.gesture_ud_count_ == 0 and self.gesture_lr_count_ == 1:
            self.gesture_motion_ = APDS9960_DIR_RIGHT
        elif self.gesture_ud_count_ == 0 and self.gesture_lr_count_ == -1:
            self.gesture_motion_ = APDS9960_DIR_LEFT
        elif self.gesture_ud_count_ == -1 and self.gesture_lr_count_ == 1:
            if abs(self.gesture_ud_delta_) > abs(self.gesture_lr_delta_):
                self.gesture_motion_ = APDS9960_DIR_UP
            else:
                self.gesture_motion_ = APDS9960_DIR_DOWN
        elif self.gesture_ud_count_ == 1 and self.gesture_lr_count_ == -1:
            if abs(self.gesture_ud_delta_) > abs(self.gesture_lr_delta_):
                self.gesture_motion_ = APDS9960_DIR_DOWN
            else:
                self.gesture_motion_ = APDS9960_DIR_LEFT
        elif self.gesture_ud_count_ == -1 and self.gesture_lr_count_ == -1:
            if abs(self.gesture_ud_delta_) > abs(self.gesture_lr_delta_):
                self.gesture_motion_ = APDS9960_DIR_UP
            else:
                self.gesture_motion_ = APDS9960_DIR_LEFT
        elif self.gesture_ud_count_ == 1 and self.gesture_lr_count_ == 1:
            if abs(self.gesture_ud_delta_) > abs(self.gesture_lr_delta_):
                self.gesture_motion_ = APDS9960_DIR_DOWN
            else:
                self.gesture_motion_ = APDS9960_DIR_RIGHT
        else:
            return False

        return True


    # *******************************************************************************
    # Getters and setters for register values
    # *******************************************************************************
    def getProxIntLowThresh(self):
        return self._read_byte_data(APDS9960_REG_PILT)

    def setProxIntLowThresh(self, threshold):
        """设置接近检测的低阈值 """
        self._write_byte_data(APDS9960_REG_PILT, threshold)

    def getProxIntHighThresh(self):
        return self._read_byte_data(APDS9960_REG_PIHT)

    def setProxIntHighThresh(self, threshold):
        """ 设置接近检测的高阈值 """
        self._write_byte_data(APDS9960_REG_PIHT, threshold)

    def getLEDDrive(self):
        val = self._read_byte_data(APDS9960_REG_CONTROL)

        return (val >> 6) & 0b00000011

    def setLEDDrive(self, drive):
        """ proximity , ALS 设置LED驱动强度 

            Value    LED Current
              0        100 mA
              1         50 mA
              2         25 mA
              3         12.5 mA
        """
        val = self._read_byte_data(APDS9960_REG_CONTROL)

        drive &= 0b00000011
        drive = drive << 6
        val &= 0b00111111
        val |= drive

        self._write_byte_data(APDS9960_REG_CONTROL, val)

    def getProximityGain(self):
        val = self._read_byte_data(APDS9960_REG_CONTROL)
        return (val >> 2) & 0b00000011

    def setProximityGain(self, drive):
        """设置接近传感器返回接收器增益。  
            Value    Gain
              0       1x
              1       2x
              2       4x
              3       8x
        """
        val = self._read_byte_data(APDS9960_REG_CONTROL)

        drive &= 0b00000011
        drive = drive << 2
        val &= 0b11110011
        val |= drive

        self._write_byte_data(APDS9960_REG_CONTROL, val)

    def getAmbientLightGain(self):
        val = self._read_byte_data(APDS9960_REG_CONTROL)
        return (val & 0b00000011)

    def setAmbientLightGain(self, drive):
        """设置环境光传感器的接收增益 (ALS)

            Value    Gain
              0       1x
              1       4x
              2       16x
              3       64x
        """
        val = self._read_byte_data(APDS9960_REG_CONTROL)

        drive &= 0b00000011
        val &= 0b11111100
        val |= drive

        self._write_byte_data(APDS9960_REG_CONTROL, val)

    def getLEDBoost(self):
        val = self._read_byte_data(APDS9960_REG_CONFIG2)
        return (val >> 4) & 0b00000011

    def setLEDBoost(self, boost):
        """设置LED电流提升值

            Value    Gain
              0        100%
              1        150%
              2        200%
              3        300%
        """
        val = self._read_byte_data(APDS9960_REG_CONFIG2)

        boost &= 0b00000011
        boost = boost << 4
        val &= 0b11001111
        val |= boost

        self._write_byte_data(APDS9960_REG_CONFIG2, val)

    def getProxGainCompEnable(self):
        val = self._read_byte_data(APDS9960_REG_CONFIG3)
        val = (val >> 5) & 0b00000001
        return val == 1

    def setProxGainCompEnable(self, enable):
        """设置接近增益补偿使能。"""
        val = self._read_byte_data(APDS9960_REG_CONFIG3)
        val &= 0b11011111
        if enable:
            val |= 0b00100000

        self._write_byte_data(APDS9960_REG_CONFIG3, val)

    def getProxPhotoMask(self):
        val = self._read_byte_data(APDS9960_REG_CONFIG3)
        return val & 0b00001111

    def setProxPhotoMask(self, mask):
        """ 设置掩码来启用/禁用近距离光电二极管。  

            Bit    Photodiode
             3       UP
             2       DOWN
             1       LEFT
             0       RIGHT

            1 = disabled, 0 = enabled

            Args:
                mask (int): 4-bit mask value
        """
        val = self._read_byte_data(APDS9960_REG_CONFIG3)

        mask &= 0b00001111
        val &= 0b11110000
        val |= mask

        self._write_byte_data(APDS9960_REG_CONFIG3, val)

    def getGestureEnterThresh(self):
        return self._read_byte_data(APDS9960_REG_GPENTH)

    def setGestureEnterThresh(self, threshold):
        """设置手势感应的入口接近阈值"""
        self._write_byte_data(APDS9960_REG_GPENTH, threshold)

    def getGestureExitThresh(self):
        return self._read_byte_data(APDS9960_REG_GEXTH)

    def setGestureExitThresh(self, threshold):
        """设置手势感应的出口接近阈值"""
        self._write_byte_data(APDS9960_REG_GEXTH, threshold)

    def getGestureGain(self):
        val = self._read_byte_data(APDS9960_REG_GCONF2)
        return (val >> 5) & 0b00000011

    def setGestureGain(self, gain):
        """ 在手势模式下设置光电二极管的增益

            Value    Gain
              0       1x
              1       2x
              2       4x
              3       8x
        """
        val = self._read_byte_data(APDS9960_REG_GCONF2)

        gain &= 0b00000011
        gain = gain << 5
        val &= 0b10011111
        val |= gain

        self._write_byte_data(APDS9960_REG_GCONF2, val)

    def getGestureLEDDrive(self):
        val = self._read_byte_data(APDS9960_REG_GCONF2)
        return (val >> 3) & 0b00000011

    def setGestureLEDDrive(self, drive):
        """ 设置proximity和ALSLED驱动强度

            Value    LED Current
              0        100 mA
              1         50 mA
              2         25 mA
              3         12.5 mA
        """
        val = self._read_byte_data(APDS9960_REG_GCONF2)

        drive &= 0b00000011
        drive = drive << 3
        val &= 0b11100111
        val |= drive

        self._write_byte_data(APDS9960_REG_GCONF2, val)

    def getGestureWaitTime(self):
        val = self._read_byte_data(APDS9960_REG_GCONF2)
        return val & 0b00000111

    def setGestureWaitTime(self, time):
        """ 设置两次手势检测之间的低功耗模式时间

            Value      Wait time
              0          0 ms
              1          2.8 ms
              2          5.6 ms
              3          8.4 ms
              4         14.0 ms
              5         22.4 ms
              6         30.8 ms
              7         39.2 ms
        """
        val = self._read_byte_data(APDS9960_REG_GCONF2)

        time &= 0b00000111
        val &= 0b11111000
        val |= time

        self._write_byte_data(APDS9960_REG_GCONF2, val)

    def getLightIntLowThreshold(self):
        return self._read_byte_data(APDS9960_REG_AILTL) | (self._read_byte_data(APDS9960_REG_AILTH) << 8)

    def setLightIntLowThreshold(self, threshold):
        """设置环境光中断的低阈值"""
        # break 16-bit threshold into 2 8-bit values
        self._write_byte_data(APDS9960_REG_AILTL, threshold & 0x00ff)
        self._write_byte_data(APDS9960_REG_AILTH, (threshold & 0xff00) >> 8)

    def getLightIntHighThreshold(self):
        return self._read_byte_data(APDS9960_REG_AIHTL) | (self._read_byte_data(APDS9960_REG_AIHTH) << 8)

    def setLightIntHighThreshold(self, threshold):
        """设置环境光中断的高阈值"""
        # break 16-bit threshold into 2 8-bit values
        self._write_byte_data(APDS9960_REG_AIHTL, threshold & 0x00ff)
        self._write_byte_data(APDS9960_REG_AIHTH, (threshold & 0xff00) >> 8)

    def getProximityIntLowThreshold(self):
        return self._read_byte_data(APDS9960_REG_PILT)

    def setProximityIntLowThreshold(self, threshold):
        """为接近中断设置低阈值"""
        self._write_byte_data(APDS9960_REG_PILT, threshold)

    def getProximityIntHighThreshold(self):
        return self._read_byte_data(APDS9960_REG_PIHT)

    def setProximityIntHighThreshold(self, threshold):
        """为接近中断设置高阈值"""
        self._write_byte_data(APDS9960_REG_PIHT, threshold)

    def getAmbientLightIntEnable(self):
        val = self._read_byte_data(APDS9960_REG_ENABLE)
        return (val >> 4) & 0b00000001 == 1

    def setAmbientLightIntEnable(self, enable):
        """打开或关闭环境光中断"""
        val = self._read_byte_data(APDS9960_REG_ENABLE)

        val &= 0b11101111
        if enable:
            val |= 0b00010000

        self._write_byte_data(APDS9960_REG_ENABLE, val)

    def getProximityIntEnable(self):
        val = self._read_byte_data(APDS9960_REG_ENABLE)
        return (val >> 5) & 0b00000001 == 1

    def setProximityIntEnable(self, enable):
        """打开或关闭靠近中断"""
        val = self._read_byte_data(APDS9960_REG_ENABLE)

        val &= 0b11011111
        if enable:
            val |= 0b00100000

        self._write_byte_data(APDS9960_REG_ENABLE, val)

    def getGestureIntEnable(self):
        val = self._read_byte_data(APDS9960_REG_GCONF4)
        return (val >> 1) & 0b00000001 == 1

    def setGestureIntEnable(self, enable):
        """打开或关闭与手势相关的中断"""
        val = self._read_byte_data(APDS9960_REG_GCONF4)

        val &= 0b11111101
        if enable:
            val |= 0b00000010

        self._write_byte_data(APDS9960_REG_GCONF4, val)

    def clearAmbientLightInt(self):
        """清除环境光中断"""
        self._read_byte_data(APDS9960_REG_AICLEAR)

    def clearProximityInt(self):
        """清除靠近中断"""
        self._read_byte_data(APDS9960_REG_PICLEAR)

    def getGestureMode(self):
        val = self._read_byte_data(APDS9960_REG_GCONF4)
        return val & 0b00000001 == 1

    def setGestureMode(self, enable):
        """打开或关闭与手势相关的中断。"""
        val = self._read_byte_data(APDS9960_REG_GCONF4)
        val &= 0b11111110
        if enable:
            val |= 0b00000001

        self._write_byte_data(APDS9960_REG_GCONF4, val)  
    

class Gesture(_APDS9960):
    def _read_byte_data(self, cmd):
        return self.bus.readfrom_mem(self.address, cmd, 1)[0]

    def _write_byte_data(self, cmd, val):
        self.bus.writeto_mem(self.address, cmd, bytes([val]))

    def _read_i2c_block_data(self, cmd, num):
        return self.bus.readfrom_mem(self.address, cmd, num)
