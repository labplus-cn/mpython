# CodexPad ESP32 掌控板 1.0 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a native MicroPython CodexPad C10/S10 BLE Central driver to the ESP32 掌控板 1.0 filesystem without changing the existing generic `Centeral` API.

**Architecture:** Add a focused `CodexPad` class beside the legacy BLE applications. It owns one `bluetooth.BLE().irq()` handler, scans `CodexPad-` advertisements, selects the strongest matching candidate, discovers `FFA0/FFA1` and the input CCCD `2902`, subscribes to notifications, and parses the 8-byte report. The implementation will use the old port's three-argument `gap_scan(duration_ms, interval_us, window_us)` API while retaining the same public input properties and button/axis constants as the ESP32-S3 driver.

**Tech Stack:** MicroPython `bluetooth.BLE`, legacy `mpython_ble.application`, ESP32 NimBLE GATT Central APIs, host-side Python static/behavior tests.

## Global Constraints

- Preserve `mpython_ble.application.Centeral`, `BLEUART`, `HID`, and their import behavior.
- Use `gap_scan(duration_ms, interval_us, window_us)`; do not pass the ESP32-S3-only fourth active-scan argument.
- Discover the CCCD dynamically; never assume descriptor adjacency or a fixed handle.
- Support only the CodexPad custom BLE protocol used by C10/S10; do not add `aioble` or classic Bluetooth HID dependencies.
- Keep one BLE IRQ owner per `CodexPad` object and expose automatic reconnect through `poll()`.

---

### Task 1: Define the legacy-port CodexPad contract test

**Files:**
- Create: `port/tests/test_codexpad_contract.py`
- Test: `port/tests/test_codexpad_contract.py`

**Interfaces:**
- Consumes: the future `port/file_system/mpython_ble/application/codexpad.py` source and `application/__init__.py` export.
- Produces: deterministic host checks for old BLE call signatures, UUIDs, constants, public API, and example presence.

- [ ] **Step 1: Write the failing source contract test**

Assert the driver source contains the `CodexPad` class, `FFA0`, `FFA1`, `2902`, all public button/axis constants, `connect`, `scan_and_connect`, `poll`, `disconnect`, and a three-argument `gap_scan` call. Assert `application/__init__.py` exports `CodexPad` and the example imports it.

- [ ] **Step 2: Run the test and verify it fails**

Run: `python port/tests/test_codexpad_contract.py`

Expected: FAIL because `codexpad.py`, its export, and the example do not exist yet.

- [ ] **Step 3: Commit the failing test**

```powershell
git add port/tests/test_codexpad_contract.py
git commit -m "test: define ESP32 CodexPad driver contract"
```

### Task 2: Port the CodexPad BLE Central driver

**Files:**
- Create: `port/file_system/mpython_ble/application/codexpad.py`
- Modify: `port/file_system/mpython_ble/application/__init__.py`
- Test: `port/tests/test_codexpad_contract.py`

**Interfaces:**
- Consumes: legacy `IRQ` values and `bluetooth.BLE` APIs from `mpython_ble.const` and the old MicroPython port.
- Produces: `CodexPad`, `BUTTON_*`, `AXIS_*`, `TX_POWER_*`, `AXIS_CENTER`; `connect(timeout_ms=20000, scan_ms=5000)`, `scan_and_connect(button_mask, timeout_ms=20000, scan_ms=5000)`, `poll()`, `disconnect()`, `is_connected()`, `is_ready()`, `on_input(callback)`, button and axis properties.

- [ ] **Step 1: Copy the protocol parsing structure from the S3 driver**

Keep the 8-byte `<IBBBB` input report, manufacturer-data mask matching, edge-event accumulation, and dynamic service/characteristic/descriptor state machine. Import `IRQ` from the old port and use the existing numeric event values.

- [ ] **Step 2: Adapt all legacy BLE calls**

Use `self.ble.gap_scan(scan_ms, 30000, 30000)` for starting scans and `self.ble.gap_scan(None)` for stopping. Keep `gattc_discover_services`, `gattc_discover_characteristics`, `gattc_discover_descriptors`, and `gattc_write(..., b"\\x01\\x00", 1)` compatible with the old port.

- [ ] **Step 3: Add explicit failure and reconnect behavior**

Return `False` with `last_error` on scan/GATT failures, cancel pending operations on timeout, call `_start_scan(5000)` from `poll()` after disconnect, and expose the same read-and-clear `pressed`/`released` and axis-change properties as the S3 driver.

- [ ] **Step 4: Export the driver**

Add `from .codexpad import CodexPad` after `Centeral` in the application package initializer without changing existing imports.

- [ ] **Step 5: Run the contract test**

Run: `python port/tests/test_codexpad_contract.py`

Expected: PASS with the driver source, export, and legacy scan signature validated.

- [ ] **Step 6: Commit the driver**

```powershell
git add port/file_system/mpython_ble/application/codexpad.py port/file_system/mpython_ble/application/__init__.py port/tests/test_codexpad_contract.py
git commit -m "feat: add CodexPad driver for ESP32 mPython"
```

### Task 3: Add a minimal ESP32 1.0 usage example and static validation

**Files:**
- Create: `port/file_system/mpython_ble/codexpad_example.py`
- Modify: `port/tests/test_codexpad_contract.py`

**Interfaces:**
- Consumes: `CodexPad`, `BUTTON_START`, `BUTTON_CROSS_A`, button and axis properties.
- Produces: a copyable filesystem example that demonstrates normal scan, optional exact button-mask selection, polling, and read-and-clear events.

- [ ] **Step 1: Add the example**

Import `CodexPad` and constants, connect with a timeout, print the selected device, call `pad.poll()` in a loop, and print button/axis changes. Keep the example free of `aioble`, `asyncio`, and address-specific assumptions.

- [ ] **Step 2: Extend the contract test**

Assert the example imports the legacy package, calls `connect()` and `poll()`, and documents `scan_and_connect(BUTTON_START | BUTTON_CROSS_A)` as the multi-controller selection path.

- [ ] **Step 3: Run static checks**

Run:

```powershell
python port/tests/test_codexpad_contract.py
python -m py_compile port/tests/test_codexpad_contract.py
git diff --check
```

Expected: all commands exit 0. A host Python compile is only a syntax check; it does not prove hardware BLE behavior.

- [ ] **Step 4: Commit the example**

```powershell
git add port/file_system/mpython_ble/codexpad_example.py port/tests/test_codexpad_contract.py
git commit -m "docs: add ESP32 CodexPad usage example"
```

### Task 4: Verify packaging and report hardware boundary

**Files:**
- Verify: `port/Makefile`, `port/make_lfs.py`, `port/file_system/mpython_ble/application/`
- Verify: `port/file_system/mpython_ble/codexpad_example.py`

**Interfaces:**
- Consumes: the committed driver and example.
- Produces: evidence that the VFS filesystem packaging picks up the new files and a clear hardware test boundary.

- [ ] **Step 1: Confirm VFS inclusion**

Verify `VFS_DIR ?= file_system` remains unchanged and the new files are under that tree, so no manifest change is required.

- [ ] **Step 2: Run final repository checks**

Run the contract test, `py_compile`, `git diff --check`, and `git status --short`. Do not claim a firmware build or hardware connection without running it on the ESP32 掌控板 1.0.

- [ ] **Step 3: Report acceptance boundary**

Report static/API validation separately from pending physical validation: scan, GATT discovery, CCCD subscription, notification parsing, button-mask selection, reconnect, and simultaneous-controller behavior require a real ESP32 掌控板 1.0 and C10/S10.

