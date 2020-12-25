// Copyright 2018 Espressif Systems (Shanghai) PTE LTD
// All rights reserved.

#include "wave_head.h"

#ifdef __cplusplus
extern "C" {
#endif

esp_err_t wav_head_parser(const uint8_t *inData, wav_info_t *info)
{
    info->audioFormat = inData[20];           // format;0X01,linear PCM;0X11 IMA ADPCM
    info->channels = inData[22];             // Number of channel;1: 1 channel;2: 2 channels;
    info->blockAlign = inData[40];            // align
    //info->dataSize = inData[32];              // size of data
    //info->totSec = inData[14];               // total time,second
    //info->curSec = inData[14];               // current time, second
    info->bitRate = (((uint32_t)inData[31]) << 24) + (((uint32_t)inData[30]) << 16) + (((uint32_t)inData[29]) << 8) + inData[28];               // bit sample rate
    info->sampleRate = (((uint32_t)inData[27]) << 24) + (((uint32_t)inData[26]) << 16) + (((uint32_t)inData[25]) << 8) + inData[24];            // sample rate
    info->bits = inData[34];                   // bit length 16bit,24bit,32bit
    info->dataShift = 12 + 8 + inData[16] + 8;             // Data shift.
    info->fmtSubchunckSize = inData[16];

    return ESP_OK;
}

void wav_head_init(wav_header_t *wavhead, int sample_ate, int bits, int channels, uint32_t dataSize)
{
    wavhead->riff.ChunkID = 0X46464952;
    wavhead->riff.ChunkSize = 36 + dataSize;
    wavhead->riff.Format = 0X45564157;

    wavhead->fmt.ChunkID = 0X20746D66;
    wavhead->fmt.ChunkSize = 0x10;        //Size of this fmt block (Not include ID and Size);16 or 18 or 40 bytes.
    wavhead->fmt.AudioFormat = 0x01;       //Format;0X01:linear PCM;0X11:IMA ADPCM
    wavhead->fmt.NumOfChannels = channels;     //Number of channel;1: 1 channel;2: 2 channels;
    wavhead->fmt.SampleRate = sample_ate;        //sample rate;0X1F40 = 8Khz
    wavhead->fmt.ByteRate = (sample_ate*bits*channels)/8;          //Byte rate;
    wavhead->fmt.BlockAlign = (bits*channels)/8;        //align with byte;
    wavhead->fmt.BitsPerSample = bits;     // Bit lenght per sample point,4 ADPCM
//  wavhead->fmt.ByteExtraData;     // Exclude in linear PCM format(0~22)
    wavhead->data.ChunkID = 0X61746164;
    wavhead->data.ChunkSize = dataSize;
}

void wav_head_size(wav_header_t *wavhead, uint32_t dataSize)
{
    wavhead->riff.ChunkSize = 36 + dataSize;
    wavhead->data.ChunkSize = dataSize;
}

#ifdef __cplusplus
}
#endif

