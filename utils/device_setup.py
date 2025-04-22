from airtest.core.api import connect_device
from poco.drivers.unity3d import UnityPoco

def connect_to_unity():
    # Connect to Unity plugin
    dev = connect_device("android://127.0.0.1:5037/emulator-5554")
    print(f"Connected to Unity device: {dev}")
    return UnityPoco()
# import sys
# print("path:"+sys.executable)