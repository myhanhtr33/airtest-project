import pytest
from Hierarchy.PopupMilitary import *
from utils.device_setup import PocoManager
from airtest.core.api import *
from logger_config import get_logger

@pytest.fixture
def military_back_button(poco):
    return poco("PopupMilitaryCareer(Clone)").offspring("B_Back (1)")
@pytest.mark.use_to_home(before=True, logger_name="PopupMilitary", back_button=military_back_button)
class TestPopupMilitary:
    @pytest.fixture(autouse=True)
    def setup(self,poco):
        self.popup=PopupMilitary(poco)
        self.poco=poco
        self.home_notice = poco("SubFeatureTopLayer").offspring("sNotice") if poco("SubFeatureTopLayer").offspring(
            "sNotice").exists() else None
        self.navigate_to_military()
        self.weapon_point_notices=[]
    def navigate_to_military(self):
        if self.popup.root.exists():
            return
        military_home_icon=self.poco("SubFeatureTopLayer").offspring("Military_Home")
        assert military_home_icon.exists(), "Military home icon not found"
        military_home_icon.click(sleep_interval=1)
        assert self.popup.root.exists(), "Military popup did not open"
        self.popup= PopupMilitary(self.poco)
    def test_element_presence(self):
        logger=get_logger()
        assert self.popup.btn_back.exists(), "Back button not found"
        assert self.popup.top_panel.exists(), "Top panel not found"
        assert self.popup.title.strip() == "Military Career", "Title text mismatch"
        assert self.popup.rank_badge.exists(), "Rank badge not found"
        assert self.popup.info_btn.exists(), "Info button not found"
        assert self.popup.mid_panel.exists(), "Mid panel not found"
        assert self.popup.mid_title.strip() == "All squads get", "Mid title text mismatch"
        assert len(self.popup.passives) == 6, "Expected 6 passives, found {}".format(len(self.popup.passives))
        for i, passive in enumerate(self.popup.passives):
            assert passive.root.exists(), f"Passive {i} not found"
            assert passive.sprite.exists(), f"Passive {i} sprite not found"
            assert passive.passive_stat_text.strip() != "", f"Passive {i} stat text is empty"
        assert self.popup.bot_panel.exists(), "Bottom panel not found"
        assert self.popup.process_fill.exists(), "Process fill not found"
        assert self.popup.process_info_btn.exists(), "Process info button not found"
        assert self.popup.upgrade_btn.exists(), "Upgrade button not found"
        assert len(self.popup.weapon_points) == 5, "Expected 5 weapon points, found {}".format(len(self.popup.weapon_points))
        for i, weapon_point in enumerate(self.popup.weapon_points):
            assert weapon_point.root.exists(), f"Weapon point {i} not found"
            assert weapon_point.icon.exists(), f"Weapon point {i} icon not found"
            assert weapon_point.name.strip() != "", f"Weapon point {i} name is empty"
            assert weapon_point.accumulated_point.strip() != "", f"Weapon point {i} accumulated point is empty"
            if weapon_point.notice:
                self.weapon_point_notices.append(True)
            else:
                self.weapon_point_notices.append(False)
        assert self.popup.level_number_text.strip() != "", "Level number text is empty"
        assert self.popup.level_category_text.strip() != "", "Level category text is empty"
        assert self.popup.process_text.strip() != "", "Process text is empty"
        assert self.popup.upgrade_price_text.strip() != "", "Upgrade price text is empty"
        logger.info("All elements are present and verified successfully.")
        print("All elements are present and verified successfully.")




