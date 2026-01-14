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
from errors.battle_errors import *

def normal_lv_play(poco,target_lv,mode="normal", logger_name="normal_lv_play"):
    logger= get_logger(logger_name)
    popup_campaign= goto_popup_campaign_select_lv(poco, logger)
    popup_campaign= ensure_mode_selected(poco, popup_campaign, logger, mode=mode)
    # Check if target level is unlocked
    if not is_level_unlocked(target_lv, popup_campaign.list_level_normal,logger):
        return {"status": "SKIP_LOCKED"}
    is_max = is_max_unlocked_level(target_lv, popup_campaign.list_level_normal) #to credit 1st reward if max level
    click_to_lv=navigate_and_click_level(poco, popup_campaign, logger)
    if not click_to_lv:
        return {"status": "FAIL_CANNOT_CLICK_LEVEL"}

    popup_prepare= PopupLevelPrepare(poco.freeze())
    assert popup_prepare.root.exists(), "PopupLevelPrepare not found after clicking level"
    assert popup_prepare.level_number == target_lv, f"PopupLevelPrepare level number {popup_prepare.level_number} does not match target level {target_lv}"

    reward1=read_1stRewardLv_popup_prepare(popup_prepare, mode, logger)
    initial_resource={
        "gold": get_single_resource_amount(poco, "gold"),
        "gem": get_single_resource_amount(poco, "gem"),
    }
    logger.info(f"[normal_lv_play] Initial resources before starting level: {initial_reward}")
    popup_prepare.btn_start.click(sleep_interval=2)

    # Wait for ingame UI to appear
    if not wait_for_element(UI_Ingame(poco).root, timeout=10, interval=1):
        logger.error("[normal_lv_play] ❌ UI_Ingame not found after starting level!")
        return {"status": "FAIL_INGAME_NOT_FOUND"}
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
        return {"status": "FAIL_BULLET_NOT_FOUND"}
    sleep(2)  # Let the game run for a but to get stable object positions



def goto_popup_campaign_select_lv(poco, logger):
    sleep(3)  # Wait for home screen to stabilize
    campaign_btn = poco("BtnCampaign")
    if not campaign_btn.exists():
        logger.error("[to_campaign_select_lv] ❌ Campaign button not found!")
        raise RuntimeError("Campaign button not found")
    campaign_btn.click(sleep_interval=1)
    # Check if PopupSelectLevelHome exists
    popup_campaign = PopupCampaignSelectLv(poco)
    if not wait_for_element(popup_campaign.root, timeout=5, interval=0.5):
        logger.error("[to_campaign_select_lv] ❌ PopupSelectLevelHome not found after clicking Campaign!")
        raise RuntimeError("PopupSelectLevelHome(Clone) not found after clicking Campaign button")
    popup_campaign= PopupCampaignSelectLv(poco.freeze())
    return popup_campaign

def ensure_mode_selected(poco,popup_campaign, logger,mode="normal"):
    mode_map = {
        "normal": popup_campaign.mode_normal,
        "hard": popup_campaign.mode_hard,
        "hell": popup_campaign.mode_hell
    }
    if mode not in mode_map:
        logger.error(f"[ensure_mode_selected] ❌ Invalid mode: {mode}")
        raise ValueError(f"Invalid mode: {mode}")

    mode_pattern= popup_campaign.mode_pattern
    if mode in mode_pattern.lowercase():
        logger.info(f"[ensure_mode_selected] Mode {mode} is already selected.")
        return popup_campaign

    target_mode_btn = mode_map[mode]
    if not target_mode_btn.exists():
        logger.error(f"[ensure_mode_selected] ❌ Mode button for {mode} not found!")
        raise RuntimeError(f"Mode button for {mode} not found")
    logger.info(f"[ensure_mode_selected] Selecting mode: {mode}")
    target_mode_btn.click(sleep_interval=1.5)

    popup_campaign= PopupCampaignSelectLv(poco.freeze())
    if mode not in mode_pattern.lowercase():
        logger.error(f"[ensure_mode_selected] ❌ Failed to select mode: {mode}, current pattern: {mode_pattern}")
        raise RuntimeError(f"Failed to select mode: {mode}, current pattern: {mode_pattern}")
    logger.info(f"[ensure_mode_selected] Mode {mode} selected successfully.")
    return popup_campaign

def read_1stRewardLv_popup_prepare(popup_prepare, mode, logger):
    reward={
        "gold": popup_prepare.gold_reward_amount,
        "gem": popup_prepare.gem_reward_amount,
    }
    logger.info(f"[read_1stRewardLv_popup_prepare] 1st Reward for mode {mode}: {reward}")
    return reward

def run_level_until_end(poco,initial_resource,logger):
    """"
    run level until win or lose popup appears or timeout reached
    return dict:
        status: "WIN" / "LOSE"
        collected_gold: int
        collected_gem: int
        killed_percent: int
    """
    frozen_ingame_UI= UI_Ingame(poco.freeze())
    max_duration= 60*70  # 7 minutes
    collected_gold= 0
    collected_gem= 0
    killed_percent= 0
    start_time= time.time()
    first_move=False

    while True:
        #1. check end signals
        if PopupGameLose(poco).root.exists():
            logger.info("[run_level_until_end] Level ended with LOSE.")
            return {
                "status": "LOSE",
                "collected_gold": collected_gold,
                "collected_gem": collected_gem,
                "killed_percent": killed_percent
            }
        if PopupGameWin(poco).root.exists():
            logger.info("[run_level_until_end] Level ended with WIN.")
            return {
                "status": "WIN",
                "collected_gold": collected_gold,
                "collected_gem": collected_gem,
                "killed_percent": killed_percent
            }
        #2. handle interruptions
        revival_popup= RevivalPopup(poco.freeze())
        if revival_popup.root.exists():
            initial_resource=handle_revival_popup(poco, revival_popup, initial_resource, logger)
        popup_pause= PausePopup(poco.freeze())
        if popup_pause.root.exists():
            logger.info("[run_level_until_end] Pause popup detected, clicking resume.")
            popup_pause.btn_resume.click(sleep_interval=2)
            press_key(poco, "UP")
        do_autoplay_action(poco,first_move,frozen_ingame_UI)

def handle_revival_popup(poco, revival_popup, initial_resource, logger):
    logger.info("[handle_revival_popup] Revival popup detected.")
    gem_amount=revival_popup.gem_amount
    if initial_resource["gem"]<gem_amount:
        logger.info(f"[handle_revival_popup] Not enough gems ({initial_resource['gem']}) to revive (cost: {gem_amount}), invoking add_gem.")
        poco.invoke("add_gem", amount=50)
        initial_resource["gem"]+=50
        sleep(1)
    revival_popup.btn_gem.click(sleep_interval=2)
    logger.info("[handle_revival_popup] Clicked revive with gems.")
    initial_resource["gem"]-=gem_amount
    logger.info(f"[handle_revival_popup] Gems after revival: {initial_resource['gem']}")
    press_key(poco,"UP")
    return initial_resource

def do_autoplay_action(poco,first_move, frozen_ingame_UI):
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
        press_key(poco, "UP")
        first_move = True
    press_key(poco, "T")
    swipe(start_pos, end_pos, duration=1)
    sleep(1)
    swipe(end_pos, start_pos, duration=1)

