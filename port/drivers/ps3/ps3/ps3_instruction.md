# 掌控板（ESP32）PS3 蓝牙手柄 C 模块使用文档

本项目在 `mpython` 经典版（ESP32 芯片）固件中集成并移植了 PS3 蓝牙手柄驱动（基于开源的 `esp32-ps3` 底层协议栈），以 C 语言原生接口注册为 MicroPython 内置的 `ps3` 模块。

---

## 一、 蓝牙配对与绑定（重要说明）

PS3 蓝牙手柄必须与主机的蓝牙 MAC 地址一致才能建立连接。我们的 `ps3` 驱动支持**两种绑定工作流**：

### 方式 1：免写手柄模式（最推荐，简单快捷）
通过让 ESP32 模拟手柄期望的 MAC 地址来建立连接。您不需要往手柄写入任何数据，只需**读取**即可：
1. 用 USB 数据线将 PS3 手柄连接电脑，打开 **SixaxisPairTool** 软件。
2. 软件会读取并显示手柄当前期望连接的 `Current Master` 地址（例如：`00:1a:7d:da:71:11`）。
3. 在 MicroPython 代码中，直接将这个 MAC 地址作为参数传入初始化函数：
   ```python
   ps3.init("00:1a:7d:da:71:11") # 填入手柄中读取到的 Current Master 地址
   ```
   *原理：底层驱动会自动调用 `esp_base_mac_addr_set`，将 ESP32 芯片的基准 MAC 地址修改为对应地址（减去 2），从而在软件层面伪装成手柄信任的蓝牙主机。*

### 方式 2：传统写入模式（`ps3.init()` 留空）
如果您希望保持 ESP32 的出厂 MAC 地址不变，可以通过工具向手柄写入 ESP32 的物理 MAC 地址：
1. 首先获取掌控板的物理蓝牙 MAC 地址（可以通过掌控板开机打印的信息，或在默认固件下用工具读取）。
2. 将手柄连接电脑，在 SixaxisPairTool 中的 `Change Master` 输入框中填入掌控板的物理 MAC 地址，点击 **Update** 写入手柄。
3. 断开连接。在 MicroPython 代码中，**留空**调用初始化函数即可：
   ```python
   ps3.init() # 留空，使用 ESP32 默认的物理 MAC 地址
   ```

---

## 二、 MicroPython API 参考说明

导入方式：
```python
import ps3
```

### 1. `ps3.init([mac_address_str])`
* **功能**：初始化蓝牙控制器与 Bluedroid 协议栈并开启 PS3 监听。
* **参数**：可选传入 MAC 地址字符串（如 `"20:00:00:01:01:66"`）。如果不传入，则默认使用当前芯片内置的 MAC。
* **返回**：`None`

### 2. `ps3.deinit()`
* **功能**：停止监听并关闭相关蓝牙连接服务。
* **返回**：`None`

### 3. `ps3.is_connected()`
* **功能**：检查当前是否有手柄处于连接激活状态。
* **返回**：`bool` (已连接返回 `True`，否则为 `False`)

### 4. `ps3.get_button(button_name)`
* **功能**：获取指定按键当前是否被按下。
* **参数**：按键名称字符串。支持的按键名字如下：
  * 方向键：`"up"`, `"down"`, `"left"`, `"right"`
  * 形状键：`"cross"` (X), `"circle"` (O), `"triangle"` (三角), `"square"` (方块)
  * 功能键：`"select"`, `"start"`, `"ps"`
  * 肩键/摇杆键：`"l1"`, `"r1"`, `"l2"`, `"r2"`, `"l3"` (左摇杆下压), `"r3"` (右摇杆下压)
* **返回**：`bool`

### 5. `ps3.get_analog(axis_name)`
* **功能**：获取摇杆坐标轴的偏移数值或模拟按键的下压深度。
* **参数**：轴向/模拟键名字。
  * **摇杆轴**（返回范围 `-128` 到 `127`）：`"lx"` (左摇杆X), `"ly"` (左摇杆Y), `"rx"` (右摇杆X), `"ry"` (右摇杆Y)。摇杆处于中心位置时返回 `0`。
  * **压力按键**（返回下压行程范围 `0` 到 `255`）：`"up"`, `"down"`, `"left"`, `"right"`, `"l1"`, `"r1"`, `"l2"`, `"r2"`, `"cross"`, `"circle"`, `"triangle"`, `"square"`。
* **返回**：`int`

### 6. `ps3.set_led(player_id)`
* **功能**：设置 PS3 手柄顶部的指示 LED 灯，常用于指示玩家序号。
* **参数**：整数 `1`、`2`、`3`、`4`（对应手柄上 4 个 LED 灯）。
* **返回**：`None`

### 7. `ps3.set_rumble(intensity, duration_ms)`
* **功能**：控制手柄内置的左右马达进行震动反馈。
* **参数**：
  * `intensity`：震动强度百分比，范围 `0` 到 `100`（0 代表关闭）。
  * `duration_ms`：持续时间（单位：毫秒）。如果传入 `-1`，则代表一直震动直到下一次修改。
* **返回**：`None`

---

## 三、 使用示例

我们在 [`G:\labplus-project\mpython-files\mpython\ps3_example.py`](file:///G:/labplus-project/mpython-files/mpython/ps3_example.py) 中存放了掌控板的完整图形屏交互例子。

您可以将该 `ps3_example.py` 烧录并作为 `main.py` 运行，来测试手柄按键与摇杆数据的获取效果。

---

## 四、 Mind+ 图形化积木与 MicroPython API 对应参考

为了方便在 Mind+ 中进行 Python 代码掌控板编程，以下是图形化积木与 `ps3` 驱动库 API 的直接对应关系表：

### 1. 手柄初始化积木
* **图形化积木**：`初始化PS3手柄，设置蓝牙配对码(冒号为英文状态): ["20:00:00:01:01:66"]`
* **Python API**：
  ```python
  ps3.init("20:00:00:01:01:66")
  ```

### 2. 获取 MAC 地址积木
* **图形化积木**：`获取ESP32主板的Mac地址`
* **Python API**：
  ```python
  import machine
  import ubinascii
  # 获取板子的 6 字节 MAC，并转换为 16 进制大写的 MAC 字符串
  mac_str = ":".join(["{:02X}".format(b) for b in machine.unique_id()])
  ```

### 3. 连接状态判断积木
* **图形化积木**：`ESP32是否连上PS3手柄?` (返回 `True`/`False`)
* **Python API**：
  ```python
  ps3.is_connected()
  ```

### 4. 按键状态判断积木
* **图形化积木**：`PS3手柄按键 [X键] 状态 [按下/放开]` (返回 `True`/`False`)
* **Python API**：
  * 检测**按下**（Pressed）：
    ```python
    ps3.get_button("cross")
    ```
  * 检测**放开**（Released）：
    ```python
    not ps3.get_button("cross")
    ```
  * *附：按键名称参数对应表*
    * **X键** -> `"cross"` | **O键** -> `"circle"` | **三角键** -> `"triangle"` | **方块键** -> `"square"`
    * **上键** -> `"up"` | **下键** -> `"down"` | **左键** -> `"left"` | **右键** -> `"right"`
    * **L1键** -> `"l1"` | **R1键** -> `"r1"` | **L2键** -> `"l2"` | **R2键** -> `"r2"`
    * **L3键** -> `"l3"` (左摇杆下压) | **R3键** -> `"r3"` (右摇杆下压)
    * **Select键** -> `"select"` | **Start键** -> `"start"` | **PS键** -> `"ps"`

### 5. 获取按键模拟压感值积木
* **图形化积木**：`获取PS3手柄按键 [X键] 的值` (返回数字 `0 ~ 255`)
* **Python API**：
  ```python
  ps3.get_analog("cross")
  ```

### 6. 摇杆数值读取积木
* **图形化积木**：`PS3手柄摇杆 [左侧X值]` (返回数字 `-128 ~ 127`)
* **Python API**：
  * **左侧X值** (Left Stick X) -> `ps3.get_analog("lx")`
  * **左侧Y值** (Left Stick Y) -> `ps3.get_analog("ly")`
  * **右侧X值** (Right Stick X) -> `ps3.get_analog("rx")`
  * **右侧Y值** (Right Stick Y) -> `ps3.get_analog("ry")`

### 7. 手柄震动与指示灯积木 (扩展)
* **设置手柄 LED 灯**：`设置PS3手柄LED为 [LED 1]` (参数支持 `1` 到 `4`)
  ```python
  ps3.set_led(1)
  ```
* **控制手柄震动**：`设置PS3手柄震动强度为 [60]%, 持续 [500] 毫秒` (强度范围 `0-100`，持续时间单位为 ms)
  ```python
  ps3.set_rumble(60, 500)
  ```
