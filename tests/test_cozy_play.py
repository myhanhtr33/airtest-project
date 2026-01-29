import pytest
from logger_config import get_logger
from utils.helper_functions import wait_for_element
from utils.test_level_helper import *
from utils.get_resource_amount import *
from airtest.core.api import swipe, sleep, wait, keyevent, Template
from airtest.core.error import TargetNotFoundError
from utils.keyboard_helper import press_key
from pywinauto.keyboard import SendKeys
from tests.cozy.level_play_util import *

class TestCozyPlay:
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

    def test_invoke(self):
        result= self.poco.invoke("get_level_data")
        level_data_phases= result['level_data']['phases']
        level_data= level_data_phases[0]['groups']
        print(level_data)
        print(f"count items in group={len(level_data)}")
        spawn_exceptions= result['spawn_exceptions']
        spawnable_item=[]
        for i in level_data:
            if i['items'] not in spawn_exceptions:
                spawnable_item.append(i['items'])
        print(f"spawnable_item={spawnable_item}")
        print(f"count spawnable_item={len(spawnable_item)}")
    def test_drag(self):
        name="goi"
        sleep(0.5)
        result= self.poco.invoke("check_small_and_get_normalized_position", objName=name)
        print(result)
        print(result['status'])
        if(result['status']==False):
            print(f"{name} is not small")
        # target_pos=result["normalized_pos"]
        # target_pos = result.get("normalized_pos")
        # print(f"before normalized_pos={target_pos} (type={type(target_pos).__name__})")
        # if isinstance(target_pos, (list, tuple)):
        #     target_pos = tuple(float(x) for x in target_pos)
        # else:
        #     try:
        #         target_pos = tuple(map(float, target_pos))
        #     except Exception:
        #         raise ValueError(f"Invalid normalized_pos: {result!r}")
        # print(f"normalized_pos={target_pos} (type={type(target_pos).__name__})")
        # lamp= self.poco(name)
        # sleep(1)
        # lamp.focus([0.5, 0.8]).click()

    def test_apk(self):
        name="pillow2"
        snapZone=self.poco.invoke("get_list_snap_zone")
        snapZone = snapZone['snap_zones']
        target_pos=None
        for itemSnap in snapZone:
            if name== itemSnap['item_identifier']:
                pos=itemSnap['position']
                target_pos= (pos['x'], pos['y'])
                print(f"found snapZone for {name}, normalized_pos={target_pos}")
                break
        if not target_pos:
            raise ValueError(f"Cannot find snapZone for {name}")
        target_pos = (target_pos[0], target_pos[1] - 2)
        print(f"adjusted normalized_pos={target_pos}")
        norm_pos= self.poco.invoke("get_normalized_position", x=target_pos[0], y=target_pos[1])
        norm_pos= norm_pos['normalized_pos']
        print(f"final normalized_pos={norm_pos}")
        obj= self.poco(name)
        obj.drag_to(norm_pos, duration=0.5)

    def test_lv4_minigame(self):
        floating_items = self.poco.invoke("get_floating_objs")
        floating_items = floating_items['floating_objs']
        print(f"float_item: {floating_items}")
        thung_rac=self.poco("0_thungrac")
        for itemFloat in floating_items:
            self.poco(itemFloat).drag_to(thung_rac.focus([0.5, 1]), duration=0.2)
