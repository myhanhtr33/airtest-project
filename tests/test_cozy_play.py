import pytest
from logger_config import get_logger
from tests.snake.snake_test import *
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
        def data_requery():
            nonlocal ingame_grid_data, layer_data, block_by, block_by2, snake_map, match_boxes
            ingame_grid_data = get_ingame_grid_data(self.poco)
            layer_data = ingame_grid_data['layerData']
            block_by = ingame_grid_data['block_by']
            block_by2 = ingame_grid_data['block_by2']
            snake_map = get_snake_map(self.poco)
            match_boxes = get_match_boxes(self.poco)
        def match_boxes_requery():
            nonlocal match_boxes
            match_boxes = get_match_boxes(self.poco)
        def is_wait_for_anim(snake_id, match_boxes):
            for box in match_boxes:
                if not is_open_box(box):
                    continue
                box_color_val = box_color(box)
                remain_slots= box['runtimeData']['remainSlots']
                snake_color = snake_map[snake_id]['color']
                if box_color_val == snake_color and remain_slots <=1:
                    return True
            return False

        ingame_grid_data = get_ingame_grid_data(self.poco)
        layer_data = ingame_grid_data['layerData']
        block_by = ingame_grid_data['block_by']
        block_by2 = ingame_grid_data['block_by2']
        snake_map = get_snake_map(self.poco)
        match_boxes = get_match_boxes(self.poco)
        while len(layer_data)>0:
            print(f"current snakes: {list(layer_data.keys())}")
            optimal_snake=find_optimal_move(block_by, snake_map, match_boxes,block_by2)
            print(f"optimal snake: {optimal_snake['snake_id']} color: {snake_map[optimal_snake['snake_id']]['color']}"
                  f"({get_color_name(snake_map[optimal_snake['snake_id']]['color'])}). "
                  f"{len(optimal_snake['plan'])} snakes to move")
            available_waiting_bar= get_available_waiting_bar_count(self.poco)
            if len(optimal_snake['plan'])>= available_waiting_bar:
                print(f"not enough waiting bars to move optimal snake, available waiting bars: {available_waiting_bar}, "
                      f"optimal snake plan length: {len(optimal_snake['plan'])}.")
                ##solution 1: open more matche box
                locked_box_count= get_locked_match_box_count(match_boxes)
                if locked_box_count>0:
                    print(f"there are {locked_box_count} locked match boxes, try to open one to get more waiting bars...")
                    for box in match_boxes:
                        if not is_open_box(box):
                            box_pos= pos_of(box, self.poco)
                            click(box_pos)
                            sleep(2)
                            match_boxes_requery()
                            break

            for i, snake in enumerate(optimal_snake['plan']):
                snake_pos = pos_of(snake_map, snake)
                print(f"moving snake {snake} color:{snake_map[snake]['color']}({get_color_name(snake_map[snake]['color'])})")
                click(snake_pos)
                if is_wait_for_anim(snake, match_boxes):
                    print("waiting for box open animation...")
                    sleep(2)
                    match_boxes_requery()
                else:
                    sleep(0.5)
            sleep(2)
            data_requery()



    def test_drag(self):
        # match_boxes = get_match_boxes(self.poco)
        # match_boxes = list(reversed(get_match_boxes(self.poco)))
        # print(f'macth_boxes: {match_boxes}')
        # box2_position= self.poco("btnBooster_4").get_position()
        # box3_position= self.poco("btnBooster_5").get_position()
        # match_boxes[2]['position_normalized']= box2_position
        # match_boxes[3]['position_normalized']= box3_position
        # print(f"after adjustment, match_boxes: {match_boxes}")
        # for box in match_boxes:
        #     if not box['position_normalized'] is None:
        #         click(box['position_normalized'])
        #         sleep(1)
        result= self.poco.invoke("get_waiting_bars")
        result=list(reversed(result['waitingBars']))
        print(f"waiting bars: {result}")
        result1= self.poco.invoke("get_user_data")
        print(f"get_user_data: {result1}")
        self.poco.invoke("add_resource", resourceId="gold",amount=100)
        self.poco.invoke("add_resource", resourceId="magnet",amount=5)
        result1 = self.poco.invoke("get_user_data")
        print(f"AFTER get_user_data: {result1}")
        available_bars=0
        available_bar_indices = []
        for idx,pole in enumerate(result):
            if pole['snakeId'] is None:
                available_bars+=1
                available_bar_indices.append(idx)
        print(f"available bars: {available_bars}, indices: {available_bar_indices}")







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

    def test_lv1(self):
        ## gameplay
        # popup_win= self.poco("PopupWin")
        # btn_next=popup_win.offspring("Next")
        # if not wait_for_element(popup_win,timeout=10):
        #     raise TargetNotFoundError("Cannot find PopupWin")
        # if not wait_for_element(btn_next,timeout=10):
        #     raise TargetNotFoundError("Cannot find Next button in PopupWin")
        # btn_next.click()
        sleep(2)
        level_display= self.poco("T_LevelCurrent")
        if not wait_for_element(level_display,timeout=10):
            raise TargetNotFoundError("Cannot find T_LevelCurrent")
        level_text= level_display.get_text().replace("Lv.","")
        assert level_text=="2", f"Expected level 2, but got level {level_text}"
        print(f"successfully enter next level {level_text}")
    def test_lv2(self,level=2):
        level_display = self.poco("T_LevelCurrent")
        if not wait_for_element(level_display, timeout=10):
            raise TargetNotFoundError("Cannot find T_LevelCurrent")
        level_text = level_display.get_text().replace("Lv.", "")
        assert level_text == f"{level}", f"Expected level {level}, but got level {level_text}"
        # gameplay
        # popup_win= self.poco("PopupWin")
        # btn_next=popup_win.offspring("Next")
        # btn_ads= popup_win.offspring("B_Ads")
        # if not wait_for_element(popup_win,timeout=10):
        #     raise TargetNotFoundError("Cannot find PopupWin")
        # if not wait_for_element(btn_next,timeout=10):
        #     raise TargetNotFoundError("Cannot find Next button in PopupWin")
        # if not wait_for_element(btn_ads,timeout=10):
        #     raise TargetNotFoundError("Cannot find Ads button in PopupWin")
        # btn_next.click()
        # sleep(2)
        # level_display = self.poco("T_LevelCurrent")
        # if not wait_for_element(level_display, timeout=10):
        #     raise TargetNotFoundError("Cannot find T_LevelCurrent")
        # level_text = level_display.get_text().replace("Lv.", "")
        # assert level_text == f"{level+1}", f"Expected level {level+1}, but got level {level_text}"
        # print(f"successfully enter next level {level_text}")