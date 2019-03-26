helix mp3解码库使用

1. 初始化
    HMP3Decoder hMP3Decoder;
    hMP3Decoder = MP3InitDecoder();
    初始化会动态分配内存给解码器，约占用内存：
2. 解码