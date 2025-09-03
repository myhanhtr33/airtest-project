﻿import cv2
from scripts.regsetup import description

from Hierarchy.HOME_Element import HomeSquad
from Hierarchy.PopupCampaignSelectLv import PopupCampaignSelectLv, PanelWorlds
from Hierarchy.PopupLevelPrepare import PopupLevelPrepare
from Hierarchy.Tutorial_UI import *
from Hierarchy.UI_ingame import *
# from airtest.core.api import keyevent, swipe, sleep, Template, wait, exists
from airtest.core.api import *
from utils import get_resource_amount
import pytest
import os
from logger_config import get_logger
from utils.get_resource_amount import get_single_resource_amount
from utils.helper_functions import wait_for_element
from utils.test_level_helper import *
current_dir=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
img_path= os.path.join(os.path.dirname(current_dir),"image","Plane1_bata.png")
bata_img = Template(img_path)
img_path= os.path.join(os.path.dirname(current_dir),"image","Tut","Handtut.png")
hand_tut_img = Template(img_path)
lv8_hand_tut_img = Template(img_path, threshold=0.5)
img_path= os.path.join(os.path.dirname(current_dir),"image","Tut","BigIconTut_Event_6.png")
event_icon= Template(img_path)
img_path= os.path.join(os.path.dirname(current_dir),"image","Tut","tutLv_noti_frame.png")
ingame_noti_img = Template(img_path)


@pytest.mark.use_to_home(before=True, after=True, logger_name="Level1_tut")
@pytest.mark.use_to_campaign_select_lv(before=True)
class TestLevel1_tut:
    def setup(self):
        pass
    def from_home_to_campaign_select(self, poco, logger):
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
    def swipe_to_world_item(self, popup_campaign, target_world_indexu, max_attempts=10):
        """
        ORIGINAL VERSION - Swipe to find and display the target WorldItem in the scrollview.
        The scrollview shows 6 visible elements at a time.
        Optimized with intelligent swipe distance calculation to minimize attempts.

        Args:
            popup_campaign: PopupCampaignSelectLv instance
            target_world_index: The index (1-based) of the world to find
            max_attempts: Maximum number of swipe attempts

        Returns:
            WorldItem if found, None otherwise
        """
        logger = get_logger("Level1_tut")
        panel_worlds = popup_campaign.panel_worlds

        if not panel_worlds:
            logger.error("Panel worlds not found")
            return None

        # Get reference positions
        title_pos = panel_worlds.title.get_position()

        # Cache world objects and indices on first attempt only
        cached_worlds = None
        avg_vertical_distance = None
        worlds_per_swipe = None

        for attempt in range(max_attempts):
            logger.info(f"ORIGINAL: Attempt {attempt + 1}: Looking for World {target_world_index}")

            # Only build cache on first attempt or if cache is empty
            if cached_worlds is None:
                logger.info("ORIGINAL: Building world cache...")
                list_world = panel_worlds.list_world
                if not list_world:
                    logger.warning("No worlds found in current view")
                    continue

                # Build cache of valid worlds with their indices
                cached_worlds = []
                for world in list_world:
                    try:
                        world_index = int(world.index) if world.index and world.index.isdigit() else None
                        if world_index:
                            cached_worlds.append((world, world_index))
                    except (ValueError, AttributeError):
                        continue

                if len(cached_worlds) < 2:
                    logger.warning("Not enough valid worlds found")
                    continue

                logger.info(f"ORIGINAL: Cached {len(cached_worlds)} valid worlds")

            # Get current positions for cached worlds (much faster than re-parsing)
            valid_worlds_with_pos = []

            for world, world_index in cached_worlds:
                try:
                    pos = world.root.get_position()
                    valid_worlds_with_pos.append((world, world_index, pos))
                except:
                    # Skip if world is no longer accessible
                    continue

            if len(valid_worlds_with_pos) < 2:
                logger.warning("Not enough worlds with valid positions")
                continue

            # Calculate average vertical distance only once
            if avg_vertical_distance is None:
                # Sort by Y position to calculate distance
                valid_worlds_with_pos.sort(key=lambda x: x[2][1])

                vertical_distances = []
                for i in range(1, min(10, len(valid_worlds_with_pos))):
                    vertical_distance = abs(valid_worlds_with_pos[i][2][1] - valid_worlds_with_pos[i-1][2][1])
                    vertical_distances.append(vertical_distance)

                avg_vertical_distance = sum(vertical_distances) / len(vertical_distances) if vertical_distances else 0
                logger.info(f"ORIGINAL: Calculated average vertical distance: {avg_vertical_distance}")

            # Find visible threshold
            visible_threshold = title_pos[1] + avg_vertical_distance

            # Filter visible worlds (y > visible_threshold)
            visible_worlds = []
            for world, world_index, world_pos in valid_worlds_with_pos:
                if world_pos[1] > visible_threshold:
                    visible_worlds.append((world, world_index, world_pos))

            # Sort visible worlds by Y position and take first 8
            visible_worlds.sort(key=lambda x: x[2][1])
            visible_worlds = visible_worlds[:8]

            if not visible_worlds:
                logger.warning("No visible worlds found")
                continue

            # Sort by world index for easier processing
            visible_worlds_by_index = sorted(visible_worlds, key=lambda x: x[1])
            visible_indices = [w[1] for w in visible_worlds_by_index]
            logger.info(f"ORIGINAL: Visible worlds: {visible_indices}")

            # Check if target world is among the visible elements
            for world, world_index, world_pos in visible_worlds:
                if world_index == target_world_index:
                    logger.info(f"ORIGINAL: Found target World {target_world_index} at position {world_pos}")
                    return world

            # Calculate worlds per swipe for intelligent swiping
            if worlds_per_swipe is None and attempt > 0:
                # Calculate based on previous swipe result
                prev_first_visible = getattr(self, '_prev_first_visible', None)
                if prev_first_visible is not None:
                    current_first_visible = visible_worlds_by_index[0][1]
                    worlds_per_swipe = abs(current_first_visible - prev_first_visible)
                    logger.info(f"ORIGINAL: Calculated worlds per swipe: {worlds_per_swipe}")

            # Store current first visible for next calculation
            self._prev_first_visible = visible_worlds_by_index[0][1]

            # Determine swipe direction and calculate intelligent swipe distance
            if not visible_worlds_by_index:
                continue

            first_visible_index = visible_worlds_by_index[0][1]
            last_visible_index = visible_worlds_by_index[-1][1]

            # Calculate swipe parameters
            screen_center_x = panel_worlds.root.get_position()[0]
            first_visible_y = visible_worlds[0][2][1]
            last_visible_y = visible_worlds[-1][2][1]
            single_swipe_distance = abs(last_visible_y - first_visible_y)

            # Calculate how many worlds we need to move
            if target_world_index < first_visible_index:
                worlds_to_move = first_visible_index - target_world_index
                # Add buffer to ensure target is in visible range
                worlds_to_move += 3
                direction = "down"
            elif target_world_index > last_visible_index:
                worlds_to_move = target_world_index - last_visible_index
                # Add buffer to ensure target is in visible range
                worlds_to_move += 3
                direction = "up"
            else:
                # Target should be visible but wasn't found - try a small adjustment
                logger.warning(f"Target {target_world_index} should be visible but not found, trying small swipe")
                worlds_to_move = 2
                direction = "up"

            # Calculate swipe multiplier based on worlds to move
            if worlds_per_swipe and worlds_per_swipe > 0:
                swipe_multiplier = max(1.0, worlds_to_move / worlds_per_swipe)
            else:
                # Use estimated multiplier based on typical scrollview behavior
                estimated_worlds_per_swipe = 6  # Based on log showing ~6-7 worlds per swipe
                swipe_multiplier = max(1.0, worlds_to_move / estimated_worlds_per_swipe)

            # Cap the multiplier to prevent overshooting
            swipe_multiplier = min(swipe_multiplier, 5.0)

            logger.info(f"ORIGINAL: Target {target_world_index}, visible range [{first_visible_index}-{last_visible_index}]")
            logger.info(f"ORIGINAL: Need to move {worlds_to_move} worlds {direction}, swipe multiplier: {swipe_multiplier:.2f}")

            if direction == "down":
                swipe_start = (screen_center_x, first_visible_y)
                swipe_end = (screen_center_x, first_visible_y + single_swipe_distance * swipe_multiplier)
            else:  # direction == "up"
                swipe_start = (screen_center_x, last_visible_y)
                swipe_end = (screen_center_x, last_visible_y - single_swipe_distance * swipe_multiplier)

            # Perform swipe

            # Normalize coordinates to range [-1, 1]
            norm_start = (max(min(swipe_start[0], 1), -1), max(min(swipe_start[1], 1), -1))
            norm_end = (max(min(swipe_end[0], 1), -1), max(min(swipe_end[1], 1), -1))
            logger.info(f"ORIGINAL: Swiping from {norm_start} to {norm_end}")
            swipe(norm_start, norm_end, duration=0.5)
            sleep(1)  # Wait for animation to complete

        logger.error(f"ORIGINAL: Could not find World {target_world_index} after {max_attempts} attempts")
        return None
    def handle_endgame_popup(self, poco, logger):
        """
        Handle endgame popups (win/lose) and navigate back popup game result.

        Args:
            poco: Poco instance
            logger: Logger instance for logging
        """
        max_attempts = 3
        popup_video_endgame = EndGameVideoPopup(poco)
        popup_rate=None # provide later
        for attempt in range(max_attempts):
            if popup_video_endgame.root.exists():
                logger.info("EndGameVideoPopup found, handling...")
                popup_video_endgame.tap_close_text.click(sleep_interval=1)
            if not popup_video_endgame.root.exists():
                logger.info("EndGameVideoPopup closed successfully")
                break
            attempt += 1
            sleep(1)
    def verify_home_screen_resources(self, poco, initial_resources, collected_gold, collected_gem, logger):
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
        current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
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
                keyevent("BACK")
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
        expected_final_gold = initial_resources["gold"] + collected_gold
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

    def play_and_verify_level(self, poco, target_level, logger_name="Level1_tut"):
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
        # ===============================================
        # PHASE 1: INITIALIZATION AND SETUP
        # ===============================================
        logger = get_logger(logger_name)
        logger.info(f"=== STARTING LEVEL {target_level} TEST ===")

        # Initialize UI components for level selection
        popup_campaign = PopupCampaignSelectLv(poco)
        panel_worlds = PanelWorlds(poco)

        # Verify we're in the campaign selection screen
        assert popup_campaign.root.exists(), "PopupCampaignSelectLv not found"

        # ===============================================
        # PHASE 2: LEVEL NAVIGATION AND PREPARATION
        # ===============================================
        logger.info(f"Phase 2: Navigating to Level {target_level}")

        # Check if this is the maximum unlocked level (affects rewards)
        is_max_level = is_max_unlocked_level(target_level, popup_campaign.list_level_normal)
        gold_1st_reward = 0
        gem_1st_reward = 0

        # Navigate to the target level
        click_to_level = navigate_and_click_level(popup_campaign, target_level, panel_worlds, logger_name=logger_name)
        if not click_to_level:
            logger.error(f"Failed to navigate to Level {target_level}")
            return

        # Verify level preparation screen is displayed
        popup_prepare = PopupLevelPrepare(poco)
        assert popup_prepare.root.exists(), f"PopupLevelPrepare not found after clicking level {target_level}"

        # Capture first-time completion rewards if this is max unlocked level
        if is_max_level:
            gold_1st_reward = popup_prepare.gold_reward_amount
            gem_1st_reward = popup_prepare.gem_reward_amount
            logger.info(f"Level {target_level} is max level. Gold 1st reward: {gold_1st_reward}, Gem 1st reward: {gem_1st_reward}")

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
            expected_gold = initial_resources["gold"] + collected_gold
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
                    logger.error(f"✗ Gold verification failed! Expected: {expected_gold}, Actual: {final_gold}, Difference: {abs(expected_gold - final_gold)}")
                if not gem_verified:
                    logger.error(f"✗ Gem verification failed! Expected: {expected_gem}, Actual: {final_gem}, Difference: {abs(expected_gem - final_gem)}")

        # ===============================================
        # PHASE 4: AUTOMATED GAMEPLAY LOOP
        # ===============================================
        logger.info("Phase 4: Starting automated gameplay")

        if wait_for_element(ui_ingame.root, timeout=5):
            # Locate game elements for automated play
            bata_pos = wait(bata_img, timeout=6)  # Player character position
            btn_skill_pos = ui_ingame.btn_plane_skill.get_position() if ui_ingame.btn_plane_skill.exists() else None

            if bata_pos and btn_skill_pos:
                # Calculate movement positions for automated gameplay
                start_pos = ((bata_pos[0] - btn_skill_pos[0]) / 2 + btn_skill_pos[0], bata_pos[1])
                end_pos = (bata_pos[0] + (bata_pos[0] - start_pos[0]), bata_pos[1])

                ingameUI = UI_Ingame(poco)
                btn = ingameUI.btn_plane_skill if ingameUI.btn_plane_skill.exists() else None
                btn_gem_revival_popup_node = RevivalPopup(poco).btn_gem
                btn_gem_revival_popup = btn_gem_revival_popup_node if btn_gem_revival_popup_node.exists() else None
                first_move = False

                # Main gameplay loop - continues until skill button disappears (game ends)
                while btn:
                    if btn_gem_revival_popup:
                        if get_single_resource_amount(poco, "gem")<50:
                            self.poco.invoke("add_gem", amount=50)
                            # logger.info("Not enough gems for revival, invoking add_gem")
                        sleep(1)
                        btn_gem_revival_popup.click(sleep_interval=1)
                        sleep(2)
                        continue
                    if not first_move:
                        # Initial setup: pause game and position player
                        for i in range(30):
                            keyevent("P")  # Pause to ensure stable state
                        swipe(bata_pos, start_pos)  # Move to starting position
                        keyevent("DPAD_UP")
                        first_move = True

                    # Perform automated movement pattern
                    keyevent("T")  # Activate skill
                    swipe(start_pos, end_pos, duration=1)

                    # Collect resource amounts during gameplay (first collection)
                    tmp = UITop(poco).collected_gold
                    collected_gold = max(collected_gold, tmp) if tmp else collected_gold
                    tmp_gem = UITop(poco).collected_gem
                    collected_gem = max(collected_gem, tmp_gem) if tmp_gem else collected_gem

                    # Return movement
                    swipe(end_pos, start_pos, duration=1)
                    sleep(0.5)

                    # Collect resource amounts during gameplay (second collection)
                    tmp = UITop(poco).collected_gold
                    collected_gold = max(collected_gold, tmp) if tmp else collected_gold
                    tmp_gem = UITop(poco).collected_gem
                    collected_gem = max(collected_gem, tmp_gem) if tmp_gem else collected_gem

                    # Check if game is still active
                    btn = ingameUI.btn_plane_skill if ingameUI.btn_plane_skill.exists() else None

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
                self.handle_endgame_popup(poco, logger)  # Handle any endgame popups
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
                    keyevent("BACK")
                    logger.warning("No next or back button found in lose popup, using BACK keyevent")
                break

            elif popup_win.root.exists():
                logger.info("Game won - processing victory scenario")
                sleep(3)
                self.handle_endgame_popup(poco, logger)
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
                    keyevent("BACK")
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
        self.verify_home_screen_resources(poco, initial_resources, collected_gold, collected_gem, logger)

        logger.info(f"=== COMPLETED LEVEL {target_level} TEST ===")

    def tutorial_play_level(self, poco, target_level, logger_name="Level1_tut"):
        # ===============================================
        # PHASE 1: INITIALIZATION AND SETUP
        # ===============================================
        logger = get_logger(logger_name)
        logger.info(f"=== STARTING LEVEL {target_level} TEST ===")

        # Initialize UI components for level selection
        popup_campaign = PopupCampaignSelectLv(poco)
        panel_worlds = PanelWorlds(poco)

        # Verify we're in the campaign selection screen
        assert popup_campaign.root.exists(), "PopupCampaignSelectLv not found"

        # ===============================================
        # PHASE 2: LEVEL NAVIGATION AND PREPARATION
        # ===============================================
        logger.info(f"Phase 2: Navigating to Level {target_level}")

        # Check if this is the maximum unlocked level (affects rewards)
        is_max_level = is_max_unlocked_level(target_level, popup_campaign.list_level_normal)
        gold_1st_reward = 0
        gem_1st_reward = 0

        # Navigate to the target level
        click_to_level = navigate_and_click_level(popup_campaign, target_level, panel_worlds,
                                                  logger_name=logger_name)
        if not click_to_level:
            logger.error(f"Failed to navigate to Level {target_level}")
            return

        # Verify level preparation screen is displayed
        popup_prepare = PopupLevelPrepare(poco)
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
            expected_gold = initial_resources["gold"] + collected_gold
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
            # Locate game elements for automated play
            bata_pos = wait(bata_img, timeout=6)  # Player character position
            btn_skill_pos = ui_ingame.btn_plane_skill.get_position() if ui_ingame.btn_plane_skill.exists() else None

            if bata_pos and btn_skill_pos:
                # Calculate movement positions for automated gameplay
                start_pos = ((bata_pos[0] - btn_skill_pos[0]) / 2 + btn_skill_pos[0], bata_pos[1])
                end_pos = (bata_pos[0] + (bata_pos[0] - start_pos[0]), bata_pos[1])

                ingameUI = UI_Ingame(poco)
                btn = ingameUI.btn_plane_skill if ingameUI.btn_plane_skill.exists() else None
                btn_gem_revival_popup_node = RevivalPopup(poco).btn_gem
                btn_gem_revival_popup = btn_gem_revival_popup_node if btn_gem_revival_popup_node.exists() else None
                first_move = False

                # Main gameplay loop - continues until skill button disappears (game ends)
                while btn:
                    if btn_gem_revival_popup:
                        if get_single_resource_amount(poco, "gem") < 50:
                            self.poco.invoke("add_gem", amount=50)
                            # logger.info("Not enough gems for revival, invoking add_gem")
                        sleep(1)
                        # logger.info("Revival popup detected, clicking revive button")
                        btn_gem_revival_popup.click(sleep_interval=1)
                        sleep(2)
                        continue
                    if not first_move:
                        # Initial setup: pause game and position player
                        for i in range(30):
                            keyevent("P")  # Pause to ensure stable state
                        swipe(bata_pos, start_pos)  # Move to starting position
                        keyevent("DPAD_UP")
                        first_move = True

                    # Perform automated movement pattern
                    keyevent("T")  # Activate skill
                    swipe(start_pos, end_pos, duration=1)

                    # Collect resource amounts during gameplay (first collection)
                    tmp = UITop(poco).collected_gold
                    collected_gold = max(collected_gold, tmp) if tmp else collected_gold
                    tmp_gem = UITop(poco).collected_gem
                    collected_gem = max(collected_gem, tmp_gem) if tmp_gem else collected_gem

                    # Return movement
                    swipe(end_pos, start_pos, duration=1)
                    sleep(0.5)

                    # Collect resource amounts during gameplay (second collection)
                    tmp = UITop(poco).collected_gold
                    collected_gold = max(collected_gold, tmp) if tmp else collected_gold
                    tmp_gem = UITop(poco).collected_gem
                    collected_gem = max(collected_gem, tmp_gem) if tmp_gem else collected_gem

                    # Check if game is still active
                    btn = ingameUI.btn_plane_skill if ingameUI.btn_plane_skill.exists() else None

                # Add first-time completion rewards to collected amounts
                collected_gold += gold_1st_reward
                collected_gem += gem_1st_reward
                logger.info(
                    f"Total collected (including first-time rewards): Gold: {collected_gold}, Gem: {collected_gem}")

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
                self.handle_endgame_popup(poco, logger)
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
                    keyevent("BACK")
                    logger.warning("No next or back button found in lose popup, using BACK keyevent")
                break

            elif popup_win.root.exists():
                logger.info("Game won - processing victory scenario")
                sleep(3)
                self.handle_endgame_popup(poco, logger)
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
                    keyevent("BACK")
                    sleep(2)
                    logger.warning("No next or back button found in win popup, using BACK keyevent")
                break

            attempt += 1
            sleep(3)

            # Fail if neither win nor lose popup appears after max attempts
            if attempt >= max_attempts - 1:
                raise AssertionError("Game didn't reach a conclusion (win or lose) after maximum attempts")

        logger.info(f"=== COMPLETED LEVEL {target_level} TEST ===")

    @pytest.mark.order(1)
    def test_playLv1_and_tutLv1(self,poco):

        # ===============================================
        # PHASE 1: INITIALIZATION AND SETUP
        # ===============================================
        target_level=1
        logger = get_logger("playing lv1 and tut lv1")
        logger.info(f"=== STARTING LEVEL {target_level} TEST ===")

        # Initialize UI components for level selection
        popup_campaign = PopupCampaignSelectLv(poco)
        panel_worlds = PanelWorlds(poco)

        # Verify we're in the campaign selection screen
        assert popup_campaign.root.exists(), "PopupCampaignSelectLv not found"

        # ===============================================
        # PHASE 2: LEVEL NAVIGATION AND PREPARATION
        # ===============================================
        logger.info(f"Phase 2: Navigating to Level {target_level}")

        # Check if this is the maximum unlocked level (affects rewards)
        is_max_level = is_max_unlocked_level(target_level, popup_campaign.list_level_normal)
        gold_1st_reward = 0
        gem_1st_reward = 0

        # Navigate to the target level
        click_to_level = navigate_and_click_level(popup_campaign, target_level, panel_worlds, logger_name="playing tut lv1")
        if not click_to_level:
            logger.error(f"Failed to navigate to Level {target_level}")
            return

        # Verify level preparation screen is displayed
        popup_prepare = PopupLevelPrepare(poco)
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
            expected_gold = initial_resources["gold"] + collected_gold
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
        btn_active_skill_tut = poco("fadeCooldownActiveSkills")
        tutLv1_P1_1 = None
        tutLv1_P1_2 = None
        is_complete_tutLv1_P1 = None
        is_complete_tutLv1_P2 = None
        if wait_for_element(ui_ingame.root, timeout=5):
            # Locate game elements for automated play
            bata_pos = wait(bata_img, timeout=6)  # Player character position
            btn_skill_pos = ui_ingame.btn_plane_skill.get_position() if ui_ingame.btn_plane_skill.exists() else None

            if bata_pos and btn_skill_pos:
                # Calculate movement positions for automated gameplay
                start_pos = ((bata_pos[0] - btn_skill_pos[0]) / 2 + btn_skill_pos[0], bata_pos[1])
                end_pos = (bata_pos[0] + (bata_pos[0] - start_pos[0]), bata_pos[1])

                ingameUI = UI_Ingame(poco)
                btn = ingameUI.btn_plane_skill if ingameUI.btn_plane_skill.exists() else None
                first_move = False

                # Main gameplay loop - continues until skill button disappears (game ends)
                while btn:
                    if not first_move:
                        # Initial setup: pause game and position player
                        for i in range(30):
                            keyevent("P")  # Pause to ensure stable state
                        swipe(bata_pos, start_pos)  # Move to starting position
                        first_move = True
                    if not tutLv1_P1_1:
                        try:
                            tutLv1_P1_1 = wait(hand_tut_img, timeout=6)
                            tutLv1_P1_2 = wait(ingame_noti_img, timeout=6)
                            btn_active_skill_tut.click(sleep_interval=1)
                            is_complete_tutLv1_P1 = tutLv1_P1_1 is not None and tutLv1_P1_2 is not None
                            logger.info(
                                f"::::::::::::::::tutLv1_1_1: {tutLv1_P1_1}, tutLv1_1_2: {tutLv1_P1_2}, is_complete_tutLv1_P1: {is_complete_tutLv1_P1}")
                        except TargetNotFoundError:
                            logger.warning("Hand tutorial image or ingame notification frame not found, continuing...")

                    # Perform automated movement pattern
                    keyevent("T")  # Activate skill
                    swipe(start_pos, end_pos, duration=2)

                    # Collect resource amounts during gameplay (first collection)
                    tmp = UITop(poco).collected_gold
                    collected_gold = max(collected_gold, tmp) if tmp else collected_gold
                    tmp_gem = UITop(poco).collected_gem
                    collected_gem = max(collected_gem, tmp_gem) if tmp_gem else collected_gem

                    # Return movement
                    swipe(end_pos, start_pos, duration=2)
                    sleep(1)

                    # Collect resource amounts during gameplay (second collection)
                    tmp = UITop(poco).collected_gold
                    collected_gold = max(collected_gold, tmp) if tmp else collected_gold
                    tmp_gem = UITop(poco).collected_gem
                    collected_gem = max(collected_gem, tmp_gem) if tmp_gem else collected_gem

                    # Check if game is still active
                    btn = ingameUI.btn_plane_skill if ingameUI.btn_plane_skill.exists() else None

                # Add first-time completion rewards to collected amounts
                collected_gold += gold_1st_reward
                collected_gem += gem_1st_reward
                logger.info(
                    f"Total collected (including first-time rewards): Gold: {collected_gold}, Gem: {collected_gem}")

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
                self.handle_endgame_popup(poco, logger)  # Handle any endgame popups
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
                    keyevent("BACK")
                    logger.warning("No next or back button found in lose popup, using BACK keyevent")
                break

            elif popup_win.root.exists():
                logger.info("Game won - processing victory scenario")
                sleep(3)
                self.handle_endgame_popup(poco, logger)
                verify_game_resources("WIN")
                try:
                    tutLv1_P2 = wait(hand_tut_img, timeout=15)
                    if tutLv1_P2:
                        btn_back = popup_win.btn_back
                        if btn_back:
                            btn_back.click(sleep_interval=1)
                            is_complete_tutLv1_P2 = True
                            print("Back button clicked after win popup")
                        else:
                            logger.warning("Back button not found after win popup")
                    else:
                        logger.warning("Hand tutorial image not found after win popup")
                except TargetNotFoundError:
                    logger.warning("Hand tutorial image not found after win popup")
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
        self.verify_home_screen_resources(poco, initial_resources, collected_gold, collected_gem, logger)
        if is_complete_tutLv1_P1 and is_complete_tutLv1_P2:
            logger.info("Tutorial Level 1 completed successfully.")
        else:
            logger.error("Tutorial Level 1 did not complete successfully. Check the logs for details.")
        logger.info(f"=== COMPLETED LEVEL {target_level} TEST ===")

    @pytest.mark.order(2)
    def test_playLv2_lv3(self,poco):
        logger= get_logger("playing lv2 and lv3")
        self.play_and_verify_level(poco, 2, logger_name="playing lv2 ")
        self.from_home_to_campaign_select(poco,logger)
        self.play_and_verify_level(poco, 3, logger_name="playing lv3 ")

    @pytest.mark.order(3)
    def test_playLv4_and_tutLv5(self, poco):
        """
        Test case to play Level 4 and then the tutorial for Level 5.
        This function will first play Level 4 and then immediately start the tutorial for Level 5.
        """
        logger = get_logger("Level4_tut")
        self.tutorial_play_level(poco, 4, logger_name="Level4_tutLv5")
        tut_manager = TutorialManager(poco)

        # Start the tutorial for Level 5
        logger.info("Starting tutorial for Level 5")
        # NPC popup interaction
        popup_npc = PopupNPC(poco)
        npc_img = popup_npc.npc_image_template
        print(f"npc_img: {npc_img}")
        try:
            result = wait(npc_img, timeout=5)
            print(f"npc: {result}")
        except TargetNotFoundError as e:
            print(f"npc not found: {e}")
        popup_npc.btn_go.click(sleep_interval=2)

        # Receive Drone popup interaction
        popup_drone = PopupReceiveDrone(poco)
        drone_img = popup_drone.drone1_image_template
        print(f"drone_img: {drone_img}")
        try:
            result = wait(drone_img, timeout=5)
            print(f"drone: {result}")
        except TargetNotFoundError as e:
            print(f"drone not found: {e}")
        print(f"drone_name: {popup_drone.drone_name}")
        print(f"message: {popup_drone.message}")
        btn_claim = tut_manager.btn_claim
        if btn_claim:
            print("btn_claim exists")
            btn_claim.click(sleep_interval=2)

        # Click squad from home screen
        try:
            result = wait(hand_tut_img, timeout=5)
            print(f"hand_tut_img found: {result}")
        except TargetNotFoundError as e:
            print(f"hand_tut_img not found: {e}")
        home_squad = HomeSquad(poco)
        circle_btn = home_squad.squad_0.circle
        if circle_btn:
            print(f"circle button exists: {circle_btn}")
            circle_btn.click(sleep_interval=2)

        # Click left drone position in hangar
        try:
            result = wait(hand_tut_img, timeout=5)
            print(f"hand_tut_img found: {result}")
        except TargetNotFoundError as e:
            print(f"hand_tut_img not found: {e}")
        btn_left_drone = tut_manager.btn_left_drone
        if btn_left_drone:
            print(f"btn_left_drone exists: {btn_left_drone}")
            btn_left_drone.click(sleep_interval=2)

        # Click equip drone button in hangar
        try:
            result = wait(hand_tut_img, timeout=5)
            print(f"hand_tut_img found: {result}")
        except TargetNotFoundError as e:
            print(f"hand_tut_img not found: {e}")
        btn_equip_drone = tut_manager.btn_equip_drone
        if btn_equip_drone:
            print(f"btn_equip_drone exists: {btn_equip_drone}")
            btn_equip_drone.click(sleep_interval=1)


    @pytest.mark.order(4)
    def test_playLv5_lv6(self, poco):
        logger= get_logger("playing lv5 and lv6")
        self.play_and_verify_level(poco, 5, logger_name="playing lv5")
        self.from_home_to_campaign_select(poco, logger)
        self.play_and_verify_level(poco, 6, logger_name="playing lv6")

    @pytest.mark.order(5)
    def test_play_lv7_and_tutlv8(self, poco):
        logger= get_logger("playing lv7 and tut lv8")
        self.tutorial_play_level(poco, 7, logger_name="playing lv7 and tut lv8")
        tut_manager= TutorialManager(poco)

        logger.info("Starting tutorial for Level 8")
        # NPC popup interaction
        popup_npc = PopupNPC(poco)
        npc_img = popup_npc.npc_image_template
        print(f"npc_img: {npc_img}")
        try:
            result = wait(npc_img, timeout=5)
            print(f"npc: {result}")
        except TargetNotFoundError as e:
            print(f"npc not found: {e}")
        popup_npc.btn_go.click(sleep_interval=2)

        popup_drone= PopupReceiveDrone(poco)
        drone_img= popup_drone.drone2_image_template
        print(f"drone_img: {drone_img}")
        try:
            result= wait(drone_img, timeout=5)
            print(f"drone: {result}")
        except TargetNotFoundError as e:
            print(f"drone not found: {e}")
        print(f"drone_name: {popup_drone.drone_name}")
        print(f"message: {popup_drone.message}")
        btn_claim = tut_manager.btn_claim
        if btn_claim:
            print("btn_claim exists")
            btn_claim.click(sleep_interval=2)

        try:
            result= wait(hand_tut_img, timeout=5)
            print(f"hand_tut_img found: {result}")
        except TargetNotFoundError as e:
            print(f"hand_tut_img not found: {e}")
        home_squad= HomeSquad(poco)
        circle_btn= home_squad.squad_0.circle
        if circle_btn:
            print(f"circle button exists: {circle_btn}")
            circle_btn.click(sleep_interval=2)

        try:
            result= wait(hand_tut_img, timeout=5)
            print(f"hand_tut_img found: {result}")
        except TargetNotFoundError as e:
            print(f"hand_tut_img not found: {e}")
        btn_right_drone= tut_manager.btn_right_drone
        if btn_right_drone:
            print(f"btn_left_drone exists: {btn_right_drone}")
            btn_right_drone.click(sleep_interval=2)

        try:
            result= wait(hand_tut_img, timeout=5)
            print(f"hand_tut_img found: {result}")
        except TargetNotFoundError as e:
            print(f"hand_tut_img not found: {e}")
        btn_equip_drone= tut_manager.btn_equip_drone
        if btn_equip_drone:
            print(f"btn_equip_drone exists: {btn_equip_drone}")
            btn_equip_drone.click(sleep_interval=1)

        try:
            result= wait(hand_tut_img, timeout=5)
            print(f"hand_tut_img found: {result}")
        except TargetNotFoundError as e:
            print(f"hand_tut_img not found: {e}")
        btn_back=tut_manager.btn_back_from_hangar
        if btn_back:
            print(f"btn_back exists: {btn_back}")
            btn_back.click(sleep_interval=2)

        event_icon_pos=None
        try:
            event_icon_pos= wait(event_icon, timeout=5)
            logger.info(f"event icon found: {event_icon_pos}")
        except TargetNotFoundError as e:
            logger.warning(f"hand_tut_img not found: {e}")
        description= tut_manager.lv8_panel_description
        title= tut_manager.lv8_panel_title
        if description== "New feature unlock" and title== "Continue":
            logger.info("Tutorial Level 8 description and title verified successfully.")
        else:
            logger.warning(f"Tutorial Level 8 description or title mismatch! Expected: 'New feature unlock' and 'Continue', but got: {description} and {title}")
        if event_icon_pos:
            click(event_icon_pos) # Click the event icon
            sleep(2)

        try:
            result= wait(tut_manager.lv8_hand_click_event_on_navigator_template, timeout=5)
        except TargetNotFoundError as e:
            print(f"hand_tut_img not found: {e}")
        if tut_manager.lv8_btn_event_on_navigator:
            tut_manager.lv8_btn_event_on_navigator.click(sleep_interval=1)
        popup_event=poco("Popup_Event_Home(Clone)")
        is_popup_event= popup_event.exists()
        if is_popup_event:
            logger.info(f"Popup event found: {is_popup_event}")
        else:
            logger.error(f"Popup event not found: {is_popup_event}")






