/home/labplus/.espressif/python_env/idf4.4_py3.6_env/bin/python release.py build/bootloader/bootloader.bin build/partition_table/partition-table.bin build/labplus.bin ./Noto_Sans_CJK_SC_Light16.bin ./esp32.bin
wait
/home/labplus/.espressif/python_env/idf4.4_py3.6_env/bin/python ../esp-idf/components/esptool_py/esptool/esptool.py -p /dev/ttyUSB0 -b 460800 --before default_reset --after hard_reset --chip esp32  write_flash  0 ./esp32.bin
