/**
 * 
 */

#ifndef __MPYTHON_BLE_SERVICE_HIDD_USAGES_H__
#define __MPYTHON_BLE_SERVICE_HIDD_USAGES_H__
#include <stdint.h>

#define LEFT_CONTROL_KEY_MASK        (1 << 0)
#define LEFT_SHIFT_KEY_MASK          (1 << 1)
#define LEFT_ALT_KEY_MASK            (1 << 2)
#define LEFT_GUI_KEY_MASK            (1 << 3)
#define RIGHT_CONTROL_KEY_MASK       (1 << 4)
#define RIGHT_SHIFT_KEY_MASK         (1 << 5)
#define RIGHT_ALT_KEY_MASK           (1 << 6)
#define RIGHT_GUI_KEY_MASK           (1 << 7)
typedef uint8_t key_mask_t;

// HID Keyboard/Keypad Usage IDs (subset of the codes available in the USB HID Usage Tables spec)
#define HID_KEY_RESERVED       0    // No event inidicated
#define HID_KEY_A              4    // Keyboard a and A
#define HID_KEY_B              5    // Keyboard b and B
#define HID_KEY_C              6    // Keyboard c and C
#define HID_KEY_D              7    // Keyboard d and D
#define HID_KEY_E              8    // Keyboard e and E
#define HID_KEY_F              9    // Keyboard f and F
#define HID_KEY_G              10   // Keyboard g and G
#define HID_KEY_H              11   // Keyboard h and H
#define HID_KEY_I              12   // Keyboard i and I
#define HID_KEY_J              13   // Keyboard j and J
#define HID_KEY_K              14   // Keyboard k and K
#define HID_KEY_L              15   // Keyboard l and L
#define HID_KEY_M              16   // Keyboard m and M
#define HID_KEY_N              17   // Keyboard n and N
#define HID_KEY_O              18   // Keyboard o and O
#define HID_KEY_P              19   // Keyboard p and p
#define HID_KEY_Q              20   // Keyboard q and Q
#define HID_KEY_R              21   // Keyboard r and R
#define HID_KEY_S              22   // Keyboard s and S
#define HID_KEY_T              23   // Keyboard t and T
#define HID_KEY_U              24   // Keyboard u and U
#define HID_KEY_V              25   // Keyboard v and V
#define HID_KEY_W              26   // Keyboard w and W
#define HID_KEY_X              27   // Keyboard x and X
#define HID_KEY_Y              28   // Keyboard y and Y
#define HID_KEY_Z              29   // Keyboard z and Z
#define HID_KEY_1              30   // Keyboard 1 and !
#define HID_KEY_2              31   // Keyboard 2 and @
#define HID_KEY_3              32   // Keyboard 3 and #
#define HID_KEY_4              33   // Keyboard 4 and %
#define HID_KEY_5              34   // Keyboard 5 and %
#define HID_KEY_6              35   // Keyboard 6 and ^
#define HID_KEY_7              36   // Keyboard 7 and &
#define HID_KEY_8              37   // Keyboard 8 and *
#define HID_KEY_9              38   // Keyboard 9 and (
#define HID_KEY_0              39   // Keyboard 0 and )
#define HID_KEY_RETURN         40   // Keyboard Return (ENTER)
#define HID_KEY_ESCAPE         41   // Keyboard ESCAPE
#define HID_KEY_DELETE         42   // Keyboard DELETE (Backspace)
#define HID_KEY_TAB            43   // Keyboard Tab
#define HID_KEY_SPACEBAR       44   // Keyboard Spacebar
#define HID_KEY_MINUS          45   // Keyboard - and (underscore)
#define HID_KEY_EQUAL          46   // Keyboard = and +
#define HID_KEY_LEFT_BRKT      47   // Keyboard [ and {
#define HID_KEY_RIGHT_BRKT     48   // Keyboard ] and }
#define HID_KEY_BACK_SLASH     49   // Keyboard \ and |
#define HID_KEY_SEMI_COLON     51   // Keyboard ; and :
#define HID_KEY_SGL_QUOTE      52   // Keyboard ' and "
#define HID_KEY_GRV_ACCENT     53   // Keyboard Grave Accent and Tilde
#define HID_KEY_COMMA          54   // Keyboard , and <
#define HID_KEY_DOT            55   // Keyboard . and >
#define HID_KEY_FWD_SLASH      56   // Keyboard / and ?
#define HID_KEY_CAPS_LOCK      57   // Keyboard Caps Lock
#define HID_KEY_F1             58   // Keyboard F1
#define HID_KEY_F2             59   // Keyboard F2
#define HID_KEY_F3             60   // Keyboard F3
#define HID_KEY_F4             61   // Keyboard F4
#define HID_KEY_F5             62   // Keyboard F5
#define HID_KEY_F6             63   // Keyboard F6
#define HID_KEY_F7             64   // Keyboard F7
#define HID_KEY_F8             65   // Keyboard F8
#define HID_KEY_F9             66   // Keyboard F9
#define HID_KEY_F10            67   // Keyboard F10
#define HID_KEY_F11            68   // Keyboard F11
#define HID_KEY_F12            69   // Keyboard F12
#define HID_KEY_PRNT_SCREEN    70   // Keyboard Print Screen
#define HID_KEY_SCROLL_LOCK    71   // Keyboard Scroll Lock
#define HID_KEY_PAUSE          72   // Keyboard Pause
#define HID_KEY_INSERT         73   // Keyboard Insert
#define HID_KEY_HOME           74   // Keyboard Home
#define HID_KEY_PAGE_UP        75   // Keyboard PageUp
#define HID_KEY_DELETE_FWD     76   // Keyboard Delete Forward
#define HID_KEY_END            77   // Keyboard End
#define HID_KEY_PAGE_DOWN      78   // Keyboard PageDown
#define HID_KEY_RIGHT_ARROW    79   // Keyboard RightArrow
#define HID_KEY_LEFT_ARROW     80   // Keyboard LeftArrow
#define HID_KEY_DOWN_ARROW     81   // Keyboard DownArrow
#define HID_KEY_UP_ARROW       82   // Keyboard UpArrow
#define HID_KEY_NUM_LOCK       83   // Keypad Num Lock and Clear
#define HID_KEY_DIVIDE         84   // Keypad /
#define HID_KEY_MULTIPLY       85   // Keypad *
#define HID_KEY_SUBTRACT       86   // Keypad -
#define HID_KEY_ADD            87   // Keypad +
#define HID_KEY_ENTER          88   // Keypad ENTER
#define HID_KEYPAD_1           89   // Keypad 1 and End
#define HID_KEYPAD_2           90   // Keypad 2 and Down Arrow
#define HID_KEYPAD_3           91   // Keypad 3 and PageDn
#define HID_KEYPAD_4           92   // Keypad 4 and Lfet Arrow
#define HID_KEYPAD_5           93   // Keypad 5
#define HID_KEYPAD_6           94   // Keypad 6 and Right Arrow
#define HID_KEYPAD_7           95   // Keypad 7 and Home
#define HID_KEYPAD_8           96   // Keypad 8 and Up Arrow
#define HID_KEYPAD_9           97   // Keypad 9 and PageUp
#define HID_KEYPAD_0           98   // Keypad 0 and Insert
#define HID_KEYPAD_DOT         99   // Keypad . and Delete
#define HID_KEY_MUTE           127  // Keyboard Mute
#define HID_KEY_VOLUME_UP      128  // Keyboard Volume up
#define HID_KEY_VOLUME_DOWN    129  // Keyboard Volume down
#define HID_KEY_LEFT_CTRL      224  // Keyboard LeftContorl
#define HID_KEY_LEFT_SHIFT     225  // Keyboard LeftShift
#define HID_KEY_LEFT_ALT       226  // Keyboard LeftAlt
#define HID_KEY_LEFT_GUI       227  // Keyboard LeftGUI
#define HID_KEY_RIGHT_CTRL     228  // Keyboard LeftContorl
#define HID_KEY_RIGHT_SHIFT    229  // Keyboard LeftShift
#define HID_KEY_RIGHT_ALT      230  // Keyboard LeftAlt
#define HID_KEY_RIGHT_GUI      231  // Keyboard RightGUI
typedef uint8_t keyboard_cmd_t;

#define HID_MOUSE_LEFT       (253)
#define HID_MOUSE_MIDDLE     (254)
#define HID_MOUSE_RIGHT      (255)
typedef uint8_t mouse_cmd_t;

// HID Consumer Usage IDs (subset of the codes available in the USB HID Usage Tables spec)
#define HID_CONSUMER_POWER          48  // Power
#define HID_CONSUMER_RESET          49  // Reset
#define HID_CONSUMER_SLEEP          50  // Sleep

#define HID_CONSUMER_MENU           64  // Menu
#define HID_CONSUMER_SELECTION      128 // Selection
#define HID_CONSUMER_ASSIGN_SEL     129 // Assign Selection
#define HID_CONSUMER_MODE_STEP      130 // Mode Step
#define HID_CONSUMER_RECALL_LAST    131 // Recall Last
#define HID_CONSUMER_QUIT           148 // Quit
#define HID_CONSUMER_HELP           149 // Help
#define HID_CONSUMER_CHANNEL_UP     156 // Channel Increment
#define HID_CONSUMER_CHANNEL_DOWN   157 // Channel Decrement

#define HID_CONSUMER_PLAY           176 // Play
#define HID_CONSUMER_PAUSE          177 // Pause
#define HID_CONSUMER_RECORD         178 // Record
#define HID_CONSUMER_FAST_FORWARD   179 // Fast Forward
#define HID_CONSUMER_REWIND         180 // Rewind
#define HID_CONSUMER_SCAN_NEXT_TRK  181 // Scan Next Track
#define HID_CONSUMER_SCAN_PREV_TRK  182 // Scan Previous Track
#define HID_CONSUMER_STOP           183 // Stop
#define HID_CONSUMER_EJECT          184 // Eject
#define HID_CONSUMER_RANDOM_PLAY    185 // Random Play
#define HID_CONSUMER_SELECT_DISC    186 // Select Disk
#define HID_CONSUMER_ENTER_DISC     187 // Enter Disc
#define HID_CONSUMER_REPEAT         188 // Repeat
#define HID_CONSUMER_STOP_EJECT     204 // Stop/Eject
#define HID_CONSUMER_PLAY_PAUSE     205 // Play/Pause
#define HID_CONSUMER_PLAY_SKIP      206 // Play/Skip

#define HID_CONSUMER_VOLUME         224 // Volume
#define HID_CONSUMER_BALANCE        225 // Balance
#define HID_CONSUMER_MUTE           226 // Mute
#define HID_CONSUMER_BASS           227 // Bass
#define HID_CONSUMER_VOLUME_UP      233 // Volume Increment
#define HID_CONSUMER_VOLUME_DOWN    234 // Volume Decrement
typedef uint8_t consumer_cmd_t;

#endif