import threading

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
from utils.campaignLv_playing_helper2 import   *

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
        frozen_ingame_UI = UI_Ingame(self.poco.freeze())
        first_move = False
        stats={
            "collected_gold": 0,
            "collected_gem": 0,
            "stop":False
        }
        def autoplay_thread():
            print("1111..")
            nonlocal first_move
            print("2222..")
            while not stats["stop"]:
                print("3333.. into while loop")
                do_autoplay_action(self.poco, first_move, frozen_ingame_UI)
                first_move = True  # Set to True after first execution
        def stats_thread():
            while not stats["stop"]:
                gold,gem= stats_poller(self.poco,stats["collected_gold"],stats["collected_gem"])
                stats["collected_gold"]= gold
                stats["collected_gem"]= gem
                sleep(0.5)
        autoplay_thread_obj=threading.Thread(target=autoplay_thread)
        stats_thread_obj=threading.Thread(target=stats_thread)
        autoplay_thread_obj.start()
        stats_thread_obj.start()
        try:
            # Let them run for a specific duration (e.g., 60 seconds)
            sleep(60)
        finally:
            # Stop both threads
            stats["stop"] = True
            autoplay_thread_obj.join()
            stats_thread_obj.join()

            # Print final stats
            print(f"Final collected gold: {stats['collected_gold']}")
            print(f"Final collected gem: {stats['collected_gem']}")
    def test_new(self):
        # normal_lv_play(self.poco, target_lv=22, mode="normal", logger_name="hehehehhe LV3")
        # rate= PopupRate(self.poco.freeze())
        # print(f"rate btn exists: {rate.root}")
        lv_list= [2,8]
        multiple_normal_lv_play(self.poco, lv_list)






def do_autoplay_action(poco,first_move, frozen_ingame_UI):
    print("doing autoplay action...")
    initial_plane_pos = (227, 819)  # Player character position
    btn_skill= frozen_ingame_UI.btn_plane_skill
    btn_skill_pos= btn_skill.get_position()
    start_pos = ((initial_plane_pos[0] - btn_skill_pos[0]) / 2 + btn_skill_pos[0], initial_plane_pos[1])
    end_pos = (initial_plane_pos[0] + (initial_plane_pos[0] - start_pos[0]), initial_plane_pos[1])
    if not first_move:
        # Initial setup: press P to level up plane , swipe  to start moving
        for i in range(30):
            press_key(poco, "P")
        swipe(initial_plane_pos, start_pos)  # Move to starting position
        # press_key(poco, "UP")
        first_move = True
    press_key(poco, "T")
    swipe(start_pos, end_pos, duration=1)
    print("swipeeeing...")
    sleep(1)
    swipe(end_pos, start_pos, duration=1)
    print("swipeeeeee2222...")

def stats_poller(poco,collected_gold,collected_gem):
    UI_tmp = UITop(poco.freeze())
    tmp = UI_tmp.collected_gold
    collected_gold = max(collected_gold, tmp) if tmp else collected_gold
    tmp_gem = UI_tmp.collected_gem
    collected_gem = max(collected_gem, tmp_gem) if tmp_gem else collected_gem
    print(f"polling collected_gold: {collected_gold}, collected_gem: {collected_gem}")
    return collected_gold,collected_gem






