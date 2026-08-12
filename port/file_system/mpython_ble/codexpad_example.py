"""CodexPad C10/S10 example for the ESP32 掌控板 1.0.

For several controllers, hold the same button combination on the target while
the scan runs and replace ``connect`` with ``scan_and_connect`` below.
"""

import time

from mpython_ble.application import CodexPad
from mpython_ble.application.codexpad import (
    BUTTON_CROSS_A,
    BUTTON_START,
)


def main():
    pad = CodexPad(debug=False)

    # Normal mode selects the strongest matching CodexPad advertisement.
    if not pad.connect(timeout_ms=20000, scan_ms=5000):
        raise RuntimeError(pad.last_error)

    # To select a particular controller instead, use:
    # if not pad.scan_and_connect(BUTTON_START | BUTTON_CROSS_A):
    #     raise RuntimeError(pad.last_error)

    print("CodexPad connected:", pad.device_name)
    while True:
        # Notifications update inputs in the BLE IRQ; poll services reconnects.
        pad.poll()
        if pad.pressed(BUTTON_CROSS_A):
            print("A/Cross pressed")
        if pad.released(BUTTON_CROSS_A):
            print("A/Cross released")
        if pad.is_ready():
            print("buttons=0x{:08x}, axes={}".format(
                pad.button_states, pad.axis_values))
        time.sleep_ms(50)


main()
