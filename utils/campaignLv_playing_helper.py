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


def from_home_to_campaign_select(poco, logger_name):
    logger= get_logger(logger_name)
    sleep(3)  # Wait for home screen to stabilize
    campaign_btn = poco("BtnCampaign")
    if not campaign_btn.exists():
        logger.error("[to_campaign_select_lv] ❌ Campaign button not found!")
        raise RuntimeError("Campaign button not found")
    campaign_btn.click()
    time.sleep(1)  # Wait for the popup to appear
    # Check if PopupSelectLevelHome exists
    popup = poco("PopupSelectLevelHome(Clone)")
    if not popup.exists():
        logger.error("[to_campaign_select_lv] ❌ PopupSelectLevelHome not found after clicking Campaign!")
        raise RuntimeError("PopupSelectLevelHome(Clone) not found after clicking Campaign button")

def play_and_verify_level(poco, target_level, logger_name):
    """
    Comprehensive level testing function that navigates to a specific level,
    plays the game, and verifies resource collection accuracy.

    This function handles the complete workflow of:
    1. Level navigation and preparation
    2. Game initialization and resource tracking
    3. Automated gameplay with resource collection
    4. Game completion handling (win/lose scenarios)
    5. Final resource verification on home screen

    Args:
        poco: Poco instance for UI interaction
        target_level (int): The level number to play (e.g., 1, 2, 3, etc.)
        logger_name (str): Logger identifier for tracking this test session
                         Default: "Level1_tut"

    Returns:
        None: Function performs assertions and logs results

    Raises:
        AssertionError: If critical UI elements are not found or game doesn't conclude

    Example:
        # Test level 5 with custom logging
        self.play_and_verify_level(poco, 5, "Level5_custom")

    Test Flow:
        Navigation → Level Preparation → Game Initialization →
        Gameplay Loop → Game Completion → Resource Verification
    """
    # PHASE 1: INITIALIZATION AND SETUP
    logger = get_logger(logger_name)
    logger.info(f"=== STARTING LEVEL {target_level} TEST ===")

    popup_campaign = PopupCampaignSelectLv(poco.freeze())
    assert popup_campaign.root.exists(), "PopupCampaignSelectLv not found"

    # PHASE 2: LEVEL NAVIGATION AND PREPARATION
    logger.info(f"Phase 2: Navigating to Level {target_level}")
    is_target_level_unlocked = is_level_unlocked(target_level, popup_campaign.list_level_normal, logger)
    if not is_target_level_unlocked:
        logger.error(f"Level {target_level} is not unlocked!")
        return

    # Navigate to the target level
    click_to_level = navigate_and_click_level(poco, popup_campaign, target_level, logger)
    if not click_to_level:
        logger.error(f"Failed to navigate to Level {target_level}")
        return

    # Check if this is the maximum unlocked level (affects rewards)
    is_max_level = is_max_unlocked_level(target_level, popup_campaign.list_level_normal)
    gold_1st_reward = 0
    gem_1st_reward = 0

    # Verify level preparation screen is displayed
    popup_prepare = PopupLevelPrepare(poco.freeze())
    assert popup_prepare.root.exists(), f"PopupLevelPrepare not found after clicking level {target_level}"

    # Capture first-time completion rewards if this is max unlocked level
    if is_max_level:
        gold_1st_reward = popup_prepare.gold_reward_amount
        gem_1st_reward = popup_prepare.gem_reward_amount
        logger.info(
            f"Level {target_level} is max level. Gold 1st reward: {gold_1st_reward}, Gem 1st reward: {gem_1st_reward}")

    # ===============================================
    # PHASE 3: GAME INITIALIZATION AND RESOURCE TRACKING
    # ===============================================
    logger.info("Phase 3: Initializing game and resource tracking")

    # Capture initial resource amounts before starting
    initial_resources = get_resource_amount.get_all_resource_amounts(poco)
    logger.info(f"Initial resources: {initial_resources}")

    # Start the level
    popup_prepare.btn_start.click(sleep_interval=3)
    ui_ingame = UI_Ingame(poco)

    # Initialize resource collection counters
    collected_gold = 0
    collected_gem = 0
    bonus_gold=0

    def verify_game_resources(game_result):
        """
        Internal helper function to verify resource amounts after game completion.

        This function compares the expected resource amounts (initial + collected)
        with the actual amounts shown in the game's currency bar.

        Args:
            game_result (str): "WIN" or "LOSE" - the outcome of the game
        """
        currency_bar_ingame = CurrencyBarIngame(poco)
        final_gold = currency_bar_ingame.gold_amount
        final_gem = currency_bar_ingame.gem_amount

        # Calculate expected amounts based on initial + collected during gameplay
        expected_gold = initial_resources["gold"] + collected_gold + bonus_gold
        expected_gem = initial_resources["gem"] + collected_gem

        # Verify the amounts match expectations
        gold_verified = get_resource_amount.verify_resource_amount_change("gold", final_gold, expected_gold)
        gem_verified = get_resource_amount.verify_resource_amount_change("gem", final_gem, expected_gem)

        # Log verification results
        logger.info(f"Game result: {game_result}")
        logger.info(f"Collected during gameplay - Gold: {collected_gold}, Gem: {collected_gem}")

        if gold_verified and gem_verified:
            logger.info("✓ Resource verification successful!")
            logger.info(f"Gold verification: {gold_verified} (Expected: {expected_gold}, Actual: {final_gold})")
            logger.info(f"Gem verification: {gem_verified} (Expected: {expected_gem}, Actual: {final_gem})")
        else:
            if not gold_verified:
                logger.error(
                    f"✗ Gold verification failed! Expected: {expected_gold}, Actual: {final_gold}, Difference: {abs(expected_gold - final_gold)}")
            if not gem_verified:
                logger.error(
                    f"✗ Gem verification failed! Expected: {expected_gem}, Actual: {final_gem}, Difference: {abs(expected_gem - final_gem)}")

    # ===============================================
    # PHASE 4: AUTOMATED GAMEPLAY LOOP
    # ===============================================
    logger.info("Phase 4: Starting automated gameplay")

    if wait_for_element(ui_ingame.root, timeout=5):
        def check_bullet_pool(attempt=5):
            for _ in range(attempt):
                bullet_pool = poco("UbhObjectPool")
                if bullet_pool.exists() and len(bullet_pool.children()) > 0:
                    return True
                sleep(1)
            logger.error("Bullet pool not found or still empty after maximum attempts")
            return False

        if check_bullet_pool(5):
            #sleep to ensure game stability then calculate the positions
            sleep(2)
            initial_plane_pos = (227, 819)  # Player character position
            btn_skill = ui_ingame.btn_plane_skill
            btn_skill_pos = ui_ingame.btn_plane_skill.get_position() if ui_ingame.btn_plane_skill.exists() else None
            print(f"Found bata at position: {initial_plane_pos}, skill button position: {btn_skill_pos}")

            start_pos = ((initial_plane_pos[0] - btn_skill_pos[0]) / 2 + btn_skill_pos[0], initial_plane_pos[1])
            end_pos = (initial_plane_pos[0] + (initial_plane_pos[0] - start_pos[0]), initial_plane_pos[1])
            btn_node = ui_ingame.btn_plane_skill
            btn = btn_node if btn_node.exists() else None
            first_move = False

            # Main gameplay loop - continues until skill button disappears (game ends)
            while btn:
                revival_popup= RevivalPopup(poco.freeze())
                btn_gem_revival_node = revival_popup.btn_gem
                btn_gem_revival = btn_gem_revival_node if btn_gem_revival_node.exists() else None
                print(f"btn_gem_revival_popup: {btn_gem_revival_node}")
                btn_continue_popup_pause_node = PausePopup(poco.freeze()).btn_resume
                btn_continue_popup_pause = btn_continue_popup_pause_node if btn_continue_popup_pause_node.exists() else None
                print(f"btn_continue_popup_pause: {btn_continue_popup_pause}")
                if btn_gem_revival_node:
                    if initial_resources["gem"] < 50:
                        poco.invoke("add_gem", amount=50)
                        logger.info("Not enough gems for revival, invoking add_gem")
                        initial_resources["gem"]+=50
                    sleep(1)
                    btn_gem_revival_node.click(sleep_interval=2)
                    initial_resources["gem"]-=revival_popup.gem_amount
                    logger.info(f"Clicked gem revival button, remaining initial gems: {initial_resources["gem"]}")
                    press_key(poco, "UP")
                    continue
                if btn_continue_popup_pause:
                    btn_continue_popup_pause.click(sleep_interval=2)
                    press_key(poco, "UP")
                    continue
                if not first_move:
                    # Initial setup: pause game and position player
                    for i in range(30):
                        press_key(poco,"P")
                    swipe(initial_plane_pos, start_pos)  # Move to starting position
                    press_key(poco,"UP")
                    first_move = True

                # Perform automated movement pattern
                press_key(poco,"T")  # Activate skill
                swipe(start_pos, end_pos, duration=1)

                # Collect resource amounts during gameplay (first collection)
                UI_tmp= UITop(poco.freeze())
                tmp = UI_tmp.collected_gold
                collected_gold = max(collected_gold, tmp) if tmp else collected_gold
                tmp_gem = UI_tmp.collected_gem
                collected_gem = max(collected_gem, tmp_gem) if tmp_gem else collected_gem

                # Return movement
                swipe(end_pos, start_pos, duration=1)

                # Collect resource amounts during gameplay (second collection)
                UI_tmp = UITop(poco.freeze())
                tmp = UI_tmp.collected_gold
                collected_gold = max(collected_gold, tmp) if tmp else collected_gold
                tmp_gem = UI_tmp.collected_gem
                collected_gem = max(collected_gem, tmp_gem) if tmp_gem else collected_gem

                # Check if game is still active
                btn = ui_ingame.btn_plane_skill if ui_ingame.btn_plane_skill.exists() else None

            # Add first-time completion rewards to collected amounts
            collected_gold += gold_1st_reward
            collected_gem += gem_1st_reward
            logger.info(f"Total collected (including first-time rewards): Gold: {collected_gold}, Gem: {collected_gem}")

    # ===============================================
    # PHASE 5: GAME COMPLETION HANDLING
    # ===============================================
    logger.info("Phase 5: Waiting for game completion")
    max_attempts = 5
    for attempt in range(max_attempts):
        popup_lose = PopupGameLose(poco)
        popup_win = PopupGameWin(poco)

        if popup_lose.root.exists():
            logger.info("Game lost - processing loss scenario")
            sleep(3)
            handle_endgame_popup(poco, logger)  # Handle any endgame popups
            bonus_gold= popup_lose.bonus_gold_amount
            print(f"bonus_gold from lose popup: {bonus_gold}")
            verify_game_resources("LOSE")
            wait_for_element(popup_lose.btn_next, timeout=8)

            # Navigate away from lose popup
            if popup_lose.btn_next:
                popup_lose.btn_next.click(sleep_interval=2)
                logger.info("Clicked next button from lose popup")
            elif popup_lose.btn_back:
                popup_lose.btn_back.click(sleep_interval=2)
                logger.info("Clicked back button from lose popup")
            else:
                press_key(poco,"BACK")
                logger.warning("No next or back button found in lose popup, using BACK keyevent")
            break
        elif popup_win.root.exists():
            logger.info("Game won - processing victory scenario")
            sleep(3)
            handle_endgame_popup(poco, logger)
            bonus_gold= popup_win.bonus_gold_amount
            print(f"bonus_gold from win popup: {bonus_gold}")
            verify_game_resources("WIN")
            wait_for_element(popup_win.btn_next, timeout=8)

            # Navigate away from win popup
            if popup_win.btn_next:
                popup_win.btn_next.click(sleep_interval=2)
                logger.info("Clicked next button from win popup")
            elif popup_win.btn_back:
                popup_win.btn_back.click(sleep_interval=2)
                logger.info("Clicked back button from win popup")
            else:
                press_key(poco,"BACK")
                sleep(2)
                logger.warning("No next or back button found in win popup, using BACK keyevent")
            break
        attempt += 1
        sleep(2)

        # Fail if neither win nor lose popup appears after max attempts
        if attempt >= max_attempts - 1:
            raise AssertionError("Game didn't reach a conclusion (win or lose) after maximum attempts")

    # ===============================================
    # PHASE 6: FINAL VERIFICATION ON HOME SCREEN
    # ===============================================
    logger.info("Phase 6: Performing final home screen verification")

    # Verify final resource amounts match expectations on home screen
    verify_home_screen_resources(poco, initial_resources, collected_gold,bonus_gold, collected_gem, logger)

    logger.info(f"=== COMPLETED LEVEL {target_level} TEST ===")

def handle_endgame_popup( poco, logger):
        """
        Handle endgame popups (win/lose) and navigate back popup game result.

        Args:
            poco: Poco instance
            logger: Logger instance for logging
        """
        max_attempts = 3
        for attempt in range(max_attempts):
            popup_video_endgame = EndGameVideoPopup(poco)
            popup_royalty_pack = RoyalPack(poco)
            popup_starter_pack = Popup_StarterPack(poco)
            popup_vip_pack = Popup_VipPack(poco)
            popup_premium_pack = Popup_PremiumPack(poco)
            popup_rate = None  # provide later
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

def verify_home_screen_resources(poco, initial_resources, collected_gold,bonus_gold, collected_gem, logger):
        """
        Navigate to home screen and verify final resource amounts match expected values.

        Args:
            poco: Poco instance
            initial_resources: Dict of initial resource amounts before game (gold, gem)
            collected_gold: Amount of gold collected during gameplay
            collected_gem: Amount of gem collected during gameplay
            logger: Logger instance for logging

        Returns:
            bool: True if verification passed, False otherwise
        """
        # Wait for navigation to complete and ensure we're at home screen
        sleep(8)

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
                press_key(poco,"BACK")
                sleep(2)
                if home_attempt == max_home_attempts - 1:
                    logger.error("Could not navigate to home screen for final verification")
                    return False

        # Final verification after successfully returning to home screen
        logger.info("=== PERFORMING FINAL HOME SCREEN VERIFICATION ===")

        # Get final resource amounts from home screen
        final_home_resources = get_resource_amount.get_all_resource_amounts(poco)
        logger.info(f"Final home resources: {final_home_resources}")

        # Calculate expected amounts based on initial + collected
        expected_final_gold = initial_resources["gold"] + collected_gold+ bonus_gold
        expected_final_gem = initial_resources["gem"] + collected_gem

        # Verify final home screen resources match expected amounts
        final_gold_verified = get_resource_amount.verify_resource_amount_change("gold", final_home_resources["gold"], expected_final_gold)
        final_gem_verified = get_resource_amount.verify_resource_amount_change("gem", final_home_resources["gem"], expected_final_gem)

        logger.info("=== FINAL HOME SCREEN VERIFICATION ===")
        logger.info(f"Initial resources - Gold: {initial_resources['gold']}, Gem: {initial_resources['gem']}")
        logger.info(f"Collected during game - Gold: {collected_gold}, Gem: {collected_gem}")
        logger.info(f"Expected final - Gold: {expected_final_gold}, Gem: {expected_final_gem}")
        logger.info(f"Actual final - Gold: {final_home_resources['gold']}, Gem: {final_home_resources['gem']}")

        verification_passed = final_gold_verified and final_gem_verified

        if verification_passed:
            logger.info("✓ Final home screen resource verification PASSED!")
        else:
            if not final_gold_verified:
                logger.error(f"✗ Final Gold verification FAILED! Expected: {expected_final_gold}, Actual: {final_home_resources['gold']}, Difference: {abs(expected_final_gold - final_home_resources['gold'])}")
            if not final_gem_verified:
                logger.error(f"✗ Final Gem verification FAILED! Expected: {expected_final_gem}, Actual: {final_home_resources['gem']}, Difference: {abs(expected_final_gem - final_home_resources['gem'])}")

            # Log the complete resource flow for debugging
            logger.error("=== RESOURCE FLOW DEBUG ===")
            logger.error(f"Initial → Final: Gold {initial_resources['gold']} → {final_home_resources['gold']} (Expected: {expected_final_gold})")
            logger.error(f"Initial → Final: Gem {initial_resources['gem']} → {final_home_resources['gem']} (Expected: {expected_final_gem})")
            logger.error(f"Collected amounts: Gold {collected_gold}, Gem {collected_gem}")

        logger.info("=== TEST COMPLETED ===")
        return verification_passed

