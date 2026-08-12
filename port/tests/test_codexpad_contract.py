"""Static contract checks for the ESP32 mPython CodexPad driver."""

from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[2]
DRIVER = ROOT / "port" / "file_system" / "mpython_ble" / "application" / "codexpad.py"
INIT = ROOT / "port" / "file_system" / "mpython_ble" / "application" / "__init__.py"
EXAMPLE = ROOT / "port" / "file_system" / "mpython_ble" / "codexpad_example.py"


def contains(text, needle, label):
    if needle not in text:
        raise AssertionError("{} missing {!r}".format(label, needle))


def main():
    driver = DRIVER.read_text(encoding="utf-8")
    init = INIT.read_text(encoding="utf-8")
    example = EXAMPLE.read_text(encoding="utf-8")

    for needle in (
        "class CodexPad(object):",
        "UUID(0xFFA0)",
        "UUID(0xFFA1)",
        "UUID(0x2902)",
        "gattc_discover_descriptors",
        "b\"\\x01\\x00\"",
        "def connect(self, timeout_ms=20000, scan_ms=5000):",
        "def scan_and_connect(self, button_mask, timeout_ms=20000, scan_ms=5000):",
        "def poll(self):",
        "def disconnect(self):",
        "def is_ready(self):",
        "def pressed(self, button):",
        "def released(self, button):",
        "def has_axis_value_changed(self, axis, threshold=1):",
    ):
        contains(driver, needle, "codexpad.py")

    for name in (
        "BUTTON_UP", "BUTTON_DOWN", "BUTTON_LEFT", "BUTTON_RIGHT",
        "BUTTON_SQUARE_X", "BUTTON_TRIANGLE_Y", "BUTTON_CROSS_A",
        "BUTTON_CIRCLE_B", "BUTTON_L1", "BUTTON_L2", "BUTTON_L3",
        "BUTTON_R1", "BUTTON_R2", "BUTTON_R3", "BUTTON_SELECT",
        "BUTTON_START", "BUTTON_HOME", "AXIS_LEFT_STICK_X",
        "AXIS_LEFT_STICK_Y", "AXIS_RIGHT_STICK_X", "AXIS_RIGHT_STICK_Y",
        "AXIS_CENTER", "TX_POWER_0_DBM",
    ):
        contains(driver, name, "codexpad.py public constants")

    scan_calls = re.findall(r"self\.ble\.gap_scan\(([^\n]+)\)", driver)
    if not any("scan_ms, 30000, 30000" in call for call in scan_calls):
        raise AssertionError("codexpad.py must use the legacy three-argument gap_scan")
    if any(call.rstrip().endswith(", True") for call in scan_calls):
        raise AssertionError("codexpad.py must not pass the S3-only active-scan argument")

    contains(init, "from .codexpad import CodexPad", "application/__init__.py")
    for needle in (
        "from mpython_ble.application import CodexPad",
        "pad.connect(",
        "pad.poll()",
        "BUTTON_START | BUTTON_CROSS_A",
    ):
        contains(example, needle, "codexpad_example.py")

    print("ESP32 mPython CodexPad driver contract passed")


if __name__ == "__main__":
    main()
