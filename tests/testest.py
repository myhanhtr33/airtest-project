from Hierarchy.PopupCampaignSelectLv import PopupCampaignSelectLv
from Hierarchy.Tutorial_UI import *
from Hierarchy.UI_ingame import *
from Hierarchy.HOME_Element import *
import os
from logger_config import get_logger
from utils.helper_functions import wait_for_element
from utils.test_level_helper import *
from utils.get_resource_amount import *
from airtest.core.api import swipe, sleep, wait, keyevent, Template
from airtest.core.error import TargetNotFoundError

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
    def setup(self):
        pass
    def test1111(self, poco):
        logger = get_logger()
        ui_ingame = UI_Ingame(poco)
        btn_active_skill_tut=poco("fadeCooldownActiveSkills")
        tutLv1_P1_1 = None
        tutLv1_P1_2 = None
        is_complete_tutLv1_P1 = None
        is_complete_tutLv1_P2 = None
        if wait_for_element(ui_ingame.root, timeout=5):
            bata_pos = wait(bata_img, timeout=6, intervalfunc=notfound())
            btn_skill_pos = ui_ingame.btn_plane_skill.get_position() if ui_ingame.btn_plane_skill.exists() else None
            tmp = UITop(poco).collected_gold
            gold= 0
            if bata_pos and btn_skill_pos:
                start_pos = ((bata_pos[0] - btn_skill_pos[0]) / 2 + btn_skill_pos[0], bata_pos[1])
                end_pos = (bata_pos[0] + (bata_pos[0] - start_pos[0]), bata_pos[1])

                ingameUI = UI_Ingame(poco)
                btn_node = ingameUI.btn_plane_skill
                btn = btn_node if btn_node.exists() else None
                btn_gem_revival_popup_node= RevivalPopup(poco).btn_gem
                btn_gem_revival_popup= btn_gem_revival_popup_node if btn_gem_revival_popup_node.exists() else None

                first_move = False
                while btn:
                    if btn_gem_revival_popup:
                        if get_single_resource_amount(poco, "gem")<50:
                            self.poco.invoke("add_gem", amount=50)
                            # logger.info("Not enough gems for revival, invoking add_gem")
                        sleep(1)
                        # logger.info("Revival popup detected, clicking revive button")
                        btn_gem_revival_popup.click(sleep_interval=1)
                        sleep(2)
                        continue
                    if not first_move:
                        for i in range(30):
                            keyevent("P")
                        swipe(bata_pos, start_pos)  # move to start position
                        first_move = True
                    if not tutLv1_P1_1:
                        try:
                            tutLv1_P1_1 = wait(hand_tut_img, timeout=6, intervalfunc=notfound())
                            tutLv1_P1_2 = wait(ingame_noti_img, timeout=6, intervalfunc=notfound())
                            btn_active_skill_tut.click(sleep_interval=1)
                            is_complete_tutLv1_P1 = tutLv1_P1_1 is not None and tutLv1_P1_2 is not None
                            print(
                                f"::::::::::::::::tutLv1_1_1: {tutLv1_P1_1}, tutLv1_1_2: {tutLv1_P1_2}, is_complete_tutLv1_P1: {is_complete_tutLv1_P1}")
                        except TargetNotFoundError:
                            # logger.warning("Hand tutorial image or ingame notification frame not found, continuing...")
                            is_complete_tutLv1_P1 = None
                    keyevent("C")
                    swipe(start_pos, end_pos, duration=2)
                    tmp = UITop(poco).collected_gold
                    gold= max(gold,tmp) if tmp is not None else gold
                    print(f"gold_text2: {gold}")
                    swipe(end_pos, start_pos, duration=2)
                    tmp = UITop(poco).collected_gold
                    gold= max(gold,tmp) if tmp is not None else gold
                    print(f"gold_text3: {gold}")
                    keyevent("C")
                    sleep(1)
                    tmp = UITop(poco).collected_gold
                    gold= max(gold,tmp) if tmp is not None else gold
                    print(f"gold_text4: {gold}")
                    btn = ingameUI.btn_plane_skill if ingameUI.btn_plane_skill.exists() else None
            print(f"collected_gold_text: {gold}")
            max_attempts = 5
            for attempt in range(max_attempts):
                popup_lose = PopupGameLose(poco)
                popup_win = PopupGameWin(poco)
                if popup_lose.root.exists():
                    # logger.info("Game lost, retrying...")
                    # popup_lose.btn_retry.click(sleep_interval=3)
                    # # Retry logic can be added here if needed
                    break
                elif popup_win.root.exists():
                    # logger.info("Game won!")
                    sleep(2)
                    try:
                        tutLv1_P2 = wait(hand_tut_img, timeout=15, intervalfunc=notfound())
                        if tutLv1_P2:
                            btn_back = popup_win.btn_back
                            if btn_back:
                                btn_back.click(sleep_interval=1)
                                is_complete_tutLv1_P2 = True
                                print("Back button clicked after win popup")
                            # else:
                            #     logger.warning("Back button not found after win popup")
                        # else:
                        #     logger.warning("Hand tutorial image not found after win popup")
                    except TargetNotFoundError:
                        # logger.warning("Hand tutorial image not found after win popup")
                        is_complete_tutLv1_P2 = None
                    break
                attempt += 1
                sleep(2)
                # Raise error if we run out of attempts and neither win nor lose popup appears
                if attempt >= max_attempts - 1:
                    raise AssertionError("Game didn't reach a conclusion (win or lose) after maximum attempts")
        is_complete_tutLv1= is_complete_tutLv1_P1 and is_complete_tutLv1_P2
        print(f"complete whole tutorial: {is_complete_tutLv1}")

    def test2222(self, poco):
        popup= PopupCampaignSelectLv(poco)
        normal_levels=popup.list_level_normal
        # for level in normal_levels:
        #     lv= level.index
        #     list_star= level.list_star
        #     star1_sprite= level.star1_sprite
        #     star2_sprite= level.star2_sprite
        #     star3_sprite= level.star3_sprite
        #     # Only attempt to index when list_star exists and the sprite is a non-empty string
        #     if list_star:
        #         s1 = star1_sprite[-1] if isinstance(star1_sprite, str) and star1_sprite else None
        #         s2 = star2_sprite[-1] if isinstance(star2_sprite, str) and star2_sprite else None
        #         s3 = star3_sprite[-1] if isinstance(star3_sprite, str) and star3_sprite else None
        #         print(f"lv:{lv}  {(s1, s2, s3)}")
        #     else:
        #         print(f"lv:{lv}  NOne")

        # level=7
        # is_max=is_max_unlocked_level(level, normal_levels)
        # print(f"Is {level} max level: {is_max}")

        amount, name = get_single_card_amount_by_sprite(poco, "card_A0")
        print(f"::::::::::: amount: {amount}, name: {name}")

    def test_tut(self, poco):
        from airtest.core.api import find_all
        logger=get_logger("TestTUT")
        campaign_select_lv = PopupCampaignSelectLv(poco)
        normal_levels = campaign_select_lv.list_level_normal

        # Get screen dimensions for coordinate conversion using Poco
        screen_width, screen_height = poco.get_screen_size()

        for lv in normal_levels:
            # has_mini_chest = has_valid_mini_chest(lv, poco, logger=logger)
            # if has_mini_chest:
            #     print(f"Level {lv.index}({lv.root.get_position()}) has a valid mini chest{has_mini_chest}.")
            # else:
            #     print(f"Level {lv.index} does not have a valid mini chest.")
            if lv.index==4:
                # Compute chest normalized position inline (no helper)
                level_pos_normalized = lv.root.get_position() if lv.root.exists() else None
                mini_chest_position = None
                if level_pos_normalized and lv.mini_chest_image_template:
                    tol_norm = 50.0 / float(screen_height)
                    chest_results = None
                    for _ in range(5):
                        chest_results = find_all(lv.mini_chest_image_template)
                        if chest_results:
                            break
                        sleep(0.5)
                    if chest_results:
                        for chest_result in chest_results:
                            chest_px = chest_result['result']
                            chest_norm = (float(chest_px[0]) / float(screen_width), float(chest_px[1]) / float(screen_height))
                            if chest_norm[0] > level_pos_normalized[0] and abs(chest_norm[1] - level_pos_normalized[1]) < tol_norm:
                                mini_chest_position = chest_norm
                                break
                if mini_chest_position:
                    print(f"Level {lv.index}({lv.root.get_position()}) has a valid mini chest {mini_chest_position}.")
                    claim_mini_chest_and_validate_rewards(lv, mini_chest_position, poco, logger)
