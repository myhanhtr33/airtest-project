# from popupSurprise import CommonCase
# from airtest.core.api import *

# class test(CommonCase):
#     pass
# haha=test()
# print(haha.say())

# print("Test class defined")
# haha = test()
# print("Test instance created")
# result = haha.say()
# print(f"say() returned: {result}")
# print(f"Printing: {result}")


# from airtest.core.api import *

# auto_setup(__file__)
# from airtest.core.api import *
# from airtest.core.settings import Settings as ST
# import threading
# import time
# import sys
# import datetime
# from concurrent.futures import ThreadPoolExecutor
# import os
# # from poco.drivers.unity3d import UnityPoco
# # poco = UnityPoco()
# ST.THRESHOLD = 0.6 #do chinh xac de tim ra 1 anh
# ST.THRESHOLD_STRICT = 0.6
# ST.OPDELAY = 0.1# giam thoi gian chuyen giua lenh
# ST.FIND_TIMEOUT = 1

# # dev1=connect_device("android://127.0.0.1:5037/emulator-5554")
# btn= (Template(r"tpl1744710026776.png", record_pos=(-0.391, -0.544), resolution=(900, 1800)))
# touch(btn)
import time
from poco.drivers.unity3d import UnityPoco

from pocounit.case import PocoTestCase
from pocounit.addons.poco.action_tracking import ActionTracker
# from pocounit.addons.hunter.runtime_logging import AppRuntimeLogging

from airtest.core.api import *
from popupSurprise import CommonCase
from airtest.core.api import *
dev1=connect_device("android://127.0.0.1:5037/emulator-5554")
poco = UnityPoco()

class test(CommonCase):
    pass
haha=test()
print(haha.say())

btn= (Template(r"tpl1744710026776.png", record_pos=(-0.391, -0.544), resolution=(900, 1800)))
touch(btn)
sleep(1)


btnBuy=poco("ElementPack2").child("Btn_WatchAds")
btnBuy.click()