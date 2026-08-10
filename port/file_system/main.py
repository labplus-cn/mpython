from mpython import oled
import uos

# 获取固件日期 (从 uname version 中解析，形如 "v2.6.1-31-g1a19d5f on 2026-08-10")
try:
    ver = uos.uname().version
    date_idx = ver.find("on ")
    fw_date = ver[date_idx + 3:date_idx + 13] if date_idx != -1 else "Unknown"
except Exception:
    fw_date = "Unknown"

# 获取文件系统打包日期
try:
    with open("build_date.txt", "r") as f:
        fs_date = f.read().strip()
except Exception:
    fs_date = "Unknown"

oled.fill(0)
oled.DispChar(" \u56fa\u4ef6\u65e5\u671f: %s" % fw_date, 0, 16, 1)
oled.DispChar(" \u6587\u4ef6\u7cfb\u7edf: %s" % fs_date, 0, 32, 1)
oled.show()
