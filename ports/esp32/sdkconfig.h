/* Start bootloader config */
#define CONFIG_FLASHMODE_DIO 1
#define CONFIG_ESPTOOLPY_FLASHFREQ_40M 1
/* End bootloader config */

#define CONFIG_TRACEMEM_RESERVE_DRAM 0x0
#define CONFIG_BT_RESERVE_DRAM 0x0
#define CONFIG_ULP_COPROC_RESERVE_MEM 2040
#define CONFIG_PHY_DATA_OFFSET 0xf000
#define CONFIG_APP_OFFSET 0x10000

#define CONFIG_SPI_FLASH_ROM_DRIVER_PATCH 1
#define CONFIG_FOUR_UNIVERSAL_MAC_ADDRESS 1
#define CONFIG_NUMBER_OF_UNIVERSAL_MAC_ADDRESS 4

#define CONFIG_BROWNOUT_DET 1
#define CONFIG_BROWNOUT_DET_LVL 0
#define CONFIG_BROWNOUT_DET_LVL_SEL_0 1

#define CONFIG_TCPIP_TASK_STACK_SIZE 2560
#define CONFIG_TCPIP_RECVMBOX_SIZE 32

#define CONFIG_ESP32_APPTRACE_DEST_NONE 1
#define CONFIG_ESP32_PHY_MAX_TX_POWER 20
#define CONFIG_ESP32_PANIC_PRINT_REBOOT 1
#define CONFIG_ESP32_RTC_CLOCK_SOURCE_INTERNAL_RC 1
#define CONFIG_ESP32_RTC_XTAL_BOOTSTRAP_CYCLES 100
#define CONFIG_ESP32_TIME_SYSCALL_USE_RTC_FRC1 1
#define CONFIG_ESP32_DEFAULT_CPU_FREQ_MHZ 240
#define CONFIG_ESP32_DEFAULT_CPU_FREQ_240 1
#define CONFIG_ESP32_DEBUG_OCDAWARE 1
#define CONFIG_ESP32_DEEP_SLEEP_WAKEUP_DELAY 2000
#define CONFIG_ESP32_ENABLE_COREDUMP_TO_NONE 1
#define CONFIG_ESP32_PHY_CALIBRATION_AND_DATA_STORAGE 1
#define CONFIG_ESP32_WIFI_AMPDU_ENABLED 1
#define CONFIG_ESP32_WIFI_NVS_ENABLED 1
#define CONFIG_ESP32_WIFI_STATIC_RX_BUFFER_NUM 10
#define CONFIG_ESP32_WIFI_DYNAMIC_RX_BUFFER_NUM 0
#define CONFIG_ESP32_WIFI_TX_BUFFER_TYPE 1
#define CONFIG_ESP32_WIFI_DYNAMIC_TX_BUFFER 1
#define CONFIG_ESP32_WIFI_DYNAMIC_TX_BUFFER_NUM 32
#define CONFIG_ESP32_WIFI_RX_BA_WIN 6
#define CONFIG_ESP32_WIFI_TX_BA_WIN 6
#define CONFIG_ESP32_XTAL_FREQ_AUTO 1
#define CONFIG_ESP32_XTAL_FREQ 0
#define CONFIG_ESP32_RTC_CLK_CAL_CYCLES 1024
#define CONFIG_ESP32_PTHREAD_TASK_PRIO_DEFAULT 5
#define CONFIG_ESP32_PTHREAD_TASK_STACK_SIZE_DEFAULT 2048

#if CONFIG_SPIRAM_SUPPORT
#define CONFIG_SPIRAM_TYPE_ESPPSRAM32 1
#define CONFIG_SPIRAM_SIZE 4194304
#define CONFIG_SPIRAM_SPEED_40M 1
#define CONFIG_SPIRAM_CACHE_WORKAROUND 1
#define CONFIG_SPIRAM_MALLOC_ALWAYSINTERNAL 16384
#define CONFIG_SPIRAM_BOOT_INIT 1
#define CONFIG_SPIRAM_MEMTEST 1
#define CONFIG_SPIRAM_USE_MALLOC 1
#define CONFIG_SPIRAM_MALLOC_RESERVE_INTERNAL 32768
#define CONFIG_SPIRAM_ALLOW_STACK_EXTERNAL_MEMORY 0
#endif

#define CONFIG_FOUR_MAC_ADDRESS_FROM_EFUSE 1
#define CONFIG_DMA_RX_BUF_NUM 10
#define CONFIG_DMA_TX_BUF_NUM 10
#define CONFIG_EMAC_TASK_PRIORITY 20

#define CONFIG_INT_WDT 1
#define CONFIG_INT_WDT_TIMEOUT_MS 300
#define CONFIG_INT_WDT_CHECK_CPU1 0
#define CONFIG_TASK_WDT 1
#define CONFIG_TASK_WDT_PANIC 1
#define CONFIG_TASK_WDT_TIMEOUT_S 5
#define CONFIG_TASK_WDT_CHECK_IDLE_TASK 0
#define CONFIG_TASK_WDT_CHECK_IDLE_TASK_CPU1 0

#define CONFIG_FREERTOS_UNICORE 1
#define CONFIG_FREERTOS_CORETIMER_0 1
#define CONFIG_FREERTOS_HZ 100
#define CONFIG_FREERTOS_ASSERT_FAIL_ABORT 1
#define CONFIG_FREERTOS_ASSERT_ON_UNTESTED_FUNCTION 1
#define CONFIG_FREERTOS_CHECK_STACKOVERFLOW_NONE 1
#define CONFIG_FREERTOS_THREAD_LOCAL_STORAGE_POINTERS 2
#define CONFIG_FREERTOS_IDLE_TASK_STACKSIZE 1024
#define CONFIG_FREERTOS_ISR_STACKSIZE 1536
#define CONFIG_FREERTOS_BREAK_ON_SCHEDULER_START_JTAG 1
#define CONFIG_FREERTOS_MAX_TASK_NAME_LEN 16
#define CONFIG_SUPPORT_STATIC_ALLOCATION 1
#define CONFIG_ENABLE_STATIC_TASK_CLEAN_UP_HOOK 1

#define CONFIG_MAIN_TASK_STACK_SIZE 4096
#define CONFIG_IPC_TASK_STACK_SIZE 1024
#define CONFIG_BTC_TASK_STACK_SIZE 3072
#define CONFIG_SYSTEM_EVENT_TASK_STACK_SIZE 4096
#define CONFIG_SYSTEM_EVENT_QUEUE_SIZE 32
#define CONFIG_TIMER_TASK_STACK_SIZE 4096
#define CONFIG_TIMER_TASK_PRIORITY 1
#define CONFIG_TIMER_TASK_STACK_DEPTH 2048
#define CONFIG_TIMER_QUEUE_LENGTH 10

#define CONFIG_NEWLIB_STDIN_LINE_ENDING_CR 1
#define CONFIG_NEWLIB_STDOUT_LINE_ENDING_CRLF 1
#define CONFIG_PHY_ENABLED 1
#define CONFIG_WIFI_ENABLED 1
#define CONFIG_OPTIMIZATION_LEVEL_DEBUG 1
#define CONFIG_MEMMAP_SMP 1

#define CONFIG_PARTITION_TABLE_OFFSET 0x8000
#define CONFIG_PARTITION_TABLE_SINGLE_APP 1
#define CONFIG_PARTITION_TABLE_FILENAME "partitions_singleapp.csv"
#define CONFIG_PARTITION_TABLE_CUSTOM_APP_BIN_OFFSET 0x10000
#define CONFIG_PARTITION_TABLE_CUSTOM_FILENAME "partitions.csv"

#define CONFIG_CONSOLE_UART_BAUDRATE 115200
#define CONFIG_CONSOLE_UART_NUM 0
#define CONFIG_CONSOLE_UART_DEFAULT 1

#define CONFIG_LOG_DEFAULT_LEVEL_INFO 1
#define CONFIG_LOG_BOOTLOADER_LEVEL_WARN 1
#define CONFIG_LOG_DEFAULT_LEVEL 1
#define CONFIG_LOG_COLORS 1
#define CONFIG_LOG_BOOTLOADER_LEVEL 2

#define CONFIG_LWIP_THREAD_LOCAL_STORAGE_INDEX 0
#define CONFIG_LWIP_DHCP_DOES_ARP_CHECK 1
#define CONFIG_LWIP_DHCP_MAX_NTP_SERVERS 1
#define CONFIG_LWIP_DHCPS_LEASE_UNIT 60
#define CONFIG_LWIP_DHCPS_MAX_STATION_NUM 8
#define CONFIG_LWIP_MAX_ACTIVE_TCP 16
#define CONFIG_LWIP_MAX_SOCKETS 8
#define CONFIG_LWIP_SO_REUSE 1
#define CONFIG_LWIP_ETHARP_TRUST_IP_MAC 1
#define CONFIG_PPP_SUPPORT 1
#define CONFIG_IP_LOST_TIMER_INTERVAL 120
#define CONFIG_UDP_RECVMBOX_SIZE 6
#define CONFIG_TCP_MAXRTX 12
#define CONFIG_TCP_SYNMAXRTX 6
#define CONFIG_TCP_MSL 60000
#define CONFIG_TCP_MSS 1436
#define CONFIG_TCP_SND_BUF_DEFAULT 5744
#define CONFIG_TCP_WND_DEFAULT 5744
#define CONFIG_TCP_QUEUE_OOSEQ 1
#define CONFIG_TCP_OVERSIZE_MSS 1
#define CONFIG_TCP_RECVMBOX_SIZE 6

#define CONFIG_MBEDTLS_AES_C 1
#define CONFIG_MBEDTLS_CCM_C 1
#define CONFIG_MBEDTLS_ECDH_C 1
#define CONFIG_MBEDTLS_ECDSA_C 1
#define CONFIG_MBEDTLS_ECP_C 1
#define CONFIG_MBEDTLS_ECP_DP_BP256R1_ENABLED 1
#define CONFIG_MBEDTLS_ECP_DP_BP384R1_ENABLED 1
#define CONFIG_MBEDTLS_ECP_DP_BP512R1_ENABLED 1
#define CONFIG_MBEDTLS_ECP_DP_CURVE25519_ENABLED 1
#define CONFIG_MBEDTLS_ECP_DP_SECP192K1_ENABLED 1
#define CONFIG_MBEDTLS_ECP_DP_SECP192R1_ENABLED 1
#define CONFIG_MBEDTLS_ECP_DP_SECP224K1_ENABLED 1
#define CONFIG_MBEDTLS_ECP_DP_SECP224R1_ENABLED 1
#define CONFIG_MBEDTLS_ECP_DP_SECP256K1_ENABLED 1
#define CONFIG_MBEDTLS_ECP_DP_SECP256R1_ENABLED 1
#define CONFIG_MBEDTLS_ECP_DP_SECP384R1_ENABLED 1
#define CONFIG_MBEDTLS_ECP_DP_SECP521R1_ENABLED 1
#define CONFIG_MBEDTLS_ECP_NIST_OPTIM 1
#define CONFIG_MBEDTLS_GCM_C 1
#define CONFIG_MBEDTLS_HARDWARE_AES 1
#define CONFIG_MBEDTLS_HAVE_TIME 1
#define CONFIG_MBEDTLS_KEY_EXCHANGE_DHE_RSA 1
#define CONFIG_MBEDTLS_KEY_EXCHANGE_ECDH_ECDSA 1
#define CONFIG_MBEDTLS_KEY_EXCHANGE_ECDHE_ECDSA 1
#define CONFIG_MBEDTLS_KEY_EXCHANGE_ECDHE_RSA 1
#define CONFIG_MBEDTLS_KEY_EXCHANGE_ECDH_RSA 1
#define CONFIG_MBEDTLS_KEY_EXCHANGE_ELLIPTIC_CURVE 1
#define CONFIG_MBEDTLS_KEY_EXCHANGE_RSA 1
#define CONFIG_MBEDTLS_PEM_PARSE_C 1
#define CONFIG_MBEDTLS_PEM_WRITE_C 1
#define CONFIG_MBEDTLS_RC4_DISABLED 1
#define CONFIG_MBEDTLS_SSL_ALPN 1
#define CONFIG_MBEDTLS_SSL_MAX_CONTENT_LEN 16384
#define CONFIG_MBEDTLS_SSL_PROTO_TLS1 1
#define CONFIG_MBEDTLS_SSL_PROTO_TLS1_1 1
#define CONFIG_MBEDTLS_SSL_PROTO_TLS1_2 1
#define CONFIG_MBEDTLS_SSL_RENEGOTIATION 1
#define CONFIG_MBEDTLS_SSL_SESSION_TICKETS 1
#define CONFIG_MBEDTLS_TLS_CLIENT 1
#define CONFIG_MBEDTLS_TLS_ENABLED 1
#define CONFIG_MBEDTLS_TLS_SERVER 1
#define CONFIG_MBEDTLS_TLS_SERVER_AND_CLIENT 1
#define CONFIG_MBEDTLS_X509_CRL_PARSE_C 1
#define CONFIG_MBEDTLS_X509_CSR_PARSE_C 1

#define CONFIG_MAKE_WARN_UNDEFINED_VARIABLES 1
#define CONFIG_TOOLPREFIX "xtensa-esp32-elf-"
#define CONFIG_PYTHON "python2"
