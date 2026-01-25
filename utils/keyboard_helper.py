# keyboard_helper.py
"""
Cross-platform keyboard input helper for game automation.

Supports:
- Android  : Airtest keyevent
- Windows  : win32api keybd_event (Unity Editor / PC build)

Usage:
    from keyboard_helper import press_key

    press_key(poco, "ESC")
    press_key(poco, "T")
"""

import time


# -------------------------
# Platform detection
# -------------------------
def _detect_platform(poco):
    device = getattr(poco, "device", None)
    if device is None:
        raise Exception("Poco device not found")

    device_uri = str(device).lower()

    if "android" in device_uri:
        return "android"
    if "windows" in device_uri:
        return "windows"

    raise Exception(f"Unsupported device for test: {device}")


# -------------------------
# Android implementation
# -------------------------
def _press_key_android(key):
    from airtest.core.api import keyevent
    KEY_ALIAS  = {
        "UP": "DPAD_UP",
        "DOWN": "DPAD_DOWN",
        "LEFT": "DPAD_LEFT",
        "RIGHT": "DPAD_RIGHT",
    }
    if key in KEY_ALIAS:
        key = KEY_ALIAS[key]
    keyevent(key)


# -------------------------
# Windows implementation
# -------------------------
def _press_key_windows(key, hold=0.05):
    key = key.upper()

    # Letters A–Z → raw VK
    if len(key) == 1 and "A" <= key <= "Z":
        import win32api
        import win32con

        vk = ord(key)
        win32api.keybd_event(vk, 0, 0, 0)
        time.sleep(hold)
        win32api.keybd_event(vk, 0, win32con.KEYEVENTF_KEYUP, 0)
        return

    # Special keys → SendKeys
    from pywinauto.keyboard import SendKeys

    SPECIAL_MAP = {
        "BACK": "{ESC}",
        "ENTER": "{ENTER}",
        "SPACE": "{SPACE}",
        "UP": "{UP}",
        "DOWN": "{DOWN}",
        "LEFT": "{LEFT}",
        "RIGHT": "{RIGHT}",
    }

    if key not in SPECIAL_MAP:
        raise ValueError(f"Unsupported key on Windows: {key}")

    SendKeys(SPECIAL_MAP[key])



# -------------------------
# Public API
# -------------------------
def press_key(poco, key):
    """
    Press a keyboard key on current platform.

    Args:
        poco: Poco instance
        key : str, e.g. "T", "ESC", "UP", "DOWN"
    """
    platform = _detect_platform(poco)

    if platform == "android":
        _press_key_android(key)
    elif platform == "windows":
        _press_key_windows(key)
    else:
        raise Exception(f"Unsupported platform: {platform}")
