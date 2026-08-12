"""BLE Central driver for CodexPad-C10 and CodexPad-S10 on ESP32 mPython.

The controller uses a custom BLE GATT protocol.  The notification report on
FFA1 is ``<IBBBB``: a 32-bit button mask followed by four joystick axes.
This module intentionally uses the legacy mPython ``gap_scan`` signature.
"""

import bluetooth
import struct
import time
from bluetooth import UUID

from ..const import IRQ


BUTTON_UP = 1 << 0
BUTTON_DOWN = 1 << 1
BUTTON_LEFT = 1 << 2
BUTTON_RIGHT = 1 << 3
BUTTON_SQUARE_X = 1 << 4
BUTTON_TRIANGLE_Y = 1 << 5
BUTTON_CROSS_A = 1 << 6
BUTTON_CIRCLE_B = 1 << 7
BUTTON_L1 = 1 << 8
BUTTON_L2 = 1 << 9
BUTTON_L3 = 1 << 10
BUTTON_R1 = 1 << 11
BUTTON_R2 = 1 << 12
BUTTON_R3 = 1 << 13
BUTTON_SELECT = 1 << 14
BUTTON_START = 1 << 15
BUTTON_HOME = 1 << 16

AXIS_LEFT_STICK_X = 0
AXIS_LEFT_STICK_Y = 1
AXIS_RIGHT_STICK_X = 2
AXIS_RIGHT_STICK_Y = 3
AXIS_CENTER = 0x80

TX_POWER_MINUS_16_DBM = -16
TX_POWER_MINUS_12_DBM = -12
TX_POWER_MINUS_8_DBM = -8
TX_POWER_MINUS_5_DBM = -5
TX_POWER_MINUS_3_DBM = -3
TX_POWER_MINUS_1_DBM = -1
TX_POWER_0_DBM = 0
TX_POWER_1_DBM = 1
TX_POWER_2_DBM = 2
TX_POWER_3_DBM = 3
TX_POWER_4_DBM = 4
TX_POWER_5_DBM = 5
TX_POWER_6_DBM = 6

_CODEXPAD_PREFIX = b"CodexPad-"
_MANUFACTURER_HEADER = b"CodexPad"
_INPUTS_SERVICE_UUID = UUID(0xFFA0)
_INPUTS_CHARACTERISTIC_UUID = UUID(0xFFA1)
_TX_POWER_SERVICE_UUID = UUID(0x1804)
_TX_POWER_CHARACTERISTIC_UUID = UUID(0x2A07)
_CCCD_UUID = UUID(0x2902)


def _ad_field(payload, field_type):
    index = 0
    while index + 1 < len(payload):
        length = payload[index]
        if length == 0:
            break
        end = index + length + 1
        if end > len(payload):
            break
        if payload[index + 1] == field_type:
            return bytes(payload[index + 2:end])
        index = end
    return None


def _device_name(payload):
    return _ad_field(payload, 0x09) or _ad_field(payload, 0x08)


def _advertised_state(payload):
    """Return ``(button_mask, firmware_major, held_seconds)`` if present."""
    data = _ad_field(payload, 0xFF)
    if data is None or len(data) < 18 or data[:2] != b"\xff\xff":
        return None
    data = data[2:]
    if data[:8] != _MANUFACTURER_HEADER:
        return None
    return struct.unpack_from("<I", data, 11)[0], data[8], data[15]


class CodexPad(object):
    """Input driver shared by CodexPad C10 and S10."""

    def __init__(self, name_prefix=_CODEXPAD_PREFIX, ble=None, debug=False):
        if isinstance(name_prefix, str):
            name_prefix = name_prefix.encode()
        self.ble = ble if ble is not None else bluetooth.BLE()
        self.ble.active(True)
        self.ble.irq(self._irq)
        self.name_prefix = bytes(name_prefix)
        self.debug = debug
        self.connected_handle = None
        self.device_name = None
        self.model = None
        self.last_error = None
        self.last_callback_error = None
        self._state = "idle"
        self._candidate = None
        self._scan_entries = {}
        self._button_mask = None
        self._service_ranges = {}
        self._service_queue = []
        self._service_index = -1
        self._current_service = None
        self._current_characteristics = []
        self._input_def_handle = None
        self._input_value_handle = None
        self._input_descriptor_end = None
        self._input_cccd_handle = None
        self._tx_power_value_handle = None
        self._ready = False
        self._auto_reconnect = False
        self._retry_at = time.ticks_ms()
        self._input_callback = None
        self._reset_inputs()

    def _reset_inputs(self):
        self._previous_button_states = 0
        self._button_states = 0
        self._axis_values = [AXIS_CENTER, AXIS_CENTER, AXIS_CENTER, AXIS_CENTER]
        self._pressed_events = 0
        self._released_events = 0
        self._axis_change_deltas = [0, 0, 0, 0]
        self._axis_endpoint_events = [False, False, False, False]

    def on_input(self, callback):
        """Set ``callback(button_states, axis_values)`` for input updates."""
        self._input_callback = callback

    def connect(self, timeout_ms=20000, scan_ms=5000):
        return self._connect_with_mask(None, timeout_ms, scan_ms)

    def scan_and_connect(self, button_mask, timeout_ms=20000, scan_ms=5000):
        if button_mask == BUTTON_HOME:
            raise ValueError("BUTTON_HOME alone cannot be used as a connection mask")
        return self._connect_with_mask(button_mask, timeout_ms, scan_ms)

    def _connect_with_mask(self, button_mask, timeout_ms, scan_ms):
        if self._ready:
            return True
        if self._state != "idle":
            self.last_error = "BLE operation already in progress: {}".format(self._state)
            return False
        self._auto_reconnect = True
        self.last_error = None
        self._button_mask = button_mask
        self._start_scan(scan_ms)
        deadline = time.ticks_add(time.ticks_ms(), timeout_ms)
        while time.ticks_diff(deadline, time.ticks_ms()) > 0:
            if self._ready:
                return True
            if self._state == "idle" and self.last_error is not None:
                return False
            time.sleep_ms(20)
        self.last_error = "connection timed out"
        self._cancel_pending_operation()
        return False

    def poll(self):
        """Maintain automatic reconnection; call regularly in the main loop."""
        if (self._auto_reconnect and self._state == "idle" and
                time.ticks_diff(time.ticks_ms(), self._retry_at) >= 0):
            self.last_error = None
            self._start_scan(5000)

    def disconnect(self):
        self._auto_reconnect = False
        self.last_error = None
        self._cancel_pending_operation()

    def is_connected(self):
        return self.connected_handle is not None

    def is_ready(self):
        return self._ready

    def button_state(self, button):
        return (self._button_states & button) != 0

    def pressed(self, button):
        result = bool(self._pressed_events & button)
        self._pressed_events &= ~button
        return result

    def released(self, button):
        result = bool(self._released_events & button)
        self._released_events &= ~button
        return result

    def holding(self, button):
        return bool(self._button_states & button)

    @property
    def button_states(self):
        return self._button_states

    def axis_value(self, axis):
        return self._axis_values[axis]

    @property
    def axis_values(self):
        return tuple(self._axis_values)

    def has_axis_value_changed(self, axis, threshold=1):
        if axis not in (0, 1, 2, 3) or threshold < 0:
            return False
        delta = self._axis_change_deltas[axis]
        endpoint = self._axis_endpoint_events[axis]
        self._axis_change_deltas[axis] = 0
        self._axis_endpoint_events[axis] = False
        return delta > 0 and (endpoint or delta >= threshold)

    def set_remote_tx_power(self, tx_power, response=True):
        valid = (-16, -12, -8, -5, -3, -1, 0, 1, 2, 3, 4, 5, 6)
        if tx_power not in valid:
            raise ValueError("unsupported CodexPad transmit power")
        if self.connected_handle is None or self._tx_power_value_handle is None:
            return False
        try:
            self.ble.gattc_write(
                self.connected_handle, self._tx_power_value_handle,
                struct.pack("<b", tx_power), 1 if response else 0)
        except (OSError, ValueError) as error:
            self.last_error = "could not set transmit power: {}".format(error)
            return False
        return True

    def _reset_discovery(self):
        self._candidate = None
        self._scan_entries = {}
        self.device_name = None
        self.model = None
        self._service_ranges = {}
        self._service_queue = []
        self._service_index = -1
        self._current_service = None
        self._current_characteristics = []
        self._input_def_handle = None
        self._input_value_handle = None
        self._input_descriptor_end = None
        self._input_cccd_handle = None
        self._tx_power_value_handle = None
        self._ready = False

    def _start_scan(self, scan_ms):
        if self._state != "idle":
            return
        self._reset_discovery()
        self._reset_inputs()
        self._state = "scanning"
        print("CodexPad: scanning for", self.name_prefix)
        try:
            # ESP32 掌控板 1.0 uses the legacy three-argument API.
            self.ble.gap_scan(scan_ms, 30000, 30000)
        except (OSError, ValueError) as error:
            self.last_error = "could not start scan: {}".format(error)
            self._state = "idle"

    def _cancel_pending_operation(self):
        state = self._state
        if state in ("scanning", "cancelling_scan"):
            self._state = "cancelling_scan"
            try:
                self.ble.gap_scan(None)
            except (OSError, ValueError):
                self._state = "idle"
        elif state in ("connecting", "cancelling_connection"):
            self._state = "cancelling_connection"
            try:
                self.ble.gap_connect(None)
            except (OSError, TypeError, ValueError):
                self._state = "idle"
        elif self.connected_handle is not None:
            self._state = "disconnecting"
            try:
                self.ble.gap_disconnect(self.connected_handle)
            except (OSError, ValueError):
                self.connected_handle = None
                self._ready = False
                self._state = "idle"
        else:
            self._state = "idle"
        self._reset_inputs()

    def _fail(self, message):
        self.last_error = message
        self._ready = False
        self._reset_inputs()
        print("CodexPad:", message)
        if self.connected_handle is not None:
            self._state = "disconnecting"
            try:
                self.ble.gap_disconnect(self.connected_handle)
            except (OSError, ValueError):
                self.connected_handle = None
                self._state = "idle"
        else:
            self._state = "idle"

    def _next_service(self):
        self._service_index += 1
        if self._service_index >= len(self._service_queue):
            self._start_descriptor_discovery()
            return
        self._current_service = self._service_queue[self._service_index]
        self._current_characteristics = []
        start, end = self._service_ranges[self._current_service]
        self._state = "discovering_characteristics"
        try:
            self.ble.gattc_discover_characteristics(self.connected_handle, start, end)
        except (OSError, ValueError) as error:
            self._fail("could not discover characteristics: {}".format(error))

    def _save_characteristic(self, def_handle, value_handle, uuid):
        uuid = UUID(uuid)
        self._current_characteristics.append((def_handle, value_handle, uuid))
        if self._current_service == "inputs" and uuid == _INPUTS_CHARACTERISTIC_UUID:
            self._input_def_handle = def_handle
            self._input_value_handle = value_handle
        elif self._current_service == "tx_power" and uuid == _TX_POWER_CHARACTERISTIC_UUID:
            self._tx_power_value_handle = value_handle

    def _finish_characteristic_discovery(self):
        if self._current_service != "inputs" or self._input_value_handle is None:
            return
        descriptor_end = self._service_ranges["inputs"][1]
        for def_handle, value_handle, uuid in self._current_characteristics:
            if def_handle > self._input_def_handle:
                descriptor_end = min(descriptor_end, def_handle - 1)
        self._input_descriptor_end = descriptor_end

    def _start_descriptor_discovery(self):
        if self._input_value_handle is None:
            self._fail("inputs characteristic FFA1 not found")
            return
        start = self._input_value_handle
        if self._input_descriptor_end is None or start > self._input_descriptor_end:
            self._fail("inputs CCCD 2902 has no valid discovery range")
            return
        self._state = "discovering_descriptors"
        try:
            self.ble.gattc_discover_descriptors(
                self.connected_handle, start, self._input_descriptor_end)
        except (OSError, ValueError) as error:
            self._fail("could not discover inputs CCCD: {}".format(error))

    def _subscribe_inputs(self):
        if self._input_cccd_handle is None:
            self._fail("inputs CCCD 2902 not found")
            return
        self._state = "subscribing"
        try:
            self.ble.gattc_write(
                self.connected_handle, self._input_cccd_handle, b"\x01\x00", 1)
        except (OSError, ValueError) as error:
            self._fail("could not enable input notifications: {}".format(error))

    def _parse_inputs(self, data):
        if len(data) != 8:
            return
        previous_buttons = self._button_states
        previous_axes = tuple(self._axis_values)
        values = struct.unpack("<IBBBB", data)
        self._previous_button_states = previous_buttons
        self._button_states = values[0]
        self._pressed_events |= (~previous_buttons) & self._button_states
        self._released_events |= previous_buttons & (~self._button_states)
        for index in range(4):
            self._axis_values[index] = values[index + 1]
            delta = abs(self._axis_values[index] - previous_axes[index])
            if delta > self._axis_change_deltas[index]:
                self._axis_change_deltas[index] = delta
            if delta and self._axis_values[index] in (0, 255):
                self._axis_endpoint_events[index] = True
        if self._input_callback is not None:
            try:
                self._input_callback(self._button_states, tuple(self._axis_values))
                self.last_callback_error = None
            except Exception as error:
                self.last_callback_error = error
                print("CodexPad: input callback failed:", error)

    def _irq(self, event, data):
        if self.debug:
            print("CodexPad IRQ:", event, data)

        if event == IRQ.IRQ_SCAN_RESULT:
            addr_type, addr, adv_type, rssi, adv_data = data
            if self._state != "scanning":
                return
            addr = bytes(addr)
            name = _device_name(adv_data)
            advertised = _advertised_state(adv_data)
            entry = self._scan_entries.get(addr)
            if entry is None:
                entry = [addr_type, None, None, None, None]
                self._scan_entries[addr] = entry
            if name is not None:
                entry[1] = name
            if advertised is not None:
                entry[2], entry[3], entry[4] = advertised
            if entry[1] is None or not entry[1].startswith(self.name_prefix):
                return
            if self._button_mask is not None and entry[2] != self._button_mask:
                return
            if self._button_mask is not None and entry[3] is not None:
                if entry[3] > 1 and (entry[4] is None or entry[4] < 1):
                    return
            if self._candidate is None or rssi > self._candidate[3]:
                self._candidate = (entry[0], addr, entry[1], rssi)

        elif event == IRQ.IRQ_SCAN_DONE:
            if self._state == "cancelling_scan":
                self._state = "idle"
                return
            if self._state != "scanning":
                return
            if self._candidate is None:
                self.last_error = "CodexPad not found"
                self._state = "idle"
                return
            addr_type, addr, name, rssi = self._candidate
            self.device_name = name.decode("utf-8", "ignore")
            self.model = self.device_name
            self._state = "connecting"
            print("CodexPad: found", self.device_name, "RSSI", rssi)
            try:
                self.ble.gap_connect(addr_type, addr)
            except (OSError, ValueError) as error:
                self._fail("could not start connection: {}".format(error))

        elif event == IRQ.IRQ_PERIPHERAL_CONNECT:
            conn_handle, addr_type, addr = data
            if self._state == "cancelling_connection":
                self.connected_handle = conn_handle
                self._state = "disconnecting"
                try:
                    self.ble.gap_disconnect(conn_handle)
                except (OSError, ValueError):
                    self.connected_handle = None
                    self._state = "idle"
                return
            if self._state != "connecting":
                return
            self.connected_handle = conn_handle
            self._state = "discovering_services"
            print("CodexPad: connected, discovering GATT")
            try:
                self.ble.gattc_discover_services(conn_handle)
            except (OSError, ValueError) as error:
                self._fail("could not discover services: {}".format(error))

        elif event == IRQ.IRQ_PERIPHERAL_DISCONNECT:
            conn_handle, addr_type, addr = data
            if self._state == "cancelling_connection" and self.connected_handle is None:
                self._state = "idle"
                self._retry_at = time.ticks_add(time.ticks_ms(), 1000)
                return
            if conn_handle != self.connected_handle:
                return
            was_ready = self._ready
            was_disconnecting = self._state == "disconnecting"
            self.connected_handle = None
            self._ready = False
            self._state = "idle"
            self._retry_at = time.ticks_add(time.ticks_ms(), 1000)
            self._reset_inputs()
            if not was_ready and not was_disconnecting and self.last_error is None:
                self.last_error = "disconnected before driver was ready"
            if was_ready and self._auto_reconnect:
                print("CodexPad: disconnected; reconnect scheduled")
            elif was_ready:
                print("CodexPad: disconnected")

        elif event == IRQ.IRQ_GATTC_SERVICE_RESULT:
            conn_handle, start, end, uuid = data
            if conn_handle != self.connected_handle:
                return
            uuid = UUID(uuid)
            if uuid == _INPUTS_SERVICE_UUID:
                self._service_ranges["inputs"] = (start, end)
            elif uuid == _TX_POWER_SERVICE_UUID:
                self._service_ranges["tx_power"] = (start, end)

        elif event == IRQ.IRQ_GATTC_SERVICE_DONE:
            conn_handle, status = data
            if conn_handle != self.connected_handle:
                return
            if status != 0:
                self._fail("service discovery failed: {}".format(status))
                return
            self._service_queue = []
            for service in ("inputs", "tx_power"):
                if service in self._service_ranges:
                    self._service_queue.append(service)
            self._service_index = -1
            self._next_service()

        elif event == IRQ.IRQ_GATTC_CHARACTERISTIC_RESULT:
            conn_handle, def_handle, value_handle, properties, uuid = data
            if conn_handle == self.connected_handle:
                self._save_characteristic(def_handle, value_handle, uuid)

        elif event == IRQ.IRQ_GATTC_CHARACTERISTIC_DONE:
            conn_handle, status = data
            if conn_handle != self.connected_handle:
                return
            if status != 0:
                self._fail("characteristic discovery failed: {}".format(status))
                return
            self._finish_characteristic_discovery()
            self._next_service()

        elif event == IRQ.IRQ_GATTC_DESCRIPTOR_RESULT:
            conn_handle, descriptor_handle, uuid = data
            if conn_handle != self.connected_handle or self._state != "discovering_descriptors":
                return
            if UUID(uuid) == _CCCD_UUID and self._input_cccd_handle is None:
                self._input_cccd_handle = descriptor_handle

        elif event == IRQ.IRQ_GATTC_DESCRIPTOR_DONE:
            conn_handle, status = data
            if conn_handle != self.connected_handle or self._state != "discovering_descriptors":
                return
            if status != 0:
                self._fail("descriptor discovery failed: {}".format(status))
                return
            self._subscribe_inputs()

        elif event == IRQ.IRQ_GATTC_WRITE_DONE:
            conn_handle, value_handle, status = data
            if conn_handle != self.connected_handle or self._state != "subscribing":
                return
            if value_handle != self._input_cccd_handle:
                return
            if status != 0:
                self._fail("could not enable input notifications: {}".format(status))
                return
            self._state = "ready"
            self._ready = True
            self.last_error = None
            print("CodexPad: ready, device={}".format(self.device_name))

        elif event == IRQ.IRQ_GATTC_NOTIFY:
            conn_handle, value_handle, notify_data = data
            if conn_handle == self.connected_handle and value_handle == self._input_value_handle:
                self._parse_inputs(bytes(notify_data))
