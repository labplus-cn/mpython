"""
用于 Jmrobot 4 通道 DRV8837 电机驱动模块的 MicroPython 驱动程序。

该模块通过 I2C 使用 SX1508 I/O 扩展器。SX1508 PWM/LED 驱动器的
输出连接到四个 DRV8837 电机驱动器：

    M1: IO0 / IO1
    M2: IO2 / IO3
    M3: IO4 / IO5
    M4: IO6 / IO7
"""

from time import sleep_ms


MDDRV8837_ADDRESS = 0x20

REG_INPUT_DISABLE = 0x00
REG_PULL_UP = 0x03
REG_DIR = 0x07
REG_DATA = 0x08
REG_INTERRUPT_MASK = 0x09
REG_CLOCK = 0x0F
REG_MISC = 0x10
REG_LED_DRIVER_ENABLE = 0x11
REG_RESET = 0x7D

REG_I_ON = (0x16, 0x17, 0x19, 0x1C, 0x20, 0x21, 0x23, 0x26)

INTERNAL_CLOCK_2MHZ = 2

M1_PIN_A = 0
M1_PIN_B = 1
M2_PIN_A = 2
M2_PIN_B = 3
M3_PIN_A = 4
M3_PIN_B = 5
M4_PIN_A = 6
M4_PIN_B = 7


class MDDRV8837:
    """用于 Jmrobot SX1508 + 4x DRV8837 电机模块的 I2C 驱动程序。"""

    MOTOR_PINS = (
        (M1_PIN_A, M1_PIN_B),
        (M2_PIN_A, M2_PIN_B),
        (M3_PIN_A, M3_PIN_B),
        (M4_PIN_A, M4_PIN_B),
    )

    def __init__(self, i2c, address=MDDRV8837_ADDRESS, reset_pin=None, brake_on_stop=True):
        """
        创建驱动对象并自动完成初始化。

        参数:
            i2c         : 已配置的 machine.I2C 实例。
            address     : SX1508 I2C 地址，Jmrobot 模块默认 0x20。
            reset_pin   : 可选 machine.Pin，连接到 SX1508 nRST 引脚。
            brake_on_stop: True → 速度为 0 时制动；False → 惯性滑行。

        异常:
            RuntimeError: 设备未找到或 I2C 通信失败时抛出。
        """
        self.i2c = i2c
        self.address = address
        self.reset_pin = reset_pin
        self.brake_on_stop = brake_on_stop
        self._clk_x = 0
        self._init()

    # ------------------------------------------------------------------
    # 内部初始化
    # ------------------------------------------------------------------

    def _init(self):
        """复位并初始化 SX1508 PWM 输出（由 __init__ 自动调用）。"""
        try:
            if hasattr(self.i2c, "scan") and self.address not in self.i2c.scan():
                raise RuntimeError(
                    "DRV8837 模块未找到，请检查接线及 I2C 地址 0x{:02X}".format(self.address)
                )

            self.reset()

            if self._read_byte(REG_INTERRUPT_MASK) != 0xFF:
                raise RuntimeError("DRV8837 通信验证失败，寄存器值异常")

            self.clock(INTERNAL_CLOCK_2MHZ, divider=1)
            for pin_a, pin_b in self.MOTOR_PINS:
                self.led_driver_init(pin_a)
                self.led_driver_init(pin_b)

            self.stop_motor(5)
        except OSError as exc:
            raise RuntimeError("DRV8837 I2C 通信错误") from exc

    def begin(self):
        """废弃：已改为自动初始化，此方法仅用于兼容旧代码。"""
        self._init()
        return True

    def reset(self):
        """当提供 reset_pin 时进行硬件复位，否则进行 SX1508 软件复位。"""
        if self.reset_pin is not None:
            self.reset_pin.init(getattr(self.reset_pin, "OUT", 1))
            self.reset_pin.value(0)
            sleep_ms(1)
            self.reset_pin.value(1)
            sleep_ms(1)
            return

        self._write_byte(REG_RESET, 0x12)
        self._write_byte(REG_RESET, 0x34)
        sleep_ms(1)

    def clock(self, source=INTERNAL_CLOCK_2MHZ, divider=1):
        """配置 SX1508 振荡器和 LED 驱动器时钟。"""
        divider = min(7, max(1, int(divider)))
        reg_clock = (source & 0x03) << 5
        self._write_byte(REG_CLOCK, reg_clock)

        self._clk_x = 2000000 // (1 << (divider - 1))
        reg_misc = self._read_byte(REG_MISC)
        reg_misc &= ~(0x07 << 4)
        reg_misc |= (divider & 0x07) << 4
        self._write_byte(REG_MISC, reg_misc)

    def led_driver_init(self, pin, log=False):
        """在一个 IO 引脚上启用 SX1508 PWM 输出。"""
        self._check_pin(pin)

        value = self._read_byte(REG_INPUT_DISABLE)
        self._write_byte(REG_INPUT_DISABLE, value | (1 << pin))

        value = self._read_byte(REG_PULL_UP)
        self._write_byte(REG_PULL_UP, value & ~(1 << pin))

        value = self._read_byte(REG_DIR)
        self._write_byte(REG_DIR, value & ~(1 << pin))

        value = self._read_byte(REG_CLOCK)
        value |= 1 << 6
        value &= ~(1 << 5)
        self._write_byte(REG_CLOCK, value)

        value = self._read_byte(REG_MISC)
        if log:
            value |= (1 << 7) | (1 << 3)
        else:
            value &= ~((1 << 7) | (1 << 3))
        if self._clk_x == 0:
            value &= ~(0x07 << 4)
            value |= 1 << 4
            self._clk_x = 2000000
        self._write_byte(REG_MISC, value)

        value = self._read_byte(REG_LED_DRIVER_ENABLE)
        self._write_byte(REG_LED_DRIVER_ENABLE, value | (1 << pin))

        value = self._read_byte(REG_DATA)
        self._write_byte(REG_DATA, value & ~(1 << pin))

    def analog_write(self, pin, duty):
        """设置 SX1508 PWM 占空比，范围 0..255。"""
        self._check_pin(pin)
        duty = min(255, max(0, int(duty)))
        self._write_byte(REG_I_ON[pin], duty)

    def set_motor_speed(self, pin_a, pin_b, speed):
        """通过两个 SX1508 PWM 引脚驱动一个 DRV8837。"""
        speed = min(255, max(-255, int(speed)))

        if speed > 0:
            self.analog_write(pin_a, speed)
            self.analog_write(pin_b, 0)
        elif speed < 0:
            self.analog_write(pin_b, -speed)
            self.analog_write(pin_a, 0)
        elif self.brake_on_stop:
            self.analog_write(pin_a, 255)
            self.analog_write(pin_b, 255)
        else:
            self.analog_write(pin_a, 0)
            self.analog_write(pin_b, 0)

    def set_motor(self, *args):
        """
        驱动一个电机或全部四个电机。

        调用形式:
            set_motor(motor_id, speed)
            set_motor(m1_speed, m2_speed, m3_speed, m4_speed)

        速度范围: -255..255。正值和负值控制不同方向。
        """
        if len(args) == 4:
            self.set_motors(args[0], args[1], args[2], args[3])
            return

        if len(args) != 2:
            raise TypeError("set_motor expects 2 or 4 arguments")

        motor_id, speed = args
        speed = min(255, max(-255, int(speed)))
        motor_id = int(motor_id)

        if 1 <= motor_id <= 4:
            pin_a, pin_b = self.MOTOR_PINS[motor_id - 1]
            self.set_motor_speed(pin_a, pin_b, speed)
            return

        self.set_motors(speed, speed, speed, speed)

    def set_motors(self, m1_speed, m2_speed, m3_speed, m4_speed):
        """以独立速度驱动所有四个电机。"""
        speeds = (m1_speed, m2_speed, m3_speed, m4_speed)
        for (pin_a, pin_b), speed in zip(self.MOTOR_PINS, speeds):
            self.set_motor_speed(pin_a, pin_b, speed)

    def stop_motor(self, motor_id=5, brake=None):
        """停止一个或所有电机。brake 参数会覆盖 self.brake_on_stop。"""
        previous = self.brake_on_stop
        if brake is not None:
            self.brake_on_stop = bool(brake)
        try:
            self.set_motor(motor_id, 0)
        finally:
            self.brake_on_stop = previous

    def brake_motor(self, motor_id=5):
        """通过将两个 DRV8837 输入引脚置高来停止（制动）。"""
        self.stop_motor(motor_id, brake=True)

    def coast_motor(self, motor_id=5):
        """通过将两个 DRV8837 输入引脚置低来停止（惯性滑行）。"""
        self.stop_motor(motor_id, brake=False)

    def _read_byte(self, register):
        return self.i2c.readfrom_mem(self.address, register, 1)[0]

    def _write_byte(self, register, value):
        self.i2c.writeto_mem(self.address, register, bytes((value & 0xFF,)))

    @staticmethod
    def _check_pin(pin):
        if not 0 <= int(pin) <= 7:
            raise ValueError("SX1508 pin must be in range 0..7")

    # 兼容 Arduino 风格的别名，便于代码移植。
    setMotorSpeed = set_motor_speed
    setMotor = set_motor
    setMotors = set_motors
    stopMotor = stop_motor
    brakeMotor = brake_motor
    coastMotor = coast_motor
    analogWrite = analog_write

