from Hierarchy.PopupMilitary import *
from utils.device_setup import PocoManager
from airtest.core.api import *

def test_military_popup():
    poco = PocoManager.get_poco()
    popup = PopupMilitary(poco)
    level = popup.level_text
    print(f"before click: {popup.level_text}")
    poco("BtnUpdate").click()
    for i in range(5):
        print(f"{i} after click LEVEL: {popup.level_text}")
        time.sleep(0.5)

