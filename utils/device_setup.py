from airtest.core.api import connect_device
from poco.drivers.unity3d import UnityPoco
# from utils.patched_unity_poco import UnityPoco

def connect_to_unity():
    # Connect to Unity plugin
    dev = connect_device("android://127.0.0.1:5037/emulator-5554")
    print(f"Connected to Unity device: {dev}")
    return UnityPoco()

class PocoManager:
    _poco = None

    @classmethod
    def   get_poco(cls):
        if cls._poco is None:
            connect_device("android://127.0.0.1:5037/emulator-5554")
            cls._poco = UnityPoco()
        return cls._poco
# import sys
# print("path:"+sys.executable)