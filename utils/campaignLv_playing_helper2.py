import threading
import time
from airtest.core.api import swipe, sleep
from Hierarchy.PopupCampaignSelectLv import PopupCampaignSelectLv
from Hierarchy.PopupLevelPrepare import PopupLevelPrepare
from Hierarchy.UI_ingame import UI_Ingame, CurrencyBarIngame, RevivalPopup, UITop, PopupGameLose, PopupGameWin, \
    EndGameVideoPopup, PausePopup, PopupRate
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

def multiple_normal_lv_play(poco, lv_list, mode="normal", logger_name="multiple_lv_play"):
    logger= get_logger(logger_name)
    for lv in lv_list:
        logger.info(f"[multiple_lv_play] Starting level {lv} in mode {mode}.")
        normal_lv_play(poco, lv, mode, logger_name=logger_name)
        make_sure_in_home(poco, logger)
        logger.info(f"[multiple_lv_play] Completed level {lv} in mode {mode}.")
def normal_lv_play(poco,target_lv,mode="normal", logger_name="normal_lv_play"):
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
    if mode == "hard" and popup_campaign.hard_lock:
        logger.error(f"[ensure_mode_selected] ❌ Hard mode is locked!")
        raise ValueError(f"Hard mode is locked!")
    if mode == "hell" and popup_campaign.hell_lock:
        logger.error(f"[ensure_mode_selected] ❌ Hell mode is locked!")
        raise ValueError(f"Hell mode is locked!")

    mode_pattern= popup_campaign.mode_pattern
    if mode in mode_pattern.lower():
        logger.info(f"[ensure_mode_selected] Mode {mode} is already selected.")
        return popup_campaign

    target_mode_btn = mode_map[mode]
    if not target_mode_btn.exists():
        logger.error(f"[ensure_mode_selected] ❌ Mode button for {mode} not found!")
        raise RuntimeError(f"Mode button for {mode} not found")
    logger.info(f"[ensure_mode_selected] Selecting mode: {mode}")
    target_mode_btn.click(sleep_interval=1.5)

    popup_campaign= PopupCampaignSelectLv(poco.freeze())
    mode_pattern = popup_campaign.mode_pattern
    if mode not in mode_pattern.lower():
        logger.error(f"[ensure_mode_selected] ❌ Failed to select mode: {mode}, current pattern: {mode_pattern}")
        raise RuntimeError(f"Failed to select mode: {mode}, current pattern: {mode_pattern}")
    logger.info(f"[ensure_mode_selected] Mode {mode} selected successfully.")
    return popup_campaign
def read_1stRewardLv_popup_prepare(is_max,popup_prepare, mode, logger):
    if is_max:
        reward={
            "gold": popup_prepare.gold_reward_amount,
            "gem": popup_prepare.gem_reward_amount,
        }
    else:
        reward={
            "gold": 0,
            "gem": 0,
        }
    logger.info(f"[read_1stRewardLv_popup_prepare] 1st Reward for mode {mode}: {reward}")
    return reward
def run_level_until_end(poco,initial_resource,logger,mode,target_level):
    """"
    run level until win or lose popup appears or timeout reached
    return dict:
        status: "WIN" / "LOSE"
        collected_gold: int
        collected_gem: int
        killed_percent: int
    """
    frozen_ingame_UI= UI_Ingame(poco.freeze())
    max_duration= 60*7  # 7 minutes
    ingame_results= {
        "status": "TIMEOUT",
        "collected_gold": 0,
        "collected_gem": 0,
        "killed_percent": 0
    }
    stats = {
        "stop":False
    }
    collected_gold= 0
    collected_gem= 0
    killed_percent= 0
    start_time= time.time()
    first_move=False
    i=0
    while True:
        now= time.time()
        if now - start_time > max_duration:
            logger.info(f"[run_level_until_end] Level run timed out in {max_duration} seconds. .")
            raise BattleTimeoutError(
                duration=max_duration,
                latched_hp="not implemented yettttt",
                latched_killed_percent=ingame_results["killed_percent"],
                mode=mode,
                level=target_level,
            )
        # 1. handle interruptionspppppppppppppppppppppppppppppp
        revival_popup = RevivalPopup(poco.freeze())
        if revival_popup.root.exists():
            initial_resource = handle_revival_popup(poco, revival_popup, initial_resource, logger)
        popup_pause = PausePopup(poco.freeze())
        if popup_pause.root.exists():
            logger.info("[run_level_until_end] Pause popup detected, clicking resume.")
            popup_pause.btn_resume.click(sleep_interval=1)
            press_key(poco, "UP")
        #2. Check end signals
        if PopupGameLose(poco).root.exists():
            logger.info("[run_level_until_end] Level ended with LOSE.")
            ingame_results["status"]="LOSE"
            print(f"Final ingame_results: {ingame_results}")
            return ingame_results
        if PopupGameWin(poco).root.exists():
            logger.info("[run_level_until_end] Level ended with WIN.")
            ingame_results["status"]="WIN"
            print(f"Final ingame_results: {ingame_results}")
            return ingame_results
        #3. autoplay actions and stats polling in threads
        def autoplay_thread():
            nonlocal first_move
            do_autoplay_action(poco, first_move, frozen_ingame_UI)
            first_move = True  # Set to True after first execution
        def stats_polling_thread():
            def stats_poller():
                UI_tmp = UITop(poco.freeze())
                tmp = UI_tmp.collected_gold
                ingame_results["collected_gold"] = max(ingame_results["collected_gold"], tmp) if tmp else \
                ingame_results["collected_gold"]
                tmp_gem = UI_tmp.collected_gem
                ingame_results["collected_gem"] = max(ingame_results["collected_gem"], tmp_gem) if tmp_gem else \
                ingame_results["collected_gem"]
                tmp_enemy = UI_tmp.killed_enemies_percentage
                ingame_results["killed_percent"] = max(ingame_results["killed_percent"], tmp_enemy) if tmp_enemy else ingame_results["killed_percent"]
                logger.info(f"[stats_poller] Collected gold: {ingame_results['collected_gold']}, gem: {ingame_results['collected_gem']}, killed percent: {ingame_results['killed_percent']}")
            stats_poller()
            sleep(0.5)
        autoplay_thread_obj=threading.Thread(target=autoplay_thread)
        stats_thread_obj=threading.Thread(target=stats_polling_thread)
        stats_thread_obj.start()
        autoplay_thread_obj.start()
        sleep(2.5)  # Let them run for a short duration
        autoplay_thread_obj.join()
        stats_thread_obj.join()
def handle_revival_popup(poco, revival_popup, initial_resource, logger):
    logger.info("[handle_revival_popup] Revival popup detected.")
    gem_amount=revival_popup.gem_amount
    if initial_resource["gem"]<gem_amount:
        logger.info(f"[handle_revival_popup] Not enough gems ({initial_resource['gem']}) to revive (cost: {gem_amount}), invoking add_gem.")
        poco.invoke("add_gem", amount=50)
        initial_resource["gem"]+=50
        sleep(1)
    logger.info("[handle_revival_popup] Clicked revive with gems.")
    revival_popup.btn_gem.click(sleep_interval=1)
    revival_popup= RevivalPopup(poco)
    if not wait_for_element(revival_popup.root, timeout=5, interval=1, condition="disappear"):
        logger.error("[handle_revival_popup] ❌ RevivalPopup still exists after attempting to revive with gems!")
        raise RuntimeError("RevivalPopup still exists after attempting to revive with gems")
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
        for i in range(33):
            press_key(poco, "P")
        swipe(initial_plane_pos, start_pos)  # Move to starting position
        press_key(poco, "UP")
        first_move = True
    press_key(poco, "T")
    swipe(start_pos, end_pos, duration=1)
    swipe(end_pos, start_pos, duration=1)
def verify_endgame_popup(poco,ingame_results, logger):
    status= ingame_results.get("status")
    if status == "WIN":
        popup_end= PopupGameWin(poco.freeze())
        if not wait_for_element(popup_end.root, timeout=10, interval=1):
            logger.error("[verify_endgame_popup] ❌ PopupGameWin not found after level win!")
            raise RuntimeError("PopupGameWin not found after level win")
        logger.info("[verify_endgame_popup] PopupGameWin found successfully.")
        return popup_end
    elif status == "LOSE":
        popup_end= PopupGameLose(poco.freeze())
        if not wait_for_element(popup_end.root, timeout=10, interval=1):
            logger.error("[verify_endgame_popup] ❌ PopupGameLose not found after level lose!")
            raise RuntimeError("PopupGameLose not found after level lose")
        logger.info("[verify_endgame_popup] PopupGameLose found successfully.")
        return popup_end
    else:
        logger.error(f"[verify_endgame_popup] ❌ Invalid ingame_results status: {status}")
        raise ValueError(f"Invalid ingame_results status: {status}")
def handle_interruptions_after_level_end(poco, logger):
    max_attempts = 1
    for attempt in range(max_attempts):
        popup_video_endgame = EndGameVideoPopup(poco)
        popup_rate= PopupRate(poco)
        popup_royalty_pack = RoyalPack(poco)
        popup_starter_pack = Popup_StarterPack(poco)
        popup_vip_pack = Popup_VipPack(poco)
        popup_premium_pack = Popup_PremiumPack(poco)
        if popup_rate.root:
            logger.info("Rate popup found, closing...")
            popup_rate.btn_back.click(sleep_interval=1)
            break
        if popup_video_endgame.root:
            logger.info("EndGameVideoPopup found, handling...")
            popup_video_endgame.tap_close_text.click(sleep_interval=1)
            break
        if popup_royalty_pack.root:
            logger.info("RoyalPack popup found, closing...")
            popup_royalty_pack.btnBack.click(sleep_interval=1)
            break
        if popup_starter_pack.root:
            logger.info("StarterPack popup found, closing...")
            popup_starter_pack.btn_back.click(sleep_interval=1)
            break
        if popup_vip_pack.root:
            logger.info("VipPack popup found, closing...")
            popup_vip_pack.btn_back.click(sleep_interval=1)
            break
        if popup_premium_pack.root:
            logger.info("PremiumPack popup found, closing...")
            popup_premium_pack.btn_back.click(sleep_interval=1)
            break
        attempt += 1
        sleep(1)
def verify_resource_on_end_popup(
        poco,
        initial_resource,
        ingame_results,
        reward1,
        bonus_gold_amount,
        logger
    ):
    currency_bar_ingame = CurrencyBarIngame(poco)
    final_gold = currency_bar_ingame.gold_amount
    final_gem = currency_bar_ingame.gem_amount

    logger.info(f"Initial resource: {initial_resource}")
    logger.info(f"Ingame results: {ingame_results['status']}, collected_gold: {ingame_results['collected_gold']}, collected_gem: {ingame_results['collected_gem']}, killed_percent: {ingame_results['killed_percent']}")
    logger.info(f"1st reward: {reward1}, bonus_gold_amount: {bonus_gold_amount}")

    if ingame_results["status"] == "WIN":
        expected_gold = initial_resource["gold"] + ingame_results["collected_gold"] + reward1["gold"] + bonus_gold_amount
        expected_gem = initial_resource["gem"] + ingame_results["collected_gem"] + reward1["gem"]
    else:
        expected_gold = initial_resource["gold"] + ingame_results["collected_gold"] + bonus_gold_amount
        expected_gem = initial_resource["gem"] + ingame_results["collected_gem"]

    gold_verify= get_resource_amount.verify_resource_amount_change("gold", final_gold, expected_gold)
    gem_verify= get_resource_amount.verify_resource_amount_change("gem", final_gem, expected_gem)

    # Log verification results
    logger.info(f"Game result: {ingame_results['status']}")
    logger.info(f"Collected during gameplay - Gold: {expected_gold}, Gem: {expected_gem}")

    if gold_verify and gem_verify:
        logger.info("✓ Resource verification successful!")
        logger.info(f"Gold verification: {gold_verify} (Expected: {expected_gold}, Actual: {final_gold})")
        logger.info(f"Gem verification: {gem_verify} (Expected: {expected_gem}, Actual: {final_gem})")
    else:
        if not gold_verify:
            logger.error(
                f"✗ Gold verification failed! Expected: {expected_gold}, Actual: {final_gold}, Difference: {abs(expected_gold - final_gold)}")
        if not gem_verify:
            logger.error(
                f"✗ Gem verification failed! Expected: {expected_gem}, Actual: {final_gem}, Difference: {abs(expected_gem - final_gem)}")
    return final_gold , final_gem
def navigate_to_home(poco,popup_end, logger):
    btn_next= popup_end.btn_next
    if wait_for_element(popup_end.btn_next, timeout=8):
        popup_end.btn_next.click(sleep_interval=2)
        logger.info("[navigate_to_home] Clicked btn_next to navigate to home.")
    elif wait_for_element(popup_end.btn_back, timeout=8):
        popup_end.btn_back.click(sleep_interval=2)
        logger.info("[navigate_to_home] Clicked btn_back to navigate to home.")
    else:
        press_key(poco, "BACK")
        sleep(2)
        logger.info("[navigate_to_home] Pressed BACK key to navigate to home.")
def verify_home_resource_consistent(poco,final_resource,logger):
    btnCampaign_node= poco("BtnCampaign")
    if not wait_for_element(btnCampaign_node, timeout=10, interval=1):
        logger.error("[verify_home_resource_consistent] ❌ Home screen not found after level completion!")
        raise RuntimeError("Home screen not found after level completion")

    # Verify we're actually at home screen by checking for campaign button
    current_dir = os.path.dirname(os.path.abspath(__file__))
    btnCampaign_img = Template(os.path.join(os.path.dirname(current_dir), "image", "btnCampaign.png"))

    # Check if we're at home screen, if not try to navigate there
    max_home_attempts = 5
    for home_attempt in range(max_home_attempts):
        if exists(btnCampaign_img):
            logger.info("Successfully at home screen for final verification")
            break
        else:
            logger.warning(f"Not at home screen yet, attempt {home_attempt + 1}")
            # Try to get to home by using back navigation
            press_key(poco, "BACK")
            sleep(2)
            if home_attempt == max_home_attempts - 1:
                logger.error("Could not navigate to home screen for final verification")
                return False
    sleep(3)  # Wait for home screen to stabilize
    home_resource={
        "gold": get_single_resource_amount(poco, "gold"),
        "gem": get_single_resource_amount(poco, "gem"),
    }
    logger.info(f"[verify_home_resource_consistent] Home resources: {home_resource}, Expected final resources: {final_resource}")
     # Verify final resources on home screen
    assert home_resource["gold"] == final_resource["gold"], f"Final gold on home ({home_resource['gold']}) does not match expected ({final_resource['gold']})"
    assert home_resource["gem"] == final_resource["gem"], f"Final gem on home ({home_resource['gem']}) does not match expected ({final_resource['gem']})"
    return True
def make_sure_in_home(poco, logger):
    btnCampaign_node = poco("BtnCampaign")
    if not wait_for_element(btnCampaign_node, timeout=10, interval=1):
        logger.error("[verify_home_resource_consistent] ❌ Home screen not found after level completion!")
        raise RuntimeError("Home screen not found after level completion")

    # Verify we're actually at home screen by checking for campaign button
    current_dir = os.path.dirname(os.path.abspath(__file__))
    btnCampaign_img = Template(os.path.join(os.path.dirname(current_dir), "image", "btnCampaign.png"))

    # Check if we're at home screen, if not try to navigate there
    max_home_attempts = 5
    for home_attempt in range(max_home_attempts):
        if exists(btnCampaign_img):
            logger.info("Successfully at home screen for final verification")
            break
        else:
            logger.warning(f"Not at home screen yet, attempt {home_attempt + 1}")
            # Try to get to home by using back navigation
            press_key(poco, "BACK")
            sleep(2)
            if home_attempt == max_home_attempts - 1:
                logger.error("Could not navigate to home screen for final verification")











