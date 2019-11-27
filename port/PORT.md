为方便项目管理，做以下变更。
1、新建项目文件夹，如mpython mpython-classroom-kit
2、复制需要修改的跟编译相关的文件到项目文件夹：
   port/esp32/boards
   port/esp32/modules
   port/esp32/Makefile
   port/esp32/makeimg.py
   port/esp32/mpconfigport.h
   port/esp32/partitions.csv
   port/esp32/qstrdefsport.h
3、修改跟路径相关的信息：
   Makefile
    include ../../py/mkenv.mk 改为 include ../micropython/py/mkenv.mk
    FLASH_SIZE ?= 4MB 改为 FLASH_SIZE ?= 8MB
    添加 INC += -I$(TOP)/ports/esp32
    修改SRC路径：
    SRC_C = $(addprefix ports/esp32/,\
    ）
编译测试

4、加入idf http tls相关支持：
   加一个板，BOARD ?= GENERIC_CLASSROOM_KIT， 需在boards下加一个文件夹

   INC_ESPCOMP += -I$(ESPCOMP)/lwip/lwip/src/include/lwip
   INC_ESPCOMP += -I$(ESPCOMP)/nghttp/port/include
   INC_ESPCOMP += -I$(ESPCOMP)/nghttp/nghttp2/lib/includes
   #		esp_http_client
   INC_ESPCOMP += -I$(ESPCOMP)/esp_http_client/include
   INC_ESPCOMP += -I$(ESPCOMP)/esp_http_client/lib/include
   #		tcp_transport
   INC_ESPCOMP += -I$(ESPCOMP)/tcp_transport/include
   INC_ESPCOMP += -I$(ESPCOMP)/tcp_transport/private_include
   #		esp_tls
   INC_ESPCOMP += -I$(ESPCOMP)/esp-tls
   INC_ESPCOMP += -I$(ESPCOMP)/esp-tls/private_include
   －－－－－－－
   ESPIDF_NGHTTP_O = $(patsubst %.c,%.o, $(wildcard $(ESPCOMP)/nghttp/port/*.c)) 
   ESPIDF_ESP_HTTP_CLIENT_O = \
	$(patsubst %.c,%.o, $(wildcard $(ESPCOMP)/esp_http_client/*.c)) \
	$(patsubst %.c,%.o, $(wildcard $(ESPCOMP)/esp_http_client/lib/*.c)) 
   ESPIDF_TCP_TRANSPORT_O = $(patsubst %.c,%.o, $(wildcard $(ESPCOMP)/tcp_transport/*.c)) 
   ESPIDF_ESP_TLS_O = $(addprefix $(ESPCOMP)/esp-tls/, esp_tls.o)
   －－－－－－
   $(eval $(call gen_espidf_lib_rule,nghttp,$(ESPIDF_NGHTTP_O)))
   $(eval $(call gen_espidf_lib_rule,esp_http_client,$(ESPIDF_ESP_HTTP_CLIENT_O)))
   $(eval $(call gen_espidf_lib_rule,tcp_transport,$(ESPIDF_TCP_TRANSPORT_O)))
   $(eval $(call gen_espidf_lib_rule,esp-tls,$(ESPIDF_ESP_TLS_O)))

编译测试

5、加入新境特性
   # mpython audio module includes (by jch)
   INC += -I src
   INC += -I src/codec/codec_lib/helix/include
   INC += -I src/codec/decoder/include
   INC += -I src/codec/include
   －－－－－－
   CFLAGS += -DARM -DCONFIG_AUDIO_HELIX    # 避免编译音频库出错
   CFLAGS += -Wno-unused-but-set-variable
   －－－－－－
   port/esp32 中需要修改的源文件提取出来。重定义编译路径：
   SRC_C += src/main.c 
   SRC_C += src/modmusic.c 
   SRC_C += src/modmusictunes.c 
   SRC_C += src/modradio.c 
   SRC_C += src/machine_servo_pwm.c 
   SRC_C += src/modnetwork.c 
   SRC_C += src/machine_pin.c
   SRC_C += src/machine_touchpad.c 
   －－－－－－
   新增功能源文件
   # 开机显示和异常打印功能模块
   STARTUP_SRC_C = $(addprefix src/startup/, \
      oled.c \
      i2c_master.c \
      panic.c \
      startup.c \
      )
   # 音频功能模块
   CODEC_SRC_C = $(addprefix src/codec/,\
      modcodec.c \
      http_client.c \
      audio_player.c \
      audio_renderer.c \
      url_codec.c \
      local_file.c \
      audio_recorder.c \
      wav_head.c \
      codec_lib/helix/src/bitstream.c \
      codec_lib/helix/src/buffers.c \
      codec_lib/helix/src/dct32.c \
      codec_lib/helix/src/dequant.c \
      codec_lib/helix/src/dqchan.c \
      codec_lib/helix/src/huffman.c \
      codec_lib/helix/src/hufftabs.c \
      codec_lib/helix/src/imdct.c \
      codec_lib/helix/src/mp3dec.c \
      codec_lib/helix/src/mp3tabs.c \
      codec_lib/helix/src/polyphase.c \
      codec_lib/helix/src/scalfact.c \
      codec_lib/helix/src/stproc.c \
      codec_lib/helix/src/subband.c \
      codec_lib/helix/src/trigtabs.c \
      decoder/helix_mp3_decoder.c \
      )
      －－－－－－－
      OBJ_MP += $(addprefix $(BUILD)/, $(STARTUP_SRC_C:.c=.o))
      OBJ_MP += $(addprefix $(BUILD)/, $(CODEC_SRC_C:.c=.o))
      OBJ_MP += $(addprefix $(BUILD)/, $(BLUETOOTH_SRC_C:.c=.o))
6、修改mpconfigport.h

7、修改qstrdefsport.h
   
6、增加编译配置：
   .PHONY: idf-version deploy font erase

