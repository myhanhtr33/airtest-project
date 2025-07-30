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

    def test_mission_item_details(self):
        """Test detailed properties of mission items"""
        logger = get_logger()
        logger.info("Testing mission item details...")

        # Test daily missions
        self.popup.btn_daily.click(sleep_interval=1)
        daily_missions = self.popup.daily_tab.daily_missions

        if daily_missions:
            first_mission = daily_missions[0]

            # Test mission properties
            mission_name = first_mission.name
            progress_text = first_mission.progress_text
            background = first_mission.background

            logger.info(f"✓ First daily mission - Name: {mission_name}, Progress: {progress_text}, Background: {background}")

            # Test mission rewards if available
            rewards = first_mission.rewards()
            if rewards:
                logger.info(f"✓ First daily mission has {len(rewards)} rewards")

            # Test open in message if available
            open_msg = first_mission.open_in_msg
            if open_msg:
                logger.info(f"✓ Mission has open message: {open_msg}")

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
                            progress_rewards = daily_tab.progress_rewards
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

    def test_progress_rewards_details(self):
        """Test progress rewards in daily tab"""
        logger = get_logger()
        logger.info("Testing progress rewards details...")

        self.popup.btn_daily.click(sleep_interval=1)
        progress_rewards = self.popup.daily_tab.progress_rewards

        for i, reward in enumerate(progress_rewards):
            box_icon = reward.box_icon
            claimed_icon = reward.claimed_icon

            logger.info(f"✓ Progress reward {i+1} - Box icon: {box_icon}, Claimed: {claimed_icon is not None}")
