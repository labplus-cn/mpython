# Set location of base MicroPython directory.
if(NOT MICROPY_DIR)
    get_filename_component(MICROPY_DIR ${PROJECT_DIR}/../.. ABSOLUTE)
endif()

set(MICROPY_DIR ${MICROPY_DIR}/mpython/micropython)

# message("MICROPY_DIR:"${MICROPY_DIR})
# message("PROJECT_DIR:"${PROJECT_DIR})

# Include core source components.
include(${MICROPY_DIR}/py/py.cmake)

if(NOT CMAKE_BUILD_EARLY_EXPANSION)
    # Enable extmod components that will be configured by extmod.cmake.
    # A board may also have enabled additional components.
    set(MICROPY_PY_BTREE ON)

    include(${MICROPY_DIR}/py/usermod.cmake)
    include(${MICROPY_DIR}/extmod/extmod.cmake)
endif()

set(MICROPY_QSTRDEFS_PORT
    ${PROJECT_DIR}/qstrdefsport.h
)

set(MICROPY_SOURCE_SHARED
    ${MICROPY_DIR}/shared/readline/readline.c
    ${MICROPY_DIR}/shared/netutils/netutils.c
    ${MICROPY_DIR}/shared/timeutils/timeutils.c
    ${MICROPY_DIR}/shared/runtime/interrupt_char.c
    ${MICROPY_DIR}/shared/runtime/stdout_helpers.c
    ${MICROPY_DIR}/shared/runtime/sys_stdio_mphal.c
    ${MICROPY_DIR}/shared/runtime/pyexec.c
)

set(MICROPY_SOURCE_LIB
    ${MICROPY_DIR}/lib/littlefs/lfs1.c
    ${MICROPY_DIR}/lib/littlefs/lfs1_util.c
    ${MICROPY_DIR}/lib/littlefs/lfs2.c
    ${MICROPY_DIR}/lib/littlefs/lfs2_util.c
    ${MICROPY_DIR}/lib/mbedtls_errors/mp_mbedtls_errors.c
    ${MICROPY_DIR}/lib/oofatfs/ff.c
    ${MICROPY_DIR}/lib/oofatfs/ffunicode.c
)
if(IDF_TARGET STREQUAL "esp32c3")
    list(APPEND MICROPY_SOURCE_LIB ${MICROPY_DIR}/shared/runtime/gchelper_generic.c)
endif()

set(MICROPY_SOURCE_DRIVERS
    ${MICROPY_DIR}/drivers/bus/softspi.c
    ${MICROPY_DIR}/drivers/dht/dht.c
)

set(MICROPY_SOURCE_PORT
    ${MICROPY_DIR}/ports/esp32/main.c
    ${MICROPY_DIR}/ports/esp32/uart.c
    ${MICROPY_DIR}/ports/esp32/usb.c
    ${MICROPY_DIR}/ports/esp32/usb_serial_jtag.c
    ${MICROPY_DIR}/ports/esp32/gccollect.c
    ${MICROPY_DIR}/ports/esp32/mphalport.c
    ${MICROPY_DIR}/ports/esp32/fatfs_port.c
    ${MICROPY_DIR}/ports/esp32/help.c
    ${MICROPY_DIR}/ports/esp32/modutime.c
    ${MICROPY_DIR}/ports/esp32/machine_bitstream.c
    ${MICROPY_DIR}/ports/esp32/machine_timer.c
    ${MICROPY_DIR}/ports/esp32/machine_adc.c
    ${MICROPY_DIR}/ports/esp32/machine_adcblock.c
    ${MICROPY_DIR}/ports/esp32/machine_dac.c
    ${MICROPY_DIR}/ports/esp32/machine_i2c.c
    ${MICROPY_DIR}/ports/esp32/machine_i2s.c
    ${MICROPY_DIR}/ports/esp32/machine_uart.c
    ${MICROPY_DIR}/ports/esp32/modmachine.c
    ${MICROPY_DIR}/ports/esp32/modnetwork.c
    ${MICROPY_DIR}/ports/esp32/network_lan.c
    ${MICROPY_DIR}/ports/esp32/network_ppp.c
    ${MICROPY_DIR}/ports/esp32/network_wlan.c
    ${MICROPY_DIR}/ports/esp32/mpnimbleport.c
    ${MICROPY_DIR}/ports/esp32/modsocket.c
    ${MICROPY_DIR}/ports/esp32/modesp.c
    ${MICROPY_DIR}/ports/esp32/esp32_nvs.c
    ${MICROPY_DIR}/ports/esp32/esp32_partition.c
    ${MICROPY_DIR}/ports/esp32/esp32_rmt.c
    ${MICROPY_DIR}/ports/esp32/esp32_ulp.c
    ${MICROPY_DIR}/ports/esp32/modesp32.c
    ${MICROPY_DIR}/ports/esp32/machine_hw_spi.c
    ${MICROPY_DIR}/ports/esp32/machine_wdt.c
    ${MICROPY_DIR}/ports/esp32/mpthreadport.c
    ${MICROPY_DIR}/ports/esp32/machine_rtc.c
    ${MICROPY_DIR}/ports/esp32/machine_sdcard.c
    ${MICROPY_PORT_DIR}/builtins/machine_pin.c
    ${MICROPY_PORT_DIR}/builtins/machine_servo.c
    ${MICROPY_PORT_DIR}/builtins/machine_touchpad.c
    # ${MICROPY_PORT_DIR}/builtins/modnetwork.c
    # ${MICROPY_PORT_DIR}/builtins/modcodec.c
    # ${MICROPY_PORT_DIR}/builtins/modframebuf.c
    # ${MICROPY_PORT_DIR}/builtins/modmotion.c
    # ${MICROPY_PORT_DIR}/builtins/modmusic.c
    # ${MICROPY_PORT_DIR}/builtins/modradio.c
    # ${MICROPY_PORT_DIR}/builtins/modrfid.c
    # ${MICROPY_PORT_DIR}/builtins/modrgbLED5x5.c
    # ${MICROPY_PORT_DIR}/builtins/modxunfeiAI.c
)

set(MICROPY_SOURCE_QSTR
    ${MICROPY_SOURCE_PY}
    ${MICROPY_SOURCE_EXTMOD}
    ${MICROPY_SOURCE_USERMOD}
    ${MICROPY_SOURCE_SHARED}
    ${MICROPY_SOURCE_LIB}
    ${MICROPY_SOURCE_PORT}
    ${MICROPY_SOURCE_BOARD}
)

message("MICROPY_SOURCE_PY:"${MICROPY_SOURCE_PY})
message("================")
message("MICROPY_SOURCE_PORT:"${MICROPY_SOURCE_PORT})
message("================")
message("MICROPY_SOURCE_BOARD:"${MICROPY_SOURCE_BOARD})
message("================")

set(IDF_COMPONENTS
    app_update
    bootloader_support
    bt
    driver
    esp_adc_cal
    esp_common
    esp_eth
    esp_event
    esp_ringbuf
    esp_rom
    esp_wifi
    freertos
    heap
    log
    lwip
    mbedtls
    mdns
    newlib
    nvs_flash
    sdmmc
    soc
    spi_flash
    tcpip_adapter
    ulp
    vfs
    xtensa
)

if(IDF_VERSION_MINOR GREATER_EQUAL 1 OR IDF_VERSION_MAJOR GREATER_EQUAL 5)
    list(APPEND IDF_COMPONENTS esp_netif)
endif()

if(IDF_VERSION_MINOR GREATER_EQUAL 2 OR IDF_VERSION_MAJOR GREATER_EQUAL 5)
    list(APPEND IDF_COMPONENTS esp_system)
    list(APPEND IDF_COMPONENTS esp_timer)
endif()

if(IDF_VERSION_MINOR GREATER_EQUAL 3 OR IDF_VERSION_MAJOR GREATER_EQUAL 5)
    list(APPEND IDF_COMPONENTS esp_hw_support)
    list(APPEND IDF_COMPONENTS esp_pm)
    list(APPEND IDF_COMPONENTS hal)
endif()

if(IDF_TARGET STREQUAL "esp32")
    list(APPEND IDF_COMPONENTS esp32)
elseif(IDF_TARGET STREQUAL "esp32c3")
    list(APPEND IDF_COMPONENTS esp32c3)
    list(APPEND IDF_COMPONENTS riscv)
elseif(IDF_TARGET STREQUAL "esp32s2")
    list(APPEND IDF_COMPONENTS esp32s2)
    list(APPEND IDF_COMPONENTS tinyusb)
elseif(IDF_TARGET STREQUAL "esp32s3")
    list(APPEND IDF_COMPONENTS esp32s3)
    list(APPEND IDF_COMPONENTS tinyusb)
endif()

# Register the main IDF component.
idf_component_register(
    SRCS
        ${MICROPY_SOURCE_PY}
        ${MICROPY_SOURCE_EXTMOD}
        ${MICROPY_SOURCE_SHARED}
        ${MICROPY_SOURCE_LIB}
        ${MICROPY_SOURCE_DRIVERS}
        ${MICROPY_SOURCE_PORT}
        ${MICROPY_SOURCE_BOARD}
    INCLUDE_DIRS
        ${MICROPY_INC_CORE}
        ${MICROPY_INC_USERMOD}
        ${MICROPY_PORT_DIR}
        ${MICROPY_BOARD_DIR}
        ${CMAKE_BINARY_DIR}
    REQUIRES
        ${IDF_COMPONENTS}
)

# Set the MicroPython target as the current (main) IDF component target.
set(MICROPY_TARGET ${COMPONENT_TARGET})

# Define mpy-cross flags, for use with frozen code.
set(MICROPY_CROSS_FLAGS -march=xtensawin)

# Set compile options for this port.
target_compile_definitions(${MICROPY_TARGET} PUBLIC
    ${MICROPY_DEF_CORE}
    MICROPY_ESP_IDF_4=1
    MICROPY_VFS_FAT=1
    MICROPY_VFS_LFS2=1
    FFCONF_H=\"${MICROPY_OOFATFS_DIR}/ffconf.h\"
    LFS1_NO_MALLOC LFS1_NO_DEBUG LFS1_NO_WARN LFS1_NO_ERROR LFS1_NO_ASSERT
    LFS2_NO_MALLOC LFS2_NO_DEBUG LFS2_NO_WARN LFS2_NO_ERROR LFS2_NO_ASSERT
)

# Disable some warnings to keep the build output clean.
target_compile_options(${MICROPY_TARGET} PUBLIC
    -Wno-clobbered
    -Wno-deprecated-declarations
    -Wno-missing-field-initializers
)


# Add additional extmod and usermod components.
target_link_libraries(${MICROPY_TARGET} micropy_extmod_btree)
target_link_libraries(${MICROPY_TARGET} usermod)

# Collect all of the include directories and compile definitions for the IDF components.
foreach(comp ${IDF_COMPONENTS})
    micropy_gather_target_properties(__idf_${comp})
endforeach()

if(IDF_VERSION_MINOR GREATER_EQUAL 2 OR IDF_VERSION_MAJOR GREATER_EQUAL 5)
    # These paths cannot currently be found by the IDF_COMPONENTS search loop above,
    # so add them explicitly.
    list(APPEND MICROPY_CPP_INC_EXTRA ${IDF_PATH}/components/soc/soc/${IDF_TARGET}/include)
    list(APPEND MICROPY_CPP_INC_EXTRA ${IDF_PATH}/components/soc/soc/include)
    if(IDF_VERSION_MINOR GREATER_EQUAL 3)
        list(APPEND MICROPY_CPP_INC_EXTRA ${IDF_PATH}/components/tinyusb/additions/include)
        list(APPEND MICROPY_CPP_INC_EXTRA ${IDF_PATH}/components/tinyusb/tinyusb/src)
    endif()
endif()

# Include the main MicroPython cmake rules.
include(${MICROPY_DIR}/py/mkrules.cmake)
