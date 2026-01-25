from airtest.core.api import swipe, sleep
from Hierarchy.PopupCampaignSelectLv import PopupCampaignSelectLv
from Hierarchy.PopupLevelPrepare import PopupLevelPrepare
from Hierarchy.UI_ingame import UI_Ingame, CurrencyBarIngame, RevivalPopup, UITop, PopupGameLose, PopupGameWin, \
    EndGameVideoPopup, PausePopup
from Hierarchy.IAP_pack import *
from logger_config import get_logger
from utils import get_resource_amount
from utils.helper_functions import wait_for_element
from airtest.core.api import *
import os
from utils.get_resource_amount import clean_number, get_single_resource_amount
from utils.test_level_helper import *
from utils.keyboard_helper import press_key
from utils.campaignLv_playing_helper2 import *


def extra_lv_play(poco,target_lv,mode="normal", logger_name="normal_lv_play"):
    logger= get_logger(logger_name)
    popup_campaign= goto_popup_campaign_select_lv(poco, logger)
    popup_campaign= ensure_mode_selected(poco, popup_campaign, logger, mode=mode)

    click_to_lv=navigate_and_click_level(poco, popup_campaign, target_lv, logger)
    if not click_to_lv:
        logger.error(f"[normal_lv_play] ❌ Cannot click level {target_lv}!")
        return

    is_max = is_max_unlocked_level(target_lv, popup_campaign.list_level_normal) #to credit 1st reward if max level

    popup_prepare= PopupLevelPrepare(poco.freeze())
    assert popup_prepare.root.exists(), "PopupLevelPrepare not found after clicking level"
    assert popup_prepare.level_number == target_lv, f"PopupLevelPrepare level number {popup_prepare.level_number} does not match target level {target_lv}"

    reward1=read_1stRewardLv_popup_prepare(is_max,popup_prepare, mode, logger)
    #reward1: dict:
    # gold:int
    # gem:int
    initial_resource={
        "gold": get_single_resource_amount(poco, "gold"),
        "gem": get_single_resource_amount(poco, "gem"),
    }
    logger.info(f"[normal_lv_play] Initial resources before starting level: {initial_resource}")
    popup_prepare.btn_start.click(sleep_interval=2)

    # Wait for ingame UI to appear
    if not wait_for_element(UI_Ingame(poco).root, timeout=10, interval=1):
        logger.error("[normal_lv_play] ❌ UI_Ingame not found after starting level!")
        return
    logger.info("[normal_lv_play] Ingame UI found, level started successfully.")

    #wait for bullet appears, indicating plane start shooting
    def check_bullet_pool(attempt=5):
        for _ in range(attempt):
            bullet_pool = poco("UbhObjectPool")
            if bullet_pool.exists() and len(bullet_pool.children()) > 0:
                return True
            sleep(1)
        logger.error("Bullet pool not found or still empty after maximum attempts")
        return False
    if not check_bullet_pool(5):
        logger.error("[normal_lv_play] ❌ Bullet pool not found or still empty after maximum attempts!")
        return

    #AUTOPLAY level until end
    logger.info("[normal_lv_play] Bullet pool found, AUTOPLAY run.")
    ingame_results= run_level_until_end(poco, initial_resource, logger, mode, target_lv)
    sleep(2)  # Wait for endgame popup to stabilize

    popup_end= verify_endgame_popup(poco,ingame_results, logger)
    handle_interruptions_after_level_end(poco, logger)

    final_gold, final_gem=verify_resource_on_end_popup(
        poco,
        initial_resource,
        ingame_results,
        reward1,
        popup_end.bonus_gold_amount,logger
    )
    final_resource={
        "gold": final_gold,
        "gem": final_gem,}
    navigate_to_home(poco,popup_end, logger)
    home_verify=verify_home_resource_consistent(poco,final_resource,logger)
    logger.info(f"[normal_lv_play] Level {target_lv} {mode.upper()} playthrough completed.")



