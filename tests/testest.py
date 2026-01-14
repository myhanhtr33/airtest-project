from Hierarchy.PopupCampaignSelectLv import PopupCampaignSelectLv
from Hierarchy.Tutorial_UI import *
from Hierarchy.UI_ingame import *
from Hierarchy.HOME_Element import *
from utils.test_level_helper import *
import os
import pytest
from logger_config import get_logger
from utils.helper_functions import wait_for_element
from utils.test_level_helper import *
from utils.get_resource_amount import *
from airtest.core.api import swipe, sleep, wait, keyevent, Template
from airtest.core.error import TargetNotFoundError
from utils.keyboard_helper import press_key
from pywinauto.keyboard import SendKeys
from utils.campaignLv_playing_helper import *

current_dir=os.path.dirname(os.path.abspath(__file__))
img_path= os.path.join(os.path.dirname(current_dir),"image","Plane1_bata.png")
bata_img = Template(img_path)

img_path= os.path.join(os.path.dirname(current_dir),"image","Handtut.png")
hand_tut_img = Template(img_path)
img_path= os.path.join(os.path.dirname(current_dir),"image","tutLv_noti_frame.png")
ingame_noti_img = Template(img_path)


def notfound():
    print("No target found")
    return None

class TestIngameeee:
    @pytest.fixture(scope="function", autouse=True)
    def setup(cls,poco):
        cls.poco= poco
        poco_freeze= poco.freeze()
        device=getattr(poco, 'device', None)
        print(f"pococococo freeze device: {str(device)}")
        device_uri= str(device)
        if "android" in device_uri.lower():
            #### use keyevent from airtest API
            pass
        elif "windows" in device_uri.lower():
            #### use win32api to send keyevent
            pass
        else:
            raise Exception(f"Unsupported device for test: {device_uri}")



    def test_scroll(self):
        # from pocounit.case import *
        # sleep(2)
        target_level= 9
        from_home_to_campaign_select(self.poco, "leuleuleu")
        play_and_verify_level(self.poco, target_level, "leuleuleu")








