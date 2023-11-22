#!/bin/bash
idf.py clean 
wait
idf.py build
wait

idf.py -D MICROPY_BOARD=GENERIC  -DUSER_C_MODULES=/home/labplus/esp/mpython/port/usercmodule/micropython.cmake build

