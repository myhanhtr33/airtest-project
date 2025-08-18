from poco.utils.simplerpc.simplerpc import RpcTimeoutError

from Hierarchy.PopupCampaignSelectLv import PopupCampaignSelectLv, PanelWorlds
from Hierarchy.PopupLevelPrepare import PopupLevelPrepare
from Hierarchy.UI_ingame import *
import pytest
import os
from logger_config import get_logger
from utils.helper_functions import wait_for_element
from utils.test_level_helper import *
from airtest.core.api import swipe, sleep

current_dir=os.path.dirname(os.path.abspath(__file__))
img_path= os.path.join(os.path.dirname(current_dir),"image","Plane1_bata.png")
bata_img = Template(img_path)

class TestIngameeee:
    def setup(self):
        pass
    def test1111(self, poco):
        logger = get_logger()
        ui_ingame = UI_Ingame(poco)
        if wait_for_element(ui_ingame.root, timeout=5):
            bata_pos = wait(bata_img, timeout=6)
            btn_skill_pos = ui_ingame.btn_plane_skill.get_position() if ui_ingame.btn_plane_skill.exists() else None
            tmp = UITop(poco).collected_gold_text
            gold= 0
            if bata_pos and btn_skill_pos:
                start_pos = ((bata_pos[0] - btn_skill_pos[0]) / 2 + btn_skill_pos[0], bata_pos[1])
                end_pos = (bata_pos[0] + (bata_pos[0] - start_pos[0]), bata_pos[1])

                ingameUI = UI_Ingame(poco)
                btn = ingameUI.btn_plane_skill if ingameUI.btn_plane_skill.exists() else None
                first_move = False

                while btn:
                    if not first_move:
                        for i in range(30):
                            keyevent("P")
                        swipe(bata_pos, start_pos)  # move to start position
                        first_move = True
                    # keyevent("U")
                    tmp = UITop(poco).collected_gold_text
                    gold= tmp if tmp is not None and tmp >gold else gold
                    print(f"gold_text1: {gold}")
                    swipe(start_pos, end_pos, duration=2)
                    tmp = UITop(poco).collected_gold_text
                    gold= tmp if tmp is not None and tmp >gold else gold
                    print(f"gold_text2: {gold}")
                    swipe(end_pos, start_pos, duration=2)
                    tmp = UITop(poco).collected_gold_text
                    gold= tmp if tmp is not None and tmp >gold else gold
                    print(f"gold_text3: {gold}")
                    sleep(2)
                    tmp = UITop(poco).collected_gold_text
                    gold= tmp if tmp is not None and tmp >gold else gold
                    print(f"gold_text4: {gold}")
                    btn = ingameUI.btn_plane_skill if ingameUI.btn_plane_skill.exists() else None
            print(f"collected_gold_text: {gold}")
