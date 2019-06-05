// Copyright 2018 Espressif Systems (Shanghai) PTE LTD
// All rights reserved.

#ifndef _WAV_HEADER_H_
#define _WAV_HEADER_H_

#include "esp_err.h"

#ifdef __cplusplus
extern "C" {
#endif

//RIFF block
typedef struct {
    uint32_t ChunkID;               //chunk id;"RIFF",0X46464952
    uint32_t ChunkSize ;            // file length - 8
    uint32_t Format;                //WAVE,0X45564157
} ChunkRIFF ;

//fmt block
typedef struct {
    uint32_t ChunkID;           //chunk id;"fmt ",0X20746D66
    uint32_t ChunkSize ;        //Size of this fmt block (Not include ID and Size);16 or 18 or 40 bytes.
    uint16_t AudioFormat;       //Format;0X01:linear PCM;0X11:IMA ADPCM
    uint16_t NumOfChannels;     //Number of channel;1: 1 channel;2: 2 channels;
    uint32_t SampleRate;        //sample rate;0X1F40 = 8Khz
    uint32_t ByteRate;          //Byte rate;
    uint16_t BlockAlign;        //align with byte;
    uint16_t BitsPerSample;     // Bit lenght per sample point,4 ADPCM
//  uint16_t ByteExtraData;     // Exclude in linear PCM format(0~22)
} __attribute__((packed)) ChunkFMT;

//fact block
typedef struct {
    uint32_t ChunkID;           //chunk id;"fact",0X74636166;
    uint32_t ChunkSize ;        //Size(Not include ID and Size);4 byte
    uint32_t NumOfSamples;      //number of sample
} __attribute__((packed)) ChunkFACT;

//LIST block
typedef struct {
    uint32_t ChunkID;            //chunk id 0X5453494C;
    uint32_t ChunkSize;          // Size
} __attribute__((packed)) ChunkLIST;

//PEAK block
typedef struct {
    uint32_t ChunkID;            //chunk id; 0X4B414550
    uint32_t ChunkSize;          //Size
} __attribute__((packed)) ChunkPeak;

//data block
typedef struct {
    uint32_t ChunkID;           //chunk id;"data",0X5453494C
    uint32_t ChunkSize ;        //Size of data block(Not include ID and Size)
} __attribute__((packed)) ChunkDATA;

//wav block
typedef struct {
    ChunkRIFF riff; //riff
    ChunkFMT fmt;   //fmt
//  ChunkFACT fact; //fact,Exclude in linear PCM format
    ChunkDATA data; //data
} __attribute__((packed)) wav_header_t;

//wav control struct
typedef struct {
    uint16_t audioFormat;           // format;0X01,linear PCM;0X11 IMA ADPCM
    uint16_t channels;             // Number of channel;1: 1 channel;2: 2 channels;
    uint16_t blockAlign;            // align
    uint32_t dataSize;              // size of data

    uint32_t totSec;               // total time,second
    uint32_t curSec;               // current time, second

    uint32_t bitRate;               // bit sample rate
    uint32_t sampleRate;            // sample rate
    uint16_t bits;                   // bit length 16bit,24bit,32bit

    uint32_t dataShift;             // Data shift.
    uint32_t fmtSubchunckSize;
} __attribute__((packed)) wav_info_t;

esp_err_t wav_head_parser(const uint8_t *inData, wav_info_t *info);
void wav_head_init(wav_header_t *wavhead, int sample_ate, int bits, int channels, uint32_t dataSize);
void wav_head_size(wav_header_t *wavhead, uint32_t dataSize);

#ifdef __cplusplus
}
#endif

#endif
