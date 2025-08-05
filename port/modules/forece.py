from mpython import i2c
import time


DEVICE_ADDR = 0x50  # 需要根据实际I2C设备地址修改
REG_CMD = 0xf6      # 命令寄存器
REG_STATUS = 0xf7   # 状态寄存器
REG_DATA = 0xf8     # 数据寄存器
REG_VERSION = 0x10   # 新增固件版本寄存器



class Forece():
    def __init__(self):
        self.i2c = i2c
        i2c_addr = self.i2c.scan()
        if DEVICE_ADDR not in i2c_addr:
            raise ValueError("未找到设备")
        time.sleep(0.1)  # 确保I2C初始化完成

    def word_to_signed(self, word):
        return word - 0x10000 if word & 0x8000 else word
    
    def read_sensor_data(self):
        data_buffer = bytearray()
        
        try:
            # 步骤1: 进入读取模式
            self.i2c.writeto_mem(DEVICE_ADDR, REG_CMD, b'\x20')
            n = 0
            while True:
                # 步骤2: 请求新数据帧
                self.i2c.writeto_mem(DEVICE_ADDR, REG_STATUS, b'\x00')
                
                # 步骤3: 轮询状态寄存器（最多等待100ms）
                start_time = time.ticks_ms()
                while True:
                    n = self.i2c.readfrom_mem(DEVICE_ADDR, REG_STATUS, 1)[0]
                    if n != 0 or time.ticks_diff(time.ticks_ms(), start_time) > 100:
                        break
                    time.sleep_ms(1)
                    
                
                # 步骤4: 读取数据
                data_chunk = self.i2c.readfrom_mem(DEVICE_ADDR, REG_DATA, n)
                data_buffer.extend(data_chunk)
                if n != 0:
                    break  # 没有更多数据
                time.sleep_ms(20)  # 适当延时保证数据稳定
            
            # 步骤6: 退出读取模式
            self.i2c.writeto_mem(DEVICE_ADDR, REG_CMD, b'\x00')
            # 数据完整性检查
            if len(data_buffer) < 2 or len(data_buffer) % 2 != 0:
                raise ValueError("无效数据长度")
                
            # 转换为word列表（小端模式）
            words = []
            for i in range(0, len(data_buffer), 2):
                word = (data_buffer[i+1] << 8) | data_buffer[i]
                words.append(word)
            
            # 校验和验证
            if len(words) < 1:
                raise ValueError("无有效数据")
            
            signed_data = [self.word_to_signed(w) for w in words]    
            calculated = sum(signed_data)
            
            if calculated != 0:
                raise ValueError("校验和错误")
    
            return signed_data[:1]  # 返回有效数据（排除校验和）
        
        except Exception as e:
            # 确保退出读取模式
            self.i2c.writeto_mem(DEVICE_ADDR, REG_CMD, b'\x00')
            raise e

    def read_firmware_version(self):
        """读取固件版本号"""
        try:
            # 直接读取4字节版本数据
            raw = self.i2c.readfrom_mem(DEVICE_ADDR, REG_VERSION, 4)
            if len(raw) != 4:
                raise ValueError("版本数据长度错误")
                
            # 转换为整数列表
            version_numbers = list(raw)
            # 格式化成字符串
            return "{}.{}.{}.{}".format(version_numbers[0],version_numbers[1],version_numbers[2],version_numbers[3])
            
        except Exception as e:
            print("读取版本失败: {}".format(str(e)))
    
    def read(self):
        """读取传感器数据"""
        try:   
            sensor_values = max(min(self.read_sensor_data()[0], 2000), 0)        # 单位g
            newton  = sensor_values * 0.00981    # 将质量g转为力的单位N
            return newton,sensor_values
        except Exception as e:
            print("读取错误:", e)
            return None,None
