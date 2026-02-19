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
from tests.cozy.level_play_util import *
from cozy.ingame_popup import *


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


    def test_tempt(self):
        result=self.poco.invoke("get_normalized_position", x=-4.68, y =1.285)
        print(result)

    def test_cozy(self):
        logger=get_logger("CozyPlay")
        parent_mapping=self.poco.invoke("get_parent_mapping")
        parent_mapping= parent_mapping['parent_mapping']
        spawnable_items= get_spawnable_items(self.poco)
        for i in range(len(spawnable_items)):
            self.poco("box_spawner").click()
            sleep(1)
            snapZone = self.poco.invoke("get_list_snap_zone")
            snapZone = snapZone['snap_zones']
            print(f"snapZone: {snapZone}")
            floating_items = self.poco.invoke("get_floating_objs")
            floating_items = floating_items['floating_objs']
            print(f"float_item: {floating_items}")
            if spawnable_items[i] not in floating_items:
                logger.warning(f"spawnable_item: {spawnable_items[i]} not in floating_items")
                raise TargetNotFoundError(f"Cannot find {spawnable_items[i]}")
            target_item_pos_list = []
            for itemFloat in floating_items:
                for itemSnapZone in snapZone:
                    if itemFloat == itemSnapZone['item_identifier']:
                        pos = itemSnapZone['position']
                        norm_pos = (pos['x'], pos['y'])
                        target_item_pos_list.append((itemFloat, norm_pos))
                        continue
            print(f"target_item_pos_list: {target_item_pos_list}")
            target_item_norm_pos_list = []
            for item, pos in target_item_pos_list:
                norm_pos = self.poco.invoke("get_normalized_position", x=pos[0], y=pos[1])
                norm_pos = norm_pos['normalized_pos']
                target_item_norm_pos_list.append((item, norm_pos))
                result_placed_objs = self.poco.invoke("get_placed_objs")
                placedObjs = result_placed_objs['placed_objs']
                needWait= is_wait_for_parent_place(item, parent_mapping, placedObjs)
                if needWait:
                    print(f"waiting for parent place for item: {item} ....")
                    break
            print(f"target_item_norm_pos_list: {target_item_norm_pos_list}")
            for item, norm_pos in reversed(target_item_norm_pos_list):
                obj = self.poco(item)
                result= self.poco.invoke("check_small_and_get_normalized_position", objName=item)
                if result['status']== True:
                    adjusted_pos= result['normalized_pos']
                    print(f"{item} is small, need to adjust coordinate from {norm_pos} to {adjusted_pos}")
                    norm_pos= adjusted_pos
                print(f"obj: {item}, target_norm_pos: {norm_pos}")
                # obj.drag_to(norm_pos, duration=0.2)
                swipe(obj.get_position(), norm_pos, duration=0.3)
                print(f"drag_to obj: {item}, obj_pos: {norm_pos}")

    def test_lv3_cozy(self):
        def handle_hint_tut():
            popup=self.poco("PopupTutorialBooster")
            if wait_for_element(popup, timeout=10):
                print("Found PopupTutorialBooster, handling tutorial hint...")
                btn_claim= popup.offspring("B_Claim")
                btn_claim.click(sleep_interval=1)
            #### check img hand tut
            btn_hint=self.poco("BoosterButton").offspring("Hint")
            btn_hint.click(sleep_interval=1)
        logger = get_logger("CozyPlay")
        parent_mapping = self.poco.invoke("get_parent_mapping")
        parent_mapping = parent_mapping['parent_mapping']
        spawnable_items = get_spawnable_items(self.poco)
        for i in range(len(spawnable_items)):
            self.poco("box_spawner").click()
            sleep(1)
            if i==0:
                handle_hint_tut()
                continue
            snapZone = self.poco.invoke("get_list_snap_zone")
            snapZone = snapZone['snap_zones']
            print(f"snapZone: {snapZone}")
            floating_items = self.poco.invoke("get_floating_objs")
            floating_items = floating_items['floating_objs']
            print(f"float_item: {floating_items}")
            # if spawnable_items[i] not in floating_items:
            #     logger.warning(f"spawnable_item: {spawnable_items[i]} not in floating_items")
            #     raise TargetNotFoundError(f"Cannot find {spawnable_items[i]}")
            target_item_pos_list = []
            for itemFloat in floating_items:
                for itemSnapZone in snapZone:
                    if itemFloat == itemSnapZone['item_identifier']:
                        pos = itemSnapZone['position']
                        norm_pos = (pos['x'], pos['y'])
                        target_item_pos_list.append((itemFloat, norm_pos))
                        continue
            print(f"target_item_pos_list: {target_item_pos_list}")
            target_item_norm_pos_list = []
            for item, pos in target_item_pos_list:
                norm_pos = self.poco.invoke("get_normalized_position", x=pos[0], y=pos[1])
                norm_pos = norm_pos['normalized_pos']
                target_item_norm_pos_list.append((item, norm_pos))
                result_placed_objs = self.poco.invoke("get_placed_objs")
                placedObjs = result_placed_objs['placed_objs']
                needWait = is_wait_for_parent_place(item, parent_mapping, placedObjs)
                if needWait:
                    print(f"waiting for parent place for item: {item} ....")
                    break
            print(f"target_item_norm_pos_list: {target_item_norm_pos_list}")
            for item, norm_pos in reversed(target_item_norm_pos_list):
                obj = self.poco(item)
                result = self.poco.invoke("check_small_and_get_normalized_position", objName=item)
                if result['status'] == True:
                    adjusted_pos = result['normalized_pos']
                    print(f"{item} is small, need to adjust coordinate from {norm_pos} to {adjusted_pos}")
                    norm_pos = adjusted_pos
                print(f"obj: {item}, target_norm_pos: {norm_pos}")
                # obj.drag_to(norm_pos, duration=0.2)
                swipe(obj.get_position(), norm_pos, duration=0.3)
                print(f"drag_to obj: {item}, obj_pos: {norm_pos}")













