/* ***** BEGIN LICENSE BLOCK ***** 
 * Version: RCSL 1.0/RPSL 1.0 
 *  
 * Portions Copyright (c) 1995-2002 RealNetworks, Inc. All Rights Reserved. 
 *      
 * The contents of this file, and the files included with this file, are 
 * subject to the current version of the RealNetworks Public Source License 
 * Version 1.0 (the "RPSL") available at 
 * http://www.helixcommunity.org/content/rpsl unless you have licensed 
 * the file under the RealNetworks Community Source License Version 1.0 
 * (the "RCSL") available at http://www.helixcommunity.org/content/rcsl, 
 * in which case the RCSL will apply. You may also obtain the license terms 
 * directly from RealNetworks.  You may not use this file except in 
 * compliance with the RPSL or, if you have a valid RCSL with RealNetworks 
 * applicable to this file, the RCSL.  Please see the applicable RPSL or 
 * RCSL for the rights, obligations and limitations governing use of the 
 * contents of the file.  
 *  
 * This file is part of the Helix DNA Technology. RealNetworks is the 
 * developer of the Original Code and owns the copyrights in the portions 
 * it created. 
 *  
 * This file, and the files included with this file, is distributed and made 
 * available on an 'AS IS' basis, WITHOUT WARRANTY OF ANY KIND, EITHER 
 * EXPRESS OR IMPLIED, AND REALNETWORKS HEREBY DISCLAIMS ALL SUCH WARRANTIES, 
 * INCLUDING WITHOUT LIMITATION, ANY WARRANTIES OF MERCHANTABILITY, FITNESS 
 * FOR A PARTICULAR PURPOSE, QUIET ENJOYMENT OR NON-INFRINGEMENT. 
 * 
 * Technology Compatibility Kit Test Suite(s) Location: 
 *    http://www.helixcommunity.org/content/tck 
 * 
 * Contributor(s): 
 *  
 * ***** END LICENSE BLOCK ***** */ 

/**************************************************************************************
 * Fixed-point MP3 decoder
 * Jon Recker (jrecker@real.com), Ken Cooke (kenc@real.com)
 * June 2003
 *
 * buffers.c - allocation and freeing of internal MP3 decoder buffers
 *
 * All memory allocation for the codec is done in this file, so if you don't want 
 *  to use other the default system malloc() and free() for heap management this is 
 *  the only file you'll need to change.
 **************************************************************************************/

// J.Sz. 21/04/2006 #include "hlxclib/stdlib.h"		/* for malloc, free */ 
#include "py/mphal.h"
#include "py/obj.h"
#include "py/runtime.h"
#include "py/objstr.h"

#include "stdlib.h" // J.Sz. 21/04/2006
#include "coder.h"
#include "esp_log.h"
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "esp_system.h"
// static const char *TAG = "buffer";

#define mp3_DecInfo	    MP_STATE_PORT(mp3DecInfo)
#define fh	        MP_STATE_PORT(fh)
#define si      	MP_STATE_PORT(si)
#define sfi	        MP_STATE_PORT(sfi)
#define hi	        MP_STATE_PORT(hi)
#define di	        MP_STATE_PORT(di)
#define mi	        MP_STATE_PORT(mi)
#define sbi	        MP_STATE_PORT(sbi)

/**************************************************************************************
 * Function:    ClearBuffer
 *
 * Description: fill buffer with 0's
 *
 * Inputs:      pointer to buffer
 *              number of bytes to fill with 0
 *
 * Outputs:     cleared buffer
 *
 * Return:      none
 *
 * Notes:       slow, platform-independent equivalent to memset(buf, 0, nBytes)
 **************************************************************************************/
// static void ClearBuffer(void *buf, int nBytes)
// {
// 	int i;
// 	unsigned char *cbuf = (unsigned char *)buf;

// 	for (i = 0; i < nBytes; i++)
// 		cbuf[i] = 0;

// 	return;
// }

/**************************************************************************************
 * Function:    AllocateBuffers
 *
 * Description: allocate all the memory needed for the MP3 decoder
 *
 * Inputs:      none
 *
 * Outputs:     none
 *
 * Return:      pointer to MP3DecInfo structure (initialized with pointers to all 
 *                the internal buffers needed for decoding, all other members of 
 *                MP3DecInfo structure set to 0)
 *
 * Notes:       if one or more mallocs fail, function frees any buffers already
 *                allocated before returning
 **************************************************************************************/ 
MP3DecInfo *AllocateBuffers(void)
{
	// MP3DecInfo *mp3DecInfo;
	// FrameHeader *fh;
	// SideInfo *si;
	// ScaleFactorInfo *sfi;
	// HuffmanInfo *hi;
	// DequantInfo *di;
	// IMDCTInfo *mi;
	// SubbandInfo *sbi;

	mp3_DecInfo = (MP3DecInfo *)m_new_obj(MP3DecInfo);
	if (!mp3_DecInfo)
		return 0;
	// ClearBuffer(mp3DecInfo, sizeof(MP3DecInfo));
	
	// fh =  (FrameHeader *)     calloc(1,sizeof(FrameHeader));
	// si =  (SideInfo *)        calloc(1,sizeof(SideInfo));
	// sfi = (ScaleFactorInfo *) calloc(1,sizeof(ScaleFactorInfo));
	// hi =  (HuffmanInfo *)     calloc(1,sizeof(HuffmanInfo));
	// di =  (DequantInfo *)     calloc(1,sizeof(DequantInfo));
	// mi =  (IMDCTInfo *)       calloc(1,sizeof(IMDCTInfo));
	// sbi = (SubbandInfo *)     calloc(1,sizeof(SubbandInfo));
	fh =  (FrameHeader *)     m_new_obj(FrameHeader);
	si =  (SideInfo *)        m_new_obj(SideInfo);
	sfi = (ScaleFactorInfo *) m_new_obj(ScaleFactorInfo);
	hi =  (HuffmanInfo *)     m_new_obj(HuffmanInfo);
	di =  (DequantInfo *)     m_new_obj(DequantInfo);
	mi =  (IMDCTInfo *)       m_new_obj(IMDCTInfo);
	sbi = (SubbandInfo *)     m_new_obj(SubbandInfo);

	mp3_DecInfo->FrameHeaderPS =     (void *)fh;
	mp3_DecInfo->SideInfoPS =        (void *)si;
	mp3_DecInfo->ScaleFactorInfoPS = (void *)sfi;
	mp3_DecInfo->HuffmanInfoPS =     (void *)hi;
	mp3_DecInfo->DequantInfoPS =     (void *)di;
	mp3_DecInfo->IMDCTInfoPS =       (void *)mi;
	mp3_DecInfo->SubbandInfoPS =     (void *)sbi;

	if (!fh || !si || !sfi || !hi || !di || !mi || !sbi) {
		FreeBuffers(mp3_DecInfo);	/* safe to call - only frees memory that was successfully allocated */
		return 0;
	}

	/* important to do this - DSP primitives assume a bunch of state variables are 0 on first use */
	// ClearBuffer(fh,  sizeof(FrameHeader));
	// ClearBuffer(si,  sizeof(SideInfo));
	// ClearBuffer(sfi, sizeof(ScaleFactorInfo));
	// ClearBuffer(hi,  sizeof(HuffmanInfo));
	// ClearBuffer(di,  sizeof(DequantInfo));
	// ClearBuffer(mi,  sizeof(IMDCTInfo));
	// ClearBuffer(sbi, sizeof(SubbandInfo));

	return mp3_DecInfo;
}

#define SAFE_FREE(x)	{if (x)	free(x);	(x) = 0;}	/* helper macro */

/**************************************************************************************
 * Function:    FreeBuffers
 *
 * Description: frees all the memory used by the MP3 decoder
 *
 * Inputs:      pointer to initialized MP3DecInfo structure
 *
 * Outputs:     none
 *
 * Return:      none
 *
 * Notes:       safe to call even if some buffers were not allocated (uses SAFE_FREE)
 **************************************************************************************/
void FreeBuffers(MP3DecInfo *mp3DecInfo)
{
	if (!mp3DecInfo)
		return;

	// SAFE_FREE(mp3DecInfo->FrameHeaderPS);
	// SAFE_FREE(mp3DecInfo->SideInfoPS);
	// SAFE_FREE(mp3DecInfo->ScaleFactorInfoPS);
	// SAFE_FREE(mp3DecInfo->HuffmanInfoPS);
	// SAFE_FREE(mp3DecInfo->DequantInfoPS);
	// SAFE_FREE(mp3DecInfo->IMDCTInfoPS);
	// SAFE_FREE(mp3DecInfo->SubbandInfoPS);

	// SAFE_FREE(mp3DecInfo);
	
	m_del_obj(FrameHeader, mp3DecInfo->FrameHeaderPS);
	m_del_obj(SideInfo, mp3DecInfo->SideInfoPS);
	m_del_obj(ScaleFactorInfo, mp3DecInfo->ScaleFactorInfoPS);
	m_del_obj(HuffmanInfo, mp3DecInfo->HuffmanInfoPS);
	m_del_obj(DequantInfo, mp3DecInfo->DequantInfoPS);
	m_del_obj(IMDCTInfo, mp3DecInfo->IMDCTInfoPS);
	m_del_obj(SubbandInfo, mp3DecInfo->SubbandInfoPS);

	m_del_obj(MP3DecInfo, mp3DecInfo);
}
