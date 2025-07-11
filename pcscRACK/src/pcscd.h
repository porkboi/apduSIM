/*
 * MUSCLE SmartCard Development ( https://pcsclite.apdu.fr/ )
 *
 * Copyright (C) 2006-2011
 *  Ludovic Rousseau <ludovic.rousseau@free.fr>
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions
 * are met:
 *
 * 1. Redistributions of source code must retain the above copyright
 *    notice, this list of conditions and the following disclaimer.
 * 2. Redistributions in binary form must reproduce the above copyright
 *    notice, this list of conditions and the following disclaimer in the
 *    documentation and/or other materials provided with the distribution.
 * 3. The name of the author may not be used to endorse or promote products
 *    derived from this software without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR
 * IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
 * OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
 * IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT, INDIRECT,
 * INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT
 * NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
 * DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
 * THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
 * (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF
 * THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 */

/**
 * @file
 * @brief This keeps a list of defines for pcsc-lite.
 */

#ifndef __pcscd_h__
#define __pcscd_h__

#define TIME_BEFORE_SUICIDE 60

#define SCARD_RESET			0x0001	/**< Card was reset */
#define SCARD_INSERTED			0x0002	/**< Card was inserted */
#define SCARD_REMOVED			0x0004	/**< Card was removed */

#define PCSCLITE_CONFIG_DIR		"/usr/local/etc/reader.conf.d"

#define PCSCLITE_IPC_DIR		"/run/pcscd"
#define PCSCLITE_RUN_PID		PCSCLITE_IPC_DIR "/pcscd.pid"

#define PCSCLITE_CSOCK_NAME		PCSCLITE_IPC_DIR "/pcscd.comm"

#define PCSCLITE_VERSION_NUMBER		"2.2.0"	/**< Current version */
#define PCSCLITE_STATUS_POLL_RATE	400000		/**< Status polling rate */
#define PCSCLITE_LOCK_POLL_RATE		100000		/**< Lock polling rate */

#define PCSC_MAX_CONTEXT_THREADS 200
#define PCSC_MAX_CONTEXT_CARD_HANDLES 200
#define PCSC_MAX_READER_HANDLES 200

/** Different values for struct ReaderContext powerState field */
enum
{
	POWER_STATE_UNPOWERED,	/**< auto power off */
	POWER_STATE_POWERED,	/**< powered */
	POWER_STATE_GRACE_PERIOD,	/**< card was in use */
	POWER_STATE_IN_USE		/**< card is used */
};

/** time to wait before powering down an unused card */
#define PCSCLITE_POWER_OFF_GRACE_PERIOD 5*1000 /* 5 second */

/** normal timeout for pthCardEvent driver function when
 * no card or card in use */
#define PCSCLITE_STATUS_EVENT_TIMEOUT 10*60*1000 /* 10 minutes */

/* Uncomment the next line if you do NOT want to use auto power off */
/* #define DISABLE_ON_DEMAND_POWER_ON */

/* Uncomment the next line if you do not want the card to be powered on
 * when inserted */
/* #define DISABLE_AUTO_POWER_ON */

#endif
