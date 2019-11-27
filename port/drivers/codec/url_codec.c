/*
 * url_codec.c
 *
 *  Created on: 2019.02.03
 *      Author: zhaohuijiang
 */

#include <stdio.h>
//#include <stdlib.h>
#include <string.h>
//#include <ctype.h>

#include "esp_system.h"
#include "esp_log.h"

#define TAG "url codec"
 
#define BURSIZE 2048
 
static int hex2dec(char c)
{
    if ('0' <= c && c <= '9') 
        return c - '0';
    else if ('a' <= c && c <= 'f')
        return c - 'a' + 10;
    else if ('A' <= c && c <= 'F')
        return c - 'A' + 10;
    else
        return -1;
}
 
static char dec2hex(short int c)
{
    if (0 <= c && c <= 9) 
        return c + '0';
    else if (10 <= c && c <= 15) 
        return c + 'A' - 10;
    else
        return -1;
}
 
//编码一个url  
void urlencode(char *src, char *des)
{
    int i = 0;
    int len = strlen(src);
    int res_len = 0;
    
    for (i = 0; i < len; ++i) 
    {
        char c = src[i];
        if (    ('0' <= c && c <= '9') ||
                ('a' <= c && c <= 'z') ||
                ('A' <= c && c <= 'Z') || 
                c == '/' || c == '.' || c=='=' || c=='&') 
        {
            des[res_len++] = c;
        } 
        else if (c==' ')
        {
            des[res_len++] = '+';
        }
        else
        {
            // ESP_LOGE(TAG, "position: %d", i);
            int j = (short int)c;
            if (j < 0)
                j += 256;
            int i1, i0;
            i1 = j / 16;
            i0 = j - i1 * 16;
            des[res_len++] = '%';
            des[res_len++] = dec2hex(i1);
            des[res_len++] = dec2hex(i0);
        }
    }
   des[res_len] = '\0';
}

// void urlencode(char *src, char *des) 
// {
//     char *p = src;
//     char *tp = des;

//     for (; *p; p++) 
//     {
//         if ((*p > 0x00 && *p < ',') ||
//                 (*p > '9' && *p < 'A') ||
//                 (*p > 'Z' && *p < '_') ||
//                 (*p > '_' && *p < 'a') ||
//                 (*p > 'z' && *p < 0xA1)) 
//         {
//             sprintf((char *)tp, "%%%02X", *p);
//             tp += 3; 
//         } 
//         else 
//         {
//             *tp = *p;
//             tp++;
//         }
//     }

//     *tp='\0';
// }
 
// 解码url
void urldecode(char *src, char *des)
{
    int i = 0;
    int len = strlen(src);
    int res_len = 0;

    for (i = 0; i < len; ++i) 
    {
        char c = src[i];
        if (c != '%') 
        {
            des[res_len++] = c;
        }
        else
        {
            char c1 = src[++i];
            char c0 = src[++i];
            int num = 0;
            num = hex2dec(c1) * 16 + hex2dec(c0);
            des[res_len++] = num;
        }
    }
    des[res_len] = '\0';
}
 
/* test 
int main(int argc, char *argv[])
{
    char url[100] = "二份";
    urlencode(url); //编码后
    printf("%s\n", url);
    <br>　　//char buf[100] = "%E4%BA%8C%E4%BB%BD";　　//当使用utf-8编码时　　"二份"解码出来为此
    char buf[100] = "%B6%FE%B7%DD";　　　　　　//当使用gb2312编码时   "二份"解码出来为此
    urldecode(buf); //解码后
    printf("%s\n", buf);
 
    return 0;
} */