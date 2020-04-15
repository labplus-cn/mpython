--------------------------------
|  2019.02.10 构建codec框架  |
--------------------------------
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

		INC_ESPCOMP += -I$(ESPCOMP)/esp_http_client/include

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

---------------------------------------------------
|  2019.03.13 helix解码存问题，改成libmad试试, 测试有|
|  问题，有时间再试                                 |
---------------------------------------------------
1. codec文件夹结构：
  codec
	|--codec_lib    //解码库
	|  |--helix
	|     |--include
	|     |--src
	|     |--readme.md
	|--decoder     //解码任务
	|  |--include
	|  |  |--helix_decodec.h
	|  |--helix_mp3_decoder.c
	|--include 
	|  |--audio_play.h
	|  |--audio_render.h
	|  |--board.h
	|  |--modcodec.h
	|  |--wav_head.h
	|--audio_play.c    //播放任务
	|--audio_render.c  //i2s dac设置
	|--http_client.c   //http客户端请求回应
	|--modcodec.c      //python模块
	|--readme.md       //本文档

	2.Makefile修改
	  1) esp-idf加入http_client支持
			ESPIDF_ESP_HTTP_CLIENT_O = $(addprefix $(ESPCOMP)/esp_http_client/,\
				esp_http_client.o \
				lib/http_auth.o \
				lib/http_header.o \
				lib/http_utils.o \
				lib/transport_ssl.o \
				lib/transport_tcp.o \
				lib/transport.o \
			)

		  OBJ_ESPIDF += $(addprefix $(BUILD)/, $(ESPIDF_ESP_HTTP_CLIENT_O))

			INC_ESPCOMP += -I$(ESPCOMP)/esp_http_client/include
			INC_ESPCOMP += -I$(ESPCOMP)/esp_http_client/lib/include
		2) 添加：
			CODEC_SRC_C = $(addprefix codec/,\
					audio_player.c \
					audio_renderer.c \
					http_client.c \
					modcodec.c \
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

			OBJ_MP += $(addprefix $(BUILD)/, $(CODEC_SRC_C:.c=.o))

			SRC_QSTR += $(SRC_C) $(EXTMOD_SRC_C) $(LIB_SRC_C) $(DRIVERS_SRC_C)改为：
			SRC_QSTR += $(SRC_C) $(EXTMOD_SRC_C) $(LIB_SRC_C) $(DRIVERS_SRC_C) $(CODEC_SRC_C)
			
			INC += -I$(TOP)/ports/esp32/codec/codec_lib/helix/include
			INC += -I$(TOP)/ports/esp32/codec/decoder/include
			INC += -I$(TOP)/ports/esp32/codec/include

			在 ESPIDF_DRIVER_O = $(addprefix $(ESPCOMP)/driver/,\ 下加入
     		i2s.o \

		  添加：
			CFLAGS += -DARM -DCONFIG_AUDIO_HELIX
			CFLAGS += -Wno-unused-but-set-variable

	  3) 修改mpconfigport.h
  		 加入模块mp_module_codec

----------------------------------
|  重新构建codec框架               |
|  采用helix做mp3解码库            |
----------------------------------
2019.03.10 

1. codec文件夹结构：
  codec
	|--codec_lib    //解码库，存放各解码库
	|  |--helix
	|     |--include
	|     |--src
	|     |--readme.md
	|--decoder     //解码任务
	|  |--include
	|  |  |--helix_decodec.h
	|  |--helix_mp3_decoder.c
	|--include 
	|  |--audio_play.h
	|  |--audio_render.h  
	|  |--board.h
	|  |--http_client.h  
	|  |--local_play.h  
	|  |--modcodec.h
	|  |--urlcodec.h
	|  |--wav_head.h
	|--audio_play.c    //播放任务
	|--audio_render.c  //i2s dac设置
	|--http_client.c   //网络音频获取
	|==local_file.c    //本地音频读写
	|--modcodec.c      //python模块
	|--readme.md       //本文档
	|--urlcodec.c

	2.Makefile修改
	  1) esp-idf加入http_client支持
			ESPIDF_ESP_HTTP_CLIENT_O = $(addprefix $(ESPCOMP)/esp_http_client/,\
				esp_http_client.o \
				lib/http_auth.o \
				lib/http_header.o \
				lib/http_utils.o \
				lib/transport_ssl.o \
				lib/transport_tcp.o \
				lib/transport.o \
			)

		  OBJ_ESPIDF += $(addprefix $(BUILD)/, $(ESPIDF_ESP_HTTP_CLIENT_O))

			INC_ESPCOMP += -I$(ESPCOMP)/esp_http_client/include
			INC_ESPCOMP += -I$(ESPCOMP)/esp_http_client/lib/include
		2) 添加：
			CODEC_SRC_C = $(addprefix codec/,\
					audio_player.c \
					audio_renderer.c \
					http_client.c \
					modcodec.c \
					local_file.c \
					urlcodec.c \
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

			OBJ_MP += $(addprefix $(BUILD)/, $(CODEC_SRC_C:.c=.o))

			SRC_QSTR += $(SRC_C) $(EXTMOD_SRC_C) $(LIB_SRC_C) $(DRIVERS_SRC_C)改为：
			SRC_QSTR += $(SRC_C) $(EXTMOD_SRC_C) $(LIB_SRC_C) $(DRIVERS_SRC_C) $(CODEC_SRC_C)
			
			INC += -I$(TOP)/ports/esp32/codec/codec_lib/helix/include
			INC += -I$(TOP)/ports/esp32/codec/decoder/include
			INC += -I$(TOP)/ports/esp32/codec/include

			在 ESPIDF_DRIVER_O = $(addprefix $(ESPCOMP)/driver/,\ 下加入
     		i2s.o \

		  添加：
			CFLAGS += -DARM -DCONFIG_AUDIO_HELIX
			CFLAGS += -Wno-unused-but-set-variable

	  3) 修改mpconfigport.h
  		 加入模块mp_module_codec

2019.03.20
codec-v2.3-helix

1. 修改player,


2. 修正对total_read_len的处理，body中的数据都要计入content-lenght, 而不仅是mp3数据，之前有误。
   修改：proccess_tag()
   
	 修改：http_request_task()中对total_read_len的处理：
	  while() 改为 while(1)
		修正while()中对total_read_len的处理，注意读数据时不要超过content-lenght

3. 增加对respone的文本处理
	typedef enum
	{
			MIME_UNKNOWN = 1, OCTET_STREAM, AUDIO_AAC, AUDIO_MP4, AUDIO_MPEG, AUDIO_TEXT //增加AUDIO_TEXT，用于处理respone文本.
	} content_type_t;
  
	_http_event_handler() 加入：
	  else if (strcmp(evt->header_value, "text/plain") == 0) http_param_instance->content_type = AUDIO_TEXT;
	修改http_request_task(),实现对文本和音频的分别处理。

2019.03.20
codec-v2.4-helix

1. 把读音频文件的操作放到固件层
   增加local_file.c/h文件，修改makefile加入此文件编译。
	 player里加成员
	 mp_reader_t *reader;
	 audio_type_t file_type;
	 修改audio_play.c中对本地文件的处理。
	 暂用函数调用的方式实现，任务方式会出现堆栈溢出，原因未明。

2.

2019.03.21
codec-v2.5-helix

试图把web tts做到底层
1. player里加成员
	HTTP_HEAD_VAL *http_head;
	char *http_body;
	int http_body_len;
	esp_http_client_method_t http_method;

2. 修改modecodec.c
   codec_play()添加：
		player->http_head = NULL;                    
		player->http_body = NULL;    
		player->http_method = HTTP_METHOD_GET; 


3. 修改http_client.c
   加入：
		esp_err_t _http_event_handler(esp_http_client_event_t *evt)
		{
			...
				else if (strcmp(evt->header_value, "text/plain") == 0) http_param_instance->content_type = AUDIO_TEXT;
			...
		}
	
	void http_request_task(void *pvParameters)加入：
	    .method = player->http_method,
			...
			if(player->http_head != NULL){
        for(int i = 0; i < 6; i++)
            esp_http_client_set_header(client, player->http_head[i].key, player->http_head[i].value);
    	}
			...
			if ((err = esp_http_client_open(client, 0)) != ESP_OK)  改为：
			if ((err = esp_http_client_open(client, player->http_body_len)) != ESP_OK) {
			...
			if(player->http_body != NULL && player->http_body_len > 0){
        esp_http_client_write(client, player->http_body, player->http_body_len);
    	}
			...


	modcodec.c中构建函数
	 codec_webtts()

2019.03.22
codec-v2.5-helix-2019-03-22.tar.xz

1. 增加分配给urlencode编码时的缓存大小，避免溢出。
2. helix-mp3_decode()播放结束判断做修改，避免最后一小段音频不能播放。
			if((player->eof || player->player_status == STOPPED) && (ringBufRemainBytes == 0) && (bytesLeft == 0)){
			renderer_zero_dma_buffer();
			break;
	
	mp3解码结束后，做点延时。
3. 
发布版相对之胶beta版改进：。
	功能改进：
	1、播放稳定性增加
	2.  播放本地文件时，文件的读操作在固件层完成。
	3.  web tts的urlencode在固件层完成，避免加载一大堆python库
	4.  解决tts不能播放后面最后几个词语问题。
	5. 音质有所改善。
	6. 网络音频数据获取，放底层。
  尚存在的问题：
     1.播放一首歌后不能接着播放下一首。须复位掌控板，尚未找到原因。
     2.扩展板音质还有待继续增强，正请购几个喇叭测试。

2019.03.23
codec-v2.5.1-helix-2019-03-23.tar.xz(发布版)

1. 去掉renderer.c中状态量renderer_status，renderer同步播放器状态。
2. 修改local file读代码。
3. 重写mp3_decode.c代码。
4. 解决需要复位才能播放下一首歌的问题: renderer初始化时调用了i2s_sopt(),用户代码初始化时须在相关位置调用audio_player_start()。

2019.03.23
codec-v2.5.1-helix-2019-03-23.tar.xz(发布版)

1. 重写http_client代码。
2. 加入stop pause resume模块函数。
3. 去掉一些不必要的player结构成员
4. 调整任务优先级：ESP_TASK_PRIO_MIN + 1 使播放指令可得到执行
5. 通过对mp3_decode_t结构成员赋初始值samplerate = 44100的方式解决stop或播放下一首歌时samplerate不对导致变调的问题。
6. 后续看情况调整任务堆栈、ring buffer大小，现在任务的切换和同步用的是延时方式，延时大小要调好，后续用事件组。

2019.03.25
codec-v2.5.1-helix-2019-03-23.tar.xz(发布版)
1. 添加音量控制。
2. 修改解码后output值算法。
3. 增加播放状态查询。
4. 修正http_head定义为局部变量时，导致player成员http_head会指向未知位置，导致系统复位。

2019.03.30
github分支提交
1. 完成固件层对webtts http client head处理，简化用户层面工作。
2. 增加player_init()和player_deinit(),实现播放器初始化和资源释放。
3. 修正一些bug.
4. 更改用户接口层函数名。
5. 完善出错处理。
6. 把对mp3tag处理从http_client移到mp3解码任务,使http_client只处理跟网络相关事务。

2019.05.15
添加录音模块
   增加audio_recorder.h/c源文件
	 增加以下python层面指令：
	 recorder_init
	 recorder_deinit
	 soundness
	 record
	 xunfei_iat_config
	 xunfie_iat

2019.06.05
  1 添加播放WAV文件
	2、添加录音功能
	3、支持讯飞iat
	4、修改异常处理。

1. codec文件夹结构：
  codec
	|--codec_lib    //解码库，存放各解码库
	|  |--helix
	|     |--include
	|     |--src
	|     |--readme.md
	|--decoder     //解码任务
	|  |--include
	|  |  |--helix_decodec.h
	|  |--helix_mp3_decoder.c
	|--include 
	|  |--audio_play.h
	|  |--audio_render.h  
	|  |--board.h
	|  |--http_client.h  
	|  |--local_play.h  
	|  |--modcodec.h
	|  |--urlcodec.h
	|  |--wav_head.h
	|  |--audio_recocrder.h
	|--audio_play.c    //播放任务
	|--audio_render.c  //i2s dac设置
	|--http_client.c   //网络音频获取
	|--local_file.c    //本地音频读写
	|--modcodec.c      //python模块
	|--readme.md       //本文档
	|--urlcodec.c
	|--wav_head.c
	|--audio_recorder.c
2019.06.22
test

2020.04.13
调整codec模块
1、升级到IDF4及新的项目框架后，需处理不同项目可能使用内置ADC/DAC外置CODEC解码芯片
改动：
1、audio_renderer.c
   修改init_i2s()：
     communication_format内置和外置的配置是不一样的。
	 内、外置的引脚，ADC/DAC配置不一样。

2、audio_recorder.c
	采样率调整为8000，减少数据量。
	内置需enable dac。
	内置需对采样数据做处理。

3、 local_play.c helix_mp3_decoder.c
    内置DAC需把音频数据转为正数，且加入音量处理。

2020.04.13
es8388驱动以c代码实现，解音量控制问题。
1、修改makefile加入对es8388.c/h编译。
2、修改modcodec.c，加入es8388 init/deinit
3、mpython-classroom-kit下面的的mpython.py注释掉es8388 python驱动实例化。