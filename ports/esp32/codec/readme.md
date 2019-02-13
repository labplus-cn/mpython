1、esp32新增文件夹，放增加的源文件。
    新增的源文件：
    wav_head.h
    modcodec.h/c
		wav_head.h
		helix/*.h/c 


2、修改Makefile:
  1) 添加：
		CODEC_SRC_C = $(addprefix codec/,\
				modcodec.c \
				helix/src/bitstream.c \
				helix/src/buffers.c \
				helix/src/dct32.c \
				helix/src/dequant.c \
				helix/src/dqchan.c \
				helix/src/huffman.c \
				helix/src/hufftabs.c \
				helix/src/imdct.c \
				helix/src/mp3dec.c \
				helix/src/mp3tabs.c \
				helix/src/polyphase.c \
				helix/src/scalfact.c \
				helix/src/stproc.c \
				helix/src/subband.c \
				helix/src/trigtabs.c \
			)
		
		OBJ_MP += $(addprefix $(BUILD)/, $(CODEC_SRC_C:.c=.o))

		SRC_QSTR += $(SRC_C) $(EXTMOD_SRC_C) $(LIB_SRC_C) $(DRIVERS_SRC_C)改为：
		SRC_QSTR += $(SRC_C) $(EXTMOD_SRC_C) $(LIB_SRC_C) $(DRIVERS_SRC_C) $(CODEC_SRC_C)
     
  2) 在 ESPIDF_DRIVER_O = $(addprefix $(ESPCOMP)/driver/,\ 下加入
     i2s.o \

	3) 添加：
		CFLAGS += -DARM -DCONFIG_AUDIO_HELIX
		CFLAGS += -Wno-unused-but-set-variable

		INC += -I$(TOP)/ports/esp32/codec/helix/include

3、修改mpconfigport.h
  加入模块mp_module_codec

mp3解码支持



    