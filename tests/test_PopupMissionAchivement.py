from airtest.core.api import keyevent

from Hierarchy.PopupMissionAchivement import *
import pytest
from logger_config import get_logger

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

@pytest.mark.use_to_home(before=False, after=True, logger_name="PopupMission", back_button="PopupMissionAchivement_back_btn")
class TestPopupMissionAchivement:
    @pytest.fixture(scope="function", autouse=True)
    def setup(self,poco):
        self.poco = poco
        home_icon= poco("SubFeatureTopLayer").offspring("Quest_Home")
        home_icon.click(sleep_interval=1)
        self.popup = PopupMissionAchivement(poco)
        assert self.popup.root.exists(), "PopupMissionAchivement not found!"

    def test_abc(self,poco):
        lvBef=self.popup.battle_pass_panel.level
        progressBef=self.popup.battle_pass_panel.progress_text
        print(f"Battle Pass Level before: {lvBef}, Progress: {progressBef}")
        item=poco("Grid").child("HBP_UI_Mission_Item(Clone)")[0].offspring("lName")
        item.click(sleep_interval=2)
        reward_popup= poco("PopupRewardItem(Clone)")
        assert reward_popup.exists(), "Reward popup did not appear!"
        keyevent("BACK")
        lvAft=self.popup.battle_pass_panel.level
        progressAft=self.popup.battle_pass_panel.progress_text
        print(f"Battle Pass Level after: {lvAft}, Progress: {progressAft}")