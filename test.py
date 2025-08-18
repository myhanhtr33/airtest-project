from Hierarchy.PopupCampaignSelectLv import PopupCampaignSelectLv, PanelWorlds
from Hierarchy.PopupLevelPrepare import PopupLevelPrepare
from Hierarchy.UI_ingame import *
import pytest
from logger_config import get_logger
from utils.helper_functions import wait_for_element
from utils.test_level_helper import *
from airtest.core.api import swipe, sleep
class test_1234:
    def test_1111(self, poco):
        logger = get_logger("test_1234")
        logger.info("Starting test_1111...")

        # Initialize PopupCampaignSelectLv
        popup_campaign_select_lv = PopupCampaignSelectLv(poco)
        assert popup_campaign_select_lv.root.exists(), "PopupCampaignSelectLv root not found!"

        # Click on a specific world (e.g., "World 1")
        world = popup_campaign_select_lv.worlds[0]

