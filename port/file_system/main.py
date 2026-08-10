from mpython import oled

oled.fill(0)
oled.DispChar(" \u56fa\u4ef6\u65e5\u671f: 2026-08-10", 0, 16, 1)
# oled.DispChar(" \u6587\u4ef6\u7cfb\u7edf: 2026-05-29", 0, 32, 1)
oled.DispChar("Ps3Controller", 0, 32, 1)
oled.show()
