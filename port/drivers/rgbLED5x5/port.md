1、创建源文件夹rgbLED5x5及驱动源文件源文件
2、builtin/下创建模块文件 modrgbLED5x5
2、board/mpython-classroom-kit/mpconfigboard.h添加模块及GC内存管理变量。
3、makefile中添加头文件包含及源文件编译
4、main.c中添加延时函数。