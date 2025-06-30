from airtest.core.api import connect_device
from poco.drivers.unity3d import UnityPoco
# from utils.patched_unity_poco import UnityPoco
from poco.drivers.android.uiautomation import AndroidUiautomationPoco

# dev= "android://127.0.0.1:5037/emulator-5554" # Default emulator, can be changed to another device
dev="android://127.0.0.1:5037/emulator-5562"
def connect_to_unity():
    # Connect to Unity plugin
    # dev = connect_device("android://127.0.0.1:5037/emulator-5554") # Default emulator
    connect_device(dev)
    print(f"Connected to Unity device: {dev}")
    return UnityPoco()

class PocoManager:
    _poco = None
    _pocoAndroid = None
    @classmethod
    def   get_poco(cls):
        if cls._poco is None:
            connect_device(dev)
            cls._poco = UnityPoco()
        return cls._poco
    @classmethod
    def get_pocoAndroid(cls):
        if cls._pocoAndroid is None:
            cls._pocoAndroid = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False)
        return cls._pocoAndroid


# import sys
# print("path:"+sys.executable)