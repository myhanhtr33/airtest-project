from airtest.core.api import connect_device
from poco.drivers.unity3d import UnityPoco
from airtest.core.api import *

auto_setup(__file__)





from poco.drivers.android.uiautomation import AndroidUiautomationPoco
poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False)
from airtest.core.api import *
from airtest.core.settings import Settings as ST
import threading
import time
import sys
import datetime
import os
dev1=connect_device("android://127.0.0.1:5037/emulator-5554")
# dev2= UnityEditorWindow()
# addr= ('',5001)
# poco = UnityPoco(addr, device=dev2
poco=UnityPoco()
def result(result):
    with open("result.txt", "a") as f:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Format datetime as string
        f.write(timestamp + " " + result + "\n")  # Concatenate properly
# btn=exists(Template(r"tpl1743741088741.png", record_pos=(-0.386, -0.538), resolution=(900, 1800)));
# click(btn,times=2);
btn1=poco("BtnSuprisePack")
print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+"clickkkkkkk")
print(f"Button is{'enabled' if btn1.attr('enabled') else 'disabled'}")
btn1.click(sleep_interval=3)
if poco("PopupSuprisePack(Clone)").exists():
    result("click success")


#poco("ElementPack1").offspring("Btn_Active (1)")
else:
    result("PopupSuprisePack do not showup")
print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+"after clickkkkkkk")
print(f"Button is{'enabled' if btn1.attr('enabled') else 'disabled'}")

# from popupSurprise import CommonCase
# from airtest.core.api import *

# class test(CommonCase):
#     pass
# haha=test()
# print(haha.say())



