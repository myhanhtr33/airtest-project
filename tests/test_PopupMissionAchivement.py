from airtest.core.api import *

from Hierarchy.PopupMissionAchivement import *
import pytest
from logger_config import get_logger
import time

@pytest.fixture(scope="class")
def PopupMissionAchivement_back_btn(poco):
    try:
        button = poco("Popup_MissionAchivement_2022(Clone)").offspring("btnBack")
        return button if button.exists() else None
    except Exception as e:
        # Handle RPC timeout or other connection errors when screen is on different page
        logger = get_logger()
        logger.warning(f"Failed to access PopupMissionAchivement back button due to connection error: {e}")
        return None

@pytest.mark.use_to_home(before=True, after=True, logger_name="PopupMission", back_button="PopupMissionAchivement_back_btn")
class TestPopupMissionAchivement:
    @pytest.fixture(scope="function", autouse=True)
    def setup(self, poco):
        logger = get_logger("setup method")
        logger.info("Setting up PopupMissionAchivement test environment...")
        self.poco = poco
        home_icon = poco("SubFeatureTopLayer").offspring("Quest_Home")
        assert home_icon.exists(), "Mission home icon not found!"
        home_icon.click(sleep_interval=1)
        self.popup = PopupMissionAchivement(poco)
        assert self.popup.root.exists(), "PopupMissionAchivement not found!"
        logger.info("PopupMissionAchivement setup completed successfully")

    @pytest.mark.order(1)
    def test_main_elements(self):
        """Test that all main elements in __init__ are always present when popup opens"""
        logger = get_logger()
        logger.info("Testing main elements presence in PopupMissionAchivement...")

        # Test root element
        assert self.popup.root.exists(), "PopupMissionAchivement root not found!"
        logger.info("✓ Root element exists")

        # Test back button
        assert self.popup.btn_back.exists(), "Back button not found!"
        logger.info("✓ Back button exists")

        # Test all three tab buttons
        assert self.popup.btn_daily.exists(), "Daily button not found!"
        logger.info("✓ Daily button exists")

        assert self.popup.btn_weekly.exists(), "Weekly button not found!"
        logger.info("✓ Weekly button exists")

        assert self.popup.btn_achievement.exists(), "Achievement button not found!"
        logger.info("✓ Achievement button exists")

    @pytest.mark.order(2)
    def test_battle_pass_panel_elements(self):
        """Test that all elements in battle_pass_panel property are always present"""
        logger = get_logger()
        logger.info("Testing battle pass panel elements...")

        battle_pass = self.popup.battle_pass_panel

        # Test title
        title = battle_pass.title
        assert title, "Battle pass title not found!"
        logger.info(f"✓ Battle pass title: {title}")

        # Test progress fill
        assert battle_pass.progress_fill.exists(), "Battle pass progress fill not found!"
        logger.info("✓ Battle pass progress fill exists")

        # Test level
        level = battle_pass.level
        assert level, "Battle pass level not found!"
        logger.info(f"✓ Battle pass level: {level}")

        # Test progress text
        progress_text = battle_pass.progress_text
        assert progress_text, "Battle pass progress text not found!"
        logger.info(f"✓ Battle pass progress text: {progress_text}")

        # Test countdown
        countdown = battle_pass.countdown
        assert countdown, "Battle pass countdown not found!"
        logger.info(f"✓ Battle pass countdown: {countdown}")

    @pytest.mark.order(3)
    def test_daily_tab_button_and_content(self):
        """Test daily button sprite state and daily tab availability after click"""
        logger = get_logger()
        logger.info("Testing daily tab button and content...")

        # Click daily button
        self.popup.btn_daily.click(sleep_interval=1)

        # Check daily button is active
        daily_active = UIButtonUtils.check_sprite_btn_active(self.popup.btn_daily)
        if daily_active:
            logger.info("✓ Daily button is in active state")
        else:
            logger.error("✗ Daily button is not in active state")

        # Check other buttons are deactivated
        weekly_inactive = UIButtonUtils.check_sprite_btn_deactive(self.popup.btn_weekly)
        if weekly_inactive:
            logger.info("✓ Weekly button is deactivated when daily is active")
        else:
            logger.error("✗ Weekly button is not deactivated when daily is active")

        achievement_inactive = UIButtonUtils.check_sprite_btn_deactive(self.popup.btn_achievement)
        if achievement_inactive:
            logger.info("✓ Achievement button is deactivated when daily is active")
        else:
            logger.error("✗ Achievement button is not deactivated when daily is active")

        # Test daily tab content is available
        daily_tab = self.popup.daily_tab
        assert daily_tab.root.exists(), "Daily tab content not available after clicking daily button!"

        # Test daily tab elements
        title = daily_tab.title
        assert title.strip()=="Daily mission", "Daily tab title not found or incorrect!"
        logger.info(f"✓ Daily tab title: {title}")

        swap_text = daily_tab.swap_text
        assert swap_text.strip() == "Complete daily quests and get rewards", "Daily tab swap text not found or incorrect!"
        logger.info(f"✓ Daily tab swap text: {swap_text}")

        # progress_score = daily_tab.progress_score
        # assert int(progress_score.strip()) in range(0, 6), "Daily tab progress score should be between 0 and 5!"
        # logger.info(f"✓ Daily tab progress score: {progress_score}")
        # assert daily_tab.progress_fill.exists(), "Daily tab progress fill not found!"

        # Test progress rewards
        progress_rewards = daily_tab.progress_rewards
        assert len(progress_rewards) == 3, "Daily tab should have 3 progress rewards!"
        logger.info("✓ Daily tab has 3 progress rewards")

    @pytest.mark.order(4)
    def test_weekly_tab_button_and_content(self):
        """Test weekly button sprite state and weekly tab availability after click"""
        logger = get_logger()
        logger.info("Testing weekly tab button and content...")

        # Click weekly button
        self.popup.btn_weekly.click(sleep_interval=1)

        # Check weekly button is active
        weekly_active = UIButtonUtils.check_sprite_btn_active(self.popup.btn_weekly)
        if weekly_active:
            logger.info("✓ Weekly button is in active state")
        else:
            logger.error("✗ Weekly button is not in active state")

        # Check other buttons are deactivated
        daily_inactive = UIButtonUtils.check_sprite_btn_deactive(self.popup.btn_daily)
        if daily_inactive:
            logger.info("✓ Daily button is deactivated when weekly is active")
        else:
            logger.error("✗ Daily button is not deactivated when weekly is active")

        achievement_inactive = UIButtonUtils.check_sprite_btn_deactive(self.popup.btn_achievement)
        if achievement_inactive:
            logger.info("✓ Achievement button is deactivated when weekly is active")
        else:
            logger.error("✗ Achievement button is not deactivated when weekly is active")

        # Test weekly tab content is available
        weekly_tab = self.popup.weekly_tab
        assert weekly_tab.root.exists(), "Weekly tab content not available after clicking weekly button!"

        # Test weekly tab elements
        title = weekly_tab.title.strip()
        assert title== "Weekly mission", "Weekly tab title not found or incorrect!"
        logger.info(f"✓ Weekly tab title: {title}")

    @pytest.mark.order(5)
    def test_achievement_tab_button_and_content(self):
        """Test achievement button sprite state and achievement tab availability after click"""
        logger = get_logger()
        logger.info("Testing achievement tab button and content...")

        # Click achievement button
        self.popup.btn_achievement.click(sleep_interval=1)

        # Check achievement button is active
        achievement_active = UIButtonUtils.check_sprite_btn_active(self.popup.btn_achievement)
        if achievement_active:
            logger.info("✓ Achievement button is in active state")
        else:
            logger.error("✗ Achievement button is not in active state")

        # Check other buttons are deactivated
        daily_inactive = UIButtonUtils.check_sprite_btn_deactive(self.popup.btn_daily)
        if daily_inactive:
            logger.info("✓ Daily button is deactivated when achievement is active")
        else:
            logger.error("✗ Daily button is not deactivated when achievement is active")

        weekly_inactive = UIButtonUtils.check_sprite_btn_deactive(self.popup.btn_weekly)
        if weekly_inactive:
            logger.info("✓ Weekly button is deactivated when achievement is active")
        else:
            logger.error("✗ Weekly button is not deactivated when achievement is active")

        # Test achievement tab content is available
        achievement_tab = self.popup.achievement_tab
        assert achievement_tab.root.exists(), "Achievement tab content not available after clicking achievement button!"
        logger.info("✓ Achievement tab content is available")

    @pytest.mark.order(6)
    def test_daily_missions_comprehensive(self):
        """Test all daily missions: validation, status checking, and claiming workflow"""
        logger = get_logger()
        logger.info("Starting comprehensive daily missions test...")

        # Click daily button to access daily tab
        self.popup.btn_daily.click(sleep_interval=1)
        daily_missions = self.popup.daily_tab.daily_missions

        # Verify we have 5 missions
        assert len(daily_missions) == 5, f"Expected 5 daily missions, found {len(daily_missions)}"
        logger.info(f"✓ Found {len(daily_missions)} daily missions")

        # Test each mission's elements and collect unclaimed missions
        completed_unclaimed_missions = self._validate_all_daily_mission_elements(daily_missions)

        # Claim any completed but unclaimed missions
        if completed_unclaimed_missions:
            self._claim_completed_missions(completed_unclaimed_missions)

        logger.info("✓ Comprehensive daily missions test completed successfully")

    @pytest.mark.order(7)
    def test_daily_mission_swap_functionality(self):
        """Test the mission swap functionality in daily tab"""
        logger = get_logger()
        logger.info("Testing daily mission swap functionality...")

        # Click daily button to access daily tab
        self.popup.btn_daily.click(sleep_interval=1)
        daily_tab = self.popup.daily_tab
        daily_missions = daily_tab.daily_missions

        # Test clicking btn_swap property in DailyTab (may not be available if 2 swaps used)
        btn_swap = daily_tab.btn_swap
        if btn_swap is None or not btn_swap.exists():
            logger.info("⚠ Daily tab btn_swap is not available - swap limit (2 times) may have been reached")
            logger.info("Skipping swap functionality test as no swaps are available")
            return

        logger.info("✓ Daily tab btn_swap exists and is available")

        # Click the swap button
        btn_swap.click(sleep_interval=1)
        logger.info("✓ Clicked daily tab btn_swap")

        # Verify all missions have swap_BG after clicking btn_swap
        self._verify_missions_have_swap_bg(daily_missions)

        # Check btn_swap exists only for incomplete missions
        incomplete_mission_with_btn = self._verify_mission_swap_buttons(daily_missions)

        # Test swapping an incomplete mission if available
        if incomplete_mission_with_btn:
            self._test_mission_swap_workflow(incomplete_mission_with_btn)
        else:
            logger.info("No incomplete missions with btn_swap found to test swap workflow")

        logger.info("✓ Daily mission swap functionality test completed")

    @pytest.mark.order(8)
    def test_weekly_missions_comprehensive(self):
        """Test all weekly missions: validation and status checking"""
        logger = get_logger()
        logger.info("Starting comprehensive weekly missions test...")

        # Click weekly button to access weekly tab
        self.popup.btn_weekly.click(sleep_interval=2)
        weekly_tab = self.popup.weekly_tab
        weekly_missions = weekly_tab.weekly_missions

        # Verify we have 6 missions
        len_of_weekly_missions = len(weekly_missions)
        assert len_of_weekly_missions == 6, f"Expected 6 weekly missions, found {len_of_weekly_missions}"
        logger.info(f"✓ Found {len_of_weekly_missions} weekly missions")

        # Test each mission
        for i, mission in enumerate(weekly_missions):
            self._validate_single_mission(mission, i+1, "weekly")

        logger.info("✓ Comprehensive weekly missions test completed successfully")

    @pytest.mark.order(9)
    def test_progress_rewards_system(self):
        """Test the complete progress rewards system based on mission completion"""
        logger = get_logger()
        logger.info("Testing progress rewards system...")

        # Click daily button to access daily tab
        self.popup.btn_daily.click(sleep_interval=1)
        daily_tab = self.popup.daily_tab

        # Get current progress score
        progress_score = int(daily_tab.progress_score)
        assert progress_score in range(0, 6), "Progress score should be between 0 and 5!"
        logger.info(f"✓ Current progress score: {progress_score}/5")

        # Count completed missions to verify progress score
        daily_missions = daily_tab.daily_missions
        for i,mission in enumerate(daily_missions):
            assert mission.root.exists(), f"Mission {i+1} root not found!"
        completed_missions = sum(1 for mission in daily_missions if mission.progress_text == "Completed")
        logger.info(f"✓ Completed missions count: {completed_missions}")

        # Verify progress score matches completed missions
        if progress_score == completed_missions:
            logger.info("✓ Progress score matches completed missions count")
        else:
            logger.error(f"✗ Progress score ({progress_score}) doesn't match completed missions ({completed_missions})")

        # Test each progress reward based on milestones [1, 3, 5]
        milestones = [1, 3, 5]
        progress_rewards = daily_tab.progress_rewards
        for i, reward in enumerate(progress_rewards):
            assert reward.root.exists(), f"Mission {i+1} root not found!"
            assert "UI5_Pack_Art_Daily" in reward.box_icon, f"Reward {i+1} box icon texture is incorrect: {reward.box_icon}"

        for i, (reward, milestone) in enumerate(zip(progress_rewards, milestones)):
            logger.info(f"Testing progress reward {i+1} (milestone: {milestone} score)")

            if progress_score >= milestone:
                # Score reached milestone - reward should be available or claimed
                if reward.claimed_icon:
                    logger.info(f"✓ Reward {i+1} is already claimed (milestone {milestone} reached)")
                else:
                    # Reward is available to claim
                    logger.info(f"✓ Reward {i+1} is available to claim (milestone {milestone} reached)")
                    # Try to click and claim the reward
                    try:
                        reward.root.click(sleep_interval=2)

                        # Check if reward popup appeared (should happen for available rewards)
                        reward_popup = self.poco("PopupRewardItem(Clone)")
                        if reward_popup.exists():
                            logger.info(f"✓ Reward popup appeared for reward {i+1}")
                            # Close the reward popup
                            keyevent("BACK")
                            sleep(1)
                            # Refresh progress rewards to get updated UI state
                            progress_rewards = self.popup.daily_tab.progress_rewards
                            reward = progress_rewards[i]  # Get the refreshed reward object

                            # Check if claimed icon now appears
                            if reward.claimed_icon:
                                logger.info(f"✓ Reward {i+1} is now claimed after popup")
                            else:
                                logger.error(f"✗ Reward {i+1} not marked as claimed after popup")
                        else:
                            logger.error(f"✗ No reward popup appeared for available reward {i+1}")

                    except Exception as e:
                        logger.error(f"✗ Error clicking reward {i+1}: {e}")
            else:
                # Score hasn't reached milestone - clicking should show InfoBox
                logger.info(f"Score ({progress_score}) hasn't reached milestone {milestone} for reward {i+1}")

                try:
                    reward.root.click(sleep_interval=0.5)

                    # Check if InfoBox popup appeared
                    info_box = InfoBox(self.poco)
                    if info_box.root.exists():
                        logger.info(f"✓ InfoBox appeared for unavailable reward {i+1}")
                        assert info_box.title != "", "InfoBox title should not be empty!"
                        rewards= info_box.rewards
                        if i==0 or i==1:
                            assert len(rewards) ==3, f"InfoBox should have 3 rewards for unavailable reward {i+1}"
                        else:  # When i==2 (reward 3)
                            assert len(rewards)==4, f"InfoBox should have 4 rewards for unavailable reward {i+1}"
                        # Exit InfoBox using back button
                        keyevent("BACK")
                        sleep(1)

                        # Verify InfoBox is closed
                        if not info_box.root.exists():
                            logger.info("✓ InfoBox closed successfully with back button")
                        else:
                            logger.error("✗ InfoBox not closed after back button")
                    else:
                        logger.error(f"✗ InfoBox didn't appear for unavailable reward {i+1}")

                except Exception as e:
                    logger.error(f"✗ Error testing unavailable reward {i+1}: {e}")

    @pytest.mark.order(10)
    def test_achievement_tab_comprehensive(self):
        """Test all achievement tab elements and missions comprehensively"""
        logger = get_logger()
        logger.info("Starting comprehensive achievement tab test...")

        # Click achievement button to access achievement tab
        self.popup.btn_achievement.click(sleep_interval=2)
        achievement_tab = self.popup.achievement_tab

        # Test achievement tab elements that are always present
        assert achievement_tab.root.exists(), "Achievement tab root not found!"
        assert achievement_tab.title== "Achievement", "Achievement tab title not found or incorrect!"
        assert achievement_tab.description != "", "Achievement tab description not found or empty!"

        # Get achievement missions
        achievement_missions = achievement_tab.achievement_missions

        # Verify we have 6 missions
        assert len(achievement_missions) == 6, f"Expected 6 achievement missions, found {len(achievement_missions)}"
        logger.info(f"✓ Found {len(achievement_missions)} achievement missions")

        # Test each achievement mission
        for i, mission in enumerate(achievement_missions):
            self._validate_achievement_mission(mission, i+1)

        logger.info("✓ Comprehensive achievement tab test completed successfully")

    def _validate_achievement_tab_elements(self, achievement_tab):
        """Validate that all achievement tab elements in __init__ are always present"""
        logger = get_logger()
        logger.info("Testing achievement tab elements presence...")

        # Test root element
        assert achievement_tab.root.exists(), "Achievement tab root not found!"
        logger.info("✓ Achievement tab root element exists")

        # Add additional achievement tab element validations based on the __init__ of AchievementTab class
        # You can add more specific element checks here based on what's defined in the AchievementTab __init__
        logger.info("✓ All achievement tab elements verified")

    def _validate_achievement_mission(self, mission, mission_num):
        """Validate a single achievement mission"""
        logger = get_logger()
        logger.info(f"Testing achievement mission {mission_num}...")

        # Use the existing shared method to validate basic mission elements
        self._validate_mission_basic_elements(mission, mission_num, "achievement")

        # Get mission details
        mission_name = mission.name
        progress_text = mission.progress_text
        background = mission.background

        logger.info(f"✓ Achievement mission {mission_num} - Name: {mission_name}, Progress: {progress_text}, Background: {background}")

        # Check mission status and validate accordingly
        if progress_text == "Completed":
            self._validate_completed_claimed_achievement_mission(mission, mission_num)
        elif "/" in progress_text:
            self._validate_achievement_mission_with_progress(mission, mission_num, progress_text, background)

    def _validate_completed_claimed_achievement_mission(self, mission, mission_num):
        """Validate a completed and claimed achievement mission"""
        logger = get_logger()
        logger.info(f"✓ Achievement mission {mission_num} is completed and rewards already claimed")

        # For completed achievement missions, achievement_reward should not exist
        achievement_reward = mission.achievement_reward
        assert achievement_reward is None, f"Achievement mission {mission_num} should not have achievement_reward when completed and claimed!"

        # Background should be UI5_Target_BG_3 for completed missions
        background = mission.background
        assert "UI5_Target_BG_3" in background, f"Achievement mission {mission_num} background should be UI5_Target_BG_3, got: {background}"
        logger.info(f"✓ Achievement mission {mission_num} has correct completed-claimed state")

    def _validate_achievement_mission_with_progress(self, mission, mission_num, progress_text, background):
        """Validate an achievement mission with progress (incomplete or completed but unclaimed)"""
        logger = get_logger()

        try:
            # Remove commas from the progress text before parsing
            clean_progress_text = progress_text.replace(",", "")
            current, total = map(int, clean_progress_text.split("/"))

            if current < total:
                # Mission incomplete
                logger.info(f"✓ Achievement mission {mission_num} is incomplete ({current}/{total})")
                self._validate_incomplete_achievement_mission(mission, mission_num, background)

            elif current >= total:
                # Mission completed but reward not claimed yet
                logger.info(f"✓ Achievement mission {mission_num} is completed but not claimed ({current}/{total})")
                self._validate_completed_unclaimed_achievement_mission(mission, mission_num, background)

        except ValueError:
            logger.error(f"✗ Achievement mission {mission_num} has invalid progress format: {progress_text}")
            assert False, f"Achievement mission {mission_num} progress text format is invalid: {progress_text}"

    def _validate_incomplete_achievement_mission(self, mission, mission_num, background):
        """Validate an incomplete achievement mission's reward and background"""
        logger = get_logger()

        # Achievement missions should have exactly 1 achievement_reward
        achievement_reward = mission.achievement_reward
        assert achievement_reward is not None, f"Achievement mission {mission_num} should have an achievement_reward when incomplete!"

        # Check the achievement reward elements
        reward_icon = achievement_reward.reward_icon
        reward_amount = achievement_reward.reward_amount
        assert reward_icon is not None, f"Achievement mission {mission_num} achievement_reward icon not found!"
        assert reward_amount is not None, f"Achievement mission {mission_num} achievement_reward amount not found!"
        logger.info(f"✓ Achievement mission {mission_num} achievement_reward - Icon: {reward_icon}, Amount: {reward_amount}")

        # Background should be UI5_Target_BG_1 for incomplete missions
        assert "UI5_Target_BG_1" in background, f"Achievement mission {mission_num} background should be UI5_Target_BG_1, got: {background}"
        logger.info(f"✓ Achievement mission {mission_num} has correct incomplete state")

    def _validate_completed_unclaimed_achievement_mission(self, mission, mission_num, background):
        """Validate a completed but unclaimed achievement mission's reward and background"""
        logger = get_logger()

        # Achievement missions should have exactly 1 achievement_reward when completed but unclaimed
        achievement_reward = mission.achievement_reward
        assert achievement_reward is not None, f"Achievement mission {mission_num} should have an achievement_reward when completed but not claimed!"

        # Check the achievement reward elements
        reward_icon = achievement_reward.reward_icon
        reward_amount = achievement_reward.reward_amount
        assert reward_icon is not None, f"Achievement mission {mission_num} achievement_reward icon not found!"
        assert reward_amount is not None, f"Achievement mission {mission_num} achievement_reward amount not found!"
        logger.info(f"✓ Achievement mission {mission_num} achievement_reward - Icon: {reward_icon}, Amount: {reward_amount}")

        # Background should be UI5_Target_BG_2 for completed but unclaimed missions
        assert "UI5_Target_BG_2" in background, f"Achievement mission {mission_num} background should be UI5_Target_BG_2, got: {background}"
        logger.info(f"✓ Achievement mission {mission_num} has correct completed-unclaimed state")

    # ==== SHARED MISSION VALIDATION METHODS ====

    def _validate_single_mission(self, mission, mission_num, mission_type="daily"):
        """Validate a single mission (daily or weekly) based on its properties"""
        logger = get_logger()
        logger.info(f"Testing {mission_type} mission {mission_num}...")

        # Check that mission root exists
        assert mission.root.exists(), f"{mission_type.title()} mission {mission_num} root not found!"

        if mission_type == "weekly":
            # Weekly missions need to check open_in_msg first
            open_in_msg = mission.open_in_msg
            if open_in_msg is None:
                # Mission is fully accessible - check all elements like daily missions
                logger.info(f"✓ Weekly mission {mission_num} is fully accessible")
                self._validate_accessible_mission(mission, mission_num, mission_type)
            else:
                # Mission is locked with open_in_msg - validate the message format
                logger.info(f"✓ Weekly mission {mission_num} is locked with open message")
                self._validate_locked_mission(mission, mission_num, open_in_msg)
        else:
            # Daily missions are always accessible
            self._validate_accessible_mission(mission, mission_num, mission_type)

    def _validate_accessible_mission(self, mission, mission_num, mission_type):
        """Validate a mission that is fully accessible (daily or unlocked weekly)"""
        logger = get_logger()

        # Test basic mission elements
        self._validate_mission_basic_elements(mission, mission_num, mission_type)

        # Get mission details
        mission_name = mission.name
        progress_text = mission.progress_text
        background = mission.background

        logger.info(f"✓ {mission_type.title()} mission {mission_num} - Name: {mission_name}, Progress: {progress_text}, Background: {background}")

        # Check mission status based on progress_text
        if progress_text == "Completed":
            self._validate_completed_claimed_mission(mission, mission_num, mission_type)
        elif "/" in progress_text:
            self._validate_progress_mission(mission, mission_num, mission_name, progress_text, background, mission_type)

    def _validate_locked_mission(self, mission, mission_num, open_in_msg):
        """Validate a weekly mission that is locked with open_in_msg"""
        logger = get_logger()

        # Validate open_in_msg format: "Open in 03:19:41:10"
        import re
        pattern = r"^Open in \d{2}:\d{2}:\d{2}:\d{2}$"
        assert re.match(pattern, open_in_msg), f"Weekly mission {mission_num} open_in_msg format is invalid: '{open_in_msg}'. Expected format: 'Open in XX:XX:XX:XX'"

        logger.info(f"✓ Weekly mission {mission_num} has valid open_in_msg format: {open_in_msg}")

        # For locked missions, name should be None (since mission is not accessible yet)
        mission_name = mission.name
        if mission_name is None:
            logger.info(f"✓ Weekly mission {mission_num} correctly has no name (locked mission)")
        else:
            logger.info(f"⚠ Weekly mission {mission_num} has name '{mission_name}' despite being locked")

    def _validate_mission_basic_elements(self, mission, mission_num, mission_type="daily"):
        """Validate that all basic mission elements exist"""
        assert mission.root.exists(), f"{mission_type.title()} mission {mission_num} root not found!"
        assert mission.name is not None, f"{mission_type.title()} mission {mission_num} name not found!"
        assert mission.icon.exists(), f"{mission_type.title()} mission {mission_num} icon not found!"
        assert mission.progress_bar.exists(), f"{mission_type.title()} mission {mission_num} progress bar not found!"
        assert mission.progress_text is not None, f"{mission_type.title()} mission {mission_num} progress text not found!"

    def _validate_completed_claimed_mission(self, mission, mission_num, mission_type="daily"):
        """Validate a mission that is completed and rewards already claimed"""
        logger = get_logger()
        logger.info(f"✓ {mission_type.title()} mission {mission_num} is completed and rewards already claimed")

        # Rewards should not exist
        rewards = mission.rewards
        non_existing_rewards = [r for r in rewards if r is not None]
        assert len(non_existing_rewards) == 0, f"{mission_type.title()} mission {mission_num} should not have rewards when completed and claimed!"

        # Background should be UI5_Target_BG_3
        background = mission.background
        assert "UI5_Target_BG_3" in background, f"{mission_type.title()} mission {mission_num} background should be UI5_Target_BG_3, got: {background}"
        logger.info(f"✓ {mission_type.title()} mission {mission_num} has correct completed-claimed state")

    def _validate_progress_mission(self, mission, mission_num, mission_name, progress_text, background, mission_type="daily"):
        """Validate a mission with progress and return if it's completed but unclaimed"""
        logger = get_logger()

        try:
            # Remove commas from the progress text before parsing
            clean_progress_text = progress_text.replace(",", "")
            current, total = map(int, clean_progress_text.split("/"))

            if current < total:
                # Mission incomplete
                logger.info(f"✓ {mission_type.title()} mission {mission_num} is incomplete ({current}/{total})")
                self._validate_incomplete_mission(mission, mission_num, background, mission_type)
                return None

            elif current >= total:
                # Mission completed but reward not claimed yet
                logger.info(f"✓ {mission_type.title()} mission {mission_num} is completed but not claimed ({current}/{total})")
                self._validate_completed_unclaimed_mission(mission, mission_num, background, mission_type)

                # Return mission info for claiming later (only for daily missions)
                if mission_type == "daily":
                    logger.info(f"✓ {mission_type.title()} mission {mission_num} marked for claiming later")
                    return (mission_num-1, mission_name)  # Return 0-based index and name
                return None

        except ValueError:
            logger.error(f"✗ {mission_type.title()} mission {mission_num} has invalid progress format: {progress_text}")
            assert False, f"{mission_type.title()} mission {mission_num} progress text format is invalid: {progress_text}"

        return None

    def _validate_incomplete_mission(self, mission, mission_num, background, mission_type="daily"):
        """Validate an incomplete mission's rewards and background"""
        logger = get_logger()

        # Should have rewards
        rewards = mission.rewards
        existing_rewards = [r for r in rewards if r is not None]
        assert len(existing_rewards) == 3, f"{mission_type.title()} mission {mission_num} should have 3 rewards when incomplete!"

        # Check all reward elements
        for j, reward in enumerate(existing_rewards):
            reward_icon= reward.reward_icon
            reward_amount = reward.reward_amount
            assert reward_icon is not None, f"{mission_type.title()} mission {mission_num} reward {j+1} icon not found!"
            assert reward_amount is not None, f"{mission_type.title()} mission {mission_num} reward {j+1} amount not found!"
            logger.info(f"✓ {mission_type.title()} mission {mission_num} reward {j+1} - Icon: {reward_icon}, Amount: {reward_amount}")

        # Background should be UI5_Target_BG_1
        assert "UI5_Target_BG_1" in background, f"{mission_type.title()} mission {mission_num} background should be UI5_Target_BG_1, got: {background}"
        logger.info(f"✓ {mission_type.title()} mission {mission_num} has correct incomplete state")

    def _validate_completed_unclaimed_mission(self, mission, mission_num, background, mission_type="daily"):
        """Validate a completed but unclaimed mission's rewards and background"""
        logger = get_logger()

        # Should have rewards
        rewards = mission.rewards
        existing_rewards = [r for r in rewards if r is not None]
        assert len(existing_rewards) == 3, f"{mission_type.title()} mission {mission_num} should have 3 rewards when completed but not claimed!"

        # Check all reward elements
        for j, reward in enumerate(existing_rewards):
            reward_icon= reward.reward_icon
            reward_amount = reward.reward_amount
            assert reward_icon is not None, f"{mission_type.title()} mission {mission_num} reward {j+1} icon not found!"
            assert reward_amount is not None, f"{mission_type.title()} mission {mission_num} reward {j+1} amount not found!"
            logger.info(f"✓ {mission_type.title()} mission {mission_num} reward {j+1} - Icon: {reward_icon}, Amount: {reward_amount}")

        # Background should be UI5_Target_BG_2
        assert "UI5_Target_BG_2" in background, f"{mission_type.title()} mission {mission_num} background should be UI5_Target_BG_2, got: {background}"
        logger.info(f"✓ {mission_type.title()} mission {mission_num} has correct completed-unclaimed state")

    # ==== DAILY-SPECIFIC METHODS ====

    def _validate_all_daily_mission_elements(self, daily_missions):
        """Validate all daily mission elements and return list of completed but unclaimed missions"""
        logger = get_logger()
        completed_unclaimed_missions = []

        # Test each mission
        for i, mission in enumerate(daily_missions):
            logger.info(f"Testing daily mission {i+1}...")

            # Validate basic mission elements
            self._validate_mission_basic_elements(mission, i+1, "daily")

            # Get mission details
            mission_name = mission.name
            progress_text = mission.progress_text
            background = mission.background

            logger.info(f"✓ Daily mission {i+1} - Name: {mission_name}, Progress: {progress_text}, Background: {background}")

            # Check mission status and validate accordingly
            if progress_text == "Completed":
                self._validate_completed_claimed_mission(mission, i+1, "daily")
            elif "/" in progress_text:
                unclaimed_mission = self._validate_progress_mission(mission, i+1, mission_name, progress_text, background, "daily")
                if unclaimed_mission:
                    completed_unclaimed_missions.append(unclaimed_mission)

        return completed_unclaimed_missions

    # ...existing code for claiming missions, swap functionality, etc...

    def _claim_completed_missions(self, completed_unclaimed_missions):
        """Claim all completed but unclaimed missions"""
        logger = get_logger()
        logger.info(f"Found {len(completed_unclaimed_missions)} missions to claim")

        # Get current battle pass level for comparison
        current_bp_level = self.popup.battle_pass_panel.level
        logger.info(f"Current battle pass level: {current_bp_level}")

        for mission_index, mission_name in completed_unclaimed_missions:
            self._claim_single_mission(mission_name)

    def _claim_single_mission(self, mission_name):
        """Claim a single mission and verify the results"""
        logger = get_logger()
        logger.info(f"Claiming mission: {mission_name}")

        # Get progress score before claiming
        progress_score_before = int(self.popup.daily_tab.progress_score)
        logger.info(f"Progress score before claiming mission: {progress_score_before}")

        # Find and click the mission
        target_mission = self._find_mission_by_name(mission_name)
        target_mission.root.click(sleep_interval=1)

        # Handle popup rewards and tier up
        self._handle_mission_claim_popups()

        # Verify progress score increased
        self._verify_progress_score_increase(progress_score_before)

        # Verify mission is now properly claimed
        self._verify_mission_claimed(mission_name)

    def _find_mission_by_name(self, mission_name):
        """Find a mission by its name"""
        daily_missions = self.popup.daily_tab.daily_missions
        for mission in daily_missions:
            if mission.name == mission_name:
                return mission

        assert False, f"Could not find mission with name: {mission_name}"

    def _handle_mission_claim_popups(self):
        """Handle popup reward and tier up popup that may appear after mission claim"""
        logger = get_logger()

        # Check for popup reward
        popup_reward = self.poco("PopupRewardItem(Clone)")
        if popup_reward.exists():
            logger.info("✓ Popup reward appeared")
            keyevent("BACK")
            sleep(1)
            logger.info("✓ Popup reward closed with back button")

        # Check for TierUpPopup
        tier_up_popup = TierUpPopup(self.poco)
        if tier_up_popup.root.exists():
            logger.info("✓ TierUpPopup appeared")
            self._validate_tier_up_popup(tier_up_popup)

    def _validate_tier_up_popup(self, tier_up_popup):
        """Validate TierUpPopup elements and level matching"""
        logger = get_logger()

        # Check TierUpPopup elements
        assert tier_up_popup.level is not None, "TierUpPopup level not found!"
        assert tier_up_popup.btn_go_to_BP.exists(), "TierUpPopup go to BP button not found!"
        assert tier_up_popup.btn_close.exists(), "TierUpPopup close button not found!"

        # Get refreshed battle pass level for comparison
        refreshed_bp_level = self.popup.battle_pass_panel.level
        tier_up_level = tier_up_popup.level
        logger.info(f"TierUpPopup level: {tier_up_level}, Refreshed BP level: {refreshed_bp_level}")

        # Compare levels using if statement and log error if not matching
        if tier_up_level == refreshed_bp_level:
            logger.info("✓ TierUpPopup level matches refreshed battle pass level")
        else:
            logger.error(f"✗ TierUpPopup level ({tier_up_level}) doesn't match refreshed battle pass level ({refreshed_bp_level})")

        logger.info("✓ TierUpPopup elements verified")

        # Exit TierUpPopup with device back button
        keyevent("BACK")
        sleep(1)
        logger.info("✓ TierUpPopup closed with back button")

    def _verify_progress_score_increase(self, progress_score_before):
        """Verify that progress score increased by 1 after mission claim"""
        logger = get_logger()

        progress_score_after = int(self.popup.daily_tab.progress_score)
        logger.info(f"Progress score after claiming mission: {progress_score_after}")

        expected_score = progress_score_before + 1
        if progress_score_after == expected_score:
            logger.info(f"✓ Progress score correctly increased from {progress_score_before} to {progress_score_after}")
        else:
            logger.error(f"✗ Progress score should be {expected_score} but is {progress_score_after}")

    def _verify_mission_claimed(self, mission_name):
        """Verify that a mission is now properly claimed"""
        logger = get_logger()

        # Find the claimed mission
        daily_missions = self.popup.daily_tab.daily_missions
        claimed_mission = None
        for mission in daily_missions:
            if mission.name == mission_name:
                claimed_mission = mission
                break

        if claimed_mission:
            assert claimed_mission.progress_text == "Completed", f"Mission {mission_name} should be marked as Completed after claiming!"
            assert "UI5_Target_BG_3" in claimed_mission.background, f"Mission {mission_name} should have UI5_Target_BG_3 background after claiming!"

            # Rewards should not exist
            rewards = claimed_mission.rewards
            non_existing_rewards = [r for r in rewards if r is not None]
            assert len(non_existing_rewards) == 0, f"Mission {mission_name} should not have rewards after claiming!"

            logger.info(f"✓ Mission {mission_name} is now properly claimed")

    def _verify_missions_have_swap_bg(self, daily_missions):
        """Verify all missions have swap_BG after clicking btn_swap"""
        logger = get_logger()

        for i, mission in enumerate(daily_missions):
            swap_bg = mission.swap_BG
            assert swap_bg is not None and swap_bg.exists(), f"Mission {i+1} should have swap_BG after clicking btn_swap!"
            logger.info(f"✓ Mission {i+1} has swap_BG")

    def _verify_mission_swap_buttons(self, daily_missions):
        """Verify btn_swap exists only for incomplete missions and return one for testing"""
        logger = get_logger()
        incomplete_mission_with_btn = None

        for i, mission in enumerate(daily_missions):
            progress_text = mission.progress_text
            btn_swap = mission.btn_swap

            if progress_text == "Completed":
                # Completed missions should not have btn_swap
                if btn_swap is not None:
                    logger.error(f"✗ Mission {i+1} is completed but still has btn_swap!")
                else:
                    logger.info(f"✓ Mission {i+1} (completed) correctly has no btn_swap")

            elif "/" in progress_text:
                # Check if mission is incomplete
                try:
                    clean_progress_text = progress_text.replace(",", "")
                    current, total = map(int, clean_progress_text.split("/"))

                    if current < total:
                        # Incomplete mission may or may not have btn_swap (depends on swap limit)
                        if btn_swap is not None and btn_swap.exists():
                            logger.info(f"✓ Mission {i+1} (incomplete) has btn_swap available")

                            # Store one incomplete mission for testing swap workflow
                            if incomplete_mission_with_btn is None:
                                incomplete_mission_with_btn = (i+1, mission)
                        else:
                            logger.info(f"⚠ Mission {i+1} (incomplete) has no btn_swap - may have reached swap limit")

                    else:
                        # Completed but unclaimed missions should not have btn_swap
                        if btn_swap is not None:
                            logger.error(f"✗ Mission {i+1} is completed but unclaimed and should not have btn_swap!")
                        else:
                            logger.info(f"✓ Mission {i+1} (completed but unclaimed) correctly has no btn_swap")

                except ValueError:
                    logger.error(f"✗ Mission {i+1} has invalid progress format: {progress_text}")

        return incomplete_mission_with_btn

    def _test_mission_swap_workflow(self, incomplete_mission_info):
        """Test the complete mission swap workflow with popup notice"""
        logger = get_logger()
        mission_num, mission = incomplete_mission_info

        logger.info(f"Testing swap workflow for mission {mission_num}")

        # Verify btn_swap is still available before testing
        if mission.btn_swap is None or not mission.btn_swap.exists():
            logger.info(f"⚠ Mission {mission_num} btn_swap is no longer available - swap limit may have been reached")
            return

        # Get original mission name
        original_mission_name = mission.name
        logger.info(f"Original mission name: {original_mission_name}")

        # Click btn_swap on the incomplete mission
        mission.btn_swap.click(sleep_interval=1)
        logger.info(f"✓ Clicked btn_swap on mission {mission_num}")

        # Check popup notice appears
        popup_notice = self.poco("PopupNotice(Clone)")
        assert popup_notice.exists(), "PopupNotice should appear after clicking btn_swap!"
        logger.info("✓ PopupNotice appeared")

        # Check popup notice has both buttons
        close_btn = popup_notice.offspring("bClose")
        confirm_btn = popup_notice.offspring("bOK")

        assert close_btn.exists(), "PopupNotice should have close button (bClose)!"
        assert confirm_btn.exists(), "PopupNotice should have confirm button (bOK)!"
        logger.info("✓ PopupNotice has both close and confirm buttons")

        # First test: Click close button and verify mission name remains the same
        close_btn.click(sleep_interval=1.5)
        logger.info("✓ Clicked close button")

        # Verify popup is closed
        assert not popup_notice.exists(), "PopupNotice should be closed after clicking close button!"
        logger.info("✓ PopupNotice closed after clicking close button")

        # Refresh mission list and verify name remains the same
        daily_missions = self.popup.daily_tab.daily_missions
        current_mission = daily_missions[mission_num-1]  # Convert back to 0-based index
        current_mission_name = current_mission.name

        assert current_mission_name == original_mission_name, f"Mission name should remain '{original_mission_name}' after clicking close, but got '{current_mission_name}'"
        logger.info(f"✓ Mission name remained the same after clicking close: {current_mission_name}")

        # Check if btn_swap is still available for second test
        if current_mission.btn_swap is None or not current_mission.btn_swap.exists():
            logger.info(f"⚠ Mission {mission_num} btn_swap is no longer available after first use - this may be expected behavior")
            return

        # Second test: Click btn_swap again and confirm the swap
        current_mission.btn_swap.click(sleep_interval=1)
        logger.info(f"✓ Clicked btn_swap again on mission {mission_num}")

        # Check popup notice appears again
        popup_notice = self.poco("PopupNotice(Clone)")
        assert popup_notice.exists(), "PopupNotice should appear again after clicking btn_swap!"
        logger.info("✓ PopupNotice appeared again")

        # Click confirm button
        # confirm_btn = popup_notice.offspring("bOK")
        confirm_btn.click(sleep_interval=1)
        logger.info("✓ Clicked confirm button")

        # Verify popup is closed
        assert not popup_notice.exists(), "PopupNotice should be closed after clicking confirm button!"
        logger.info("✓ PopupNotice closed after clicking confirm button")

        # Refresh mission list and verify mission is replaced
        daily_missions = self.popup.daily_tab.daily_missions
        swapped_mission = daily_missions[mission_num-1]  # Convert back to 0-based index
        swapped_mission_name = swapped_mission.name

        assert swapped_mission_name != original_mission_name, f"Mission should be replaced after clicking confirm, but name is still '{swapped_mission_name}'"
        logger.info(f"✓ Mission was successfully swapped from '{original_mission_name}' to '{swapped_mission_name}'")

        # Check if btn_swap is still available after second use
        final_btn_swap = swapped_mission.btn_swap
        if final_btn_swap is None or not final_btn_swap.exists():
            logger.info(f"✓ Mission {mission_num} btn_swap is no longer available after second use - swap limit reached")
        else:
            logger.info(f"✓ Mission {mission_num} btn_swap is still available after second use")
