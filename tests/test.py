from airtest.core.api import *
from popupSurprise import CommonCase
from airtest.core.api import *
from poco.drivers.unity3d import UnityPoco
# dev1=connect_device("android://127.0.0.1:5037/emulator-5554")

class test(CommonCase):
    pass
haha=test()
print(haha.say())

poco=UnityPoco()


btn= (Template(r"tpl1744710026776.png", record_pos=(-0.391, -0.544), resolution=(900, 1800)))
touch(btn)


btnBuy=poco("ElementPack2").child("Btn_WatchAds")
btnBuy.click()

