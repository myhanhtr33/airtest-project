import time

import pytest
from Hierarchy.PopupMilitary import *
from utils.device_setup import PocoManager
from airtest.core.api import *
from logger_config import get_logger
from utils.helper_functions import check_noti
from utils.get_resource_amount import get_single_resource_amount

len_of_weapon={
    "Aircraft": 24,
    "Drone": 24,
    "Wing":24,
    "Pilot": 20,
    "Engine":18
}

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
            assert passive.passive_stat_text != "", f"Passive {i} stat text is empty"
            assert passive.passive_stat_text.endswith("%"), f"Passive {i} stat text does not end with '%': {passive.passive_stat_text}"
        assert self.popup.bot_panel.exists(), "Bottom panel not found"
        assert self.popup.progress_fill.exists(), "Process fill not found"
        assert self.popup.progress_info_btn.exists(), "Process info button not found"
        assert self.popup.upgrade_btn.exists(), "Upgrade button not found"
        assert len(self.popup.weapon_points) == 5, "Expected 5 weapon points, found {}".format(len(self.popup.weapon_points))
        for i, weapon_point in enumerate(self.popup.weapon_points):
            assert weapon_point.root.exists(), f"Weapon point {i} not found"
            assert weapon_point.icon.exists(), f"Weapon point {i} icon not found"
            assert weapon_point.name.strip() != "", f"Weapon point {i} name is empty"
            assert int(weapon_point.accumulated_point) >=0, f"Weapon point {i} accumulated point is empty"
            if weapon_point.notice:
                self.weapon_point_notices.append(True)
            else:
                self.weapon_point_notices.append(False)
        assert self.popup.level_number_text.strip() != "", "Level number text is empty"
        assert self.popup.level_category_text.strip() != "", "Level category text is empty"
        assert self.popup.progress_text.strip() != "", "Process text is empty"
        assert self.popup.upgrade_price_text.strip() != "", "Upgrade price text is empty"
        logger.info("All elements are present and verified successfully.")
    def test_valid_rank_category(self):
        logger=get_logger()
        actual_rank=self.popup.level_category_text
        assert actual_rank in rank_category, f"Invalid rank category: {actual_rank}"
        logger.info(f"rank category '{actual_rank}' is valid.")
    def test_click_info_button(self):
        logger=get_logger()
        self.popup.info_btn.click(sleep_interval=1)
        popup_info= PopupMilitaryCareerInfo(self.poco)
        assert popup_info.root.exists(), "Popup Military Career Info did not open"
        popup_info.btn_back.click(sleep_interval=1)
        assert not popup_info.root.exists(), "Popup Military Career Info did not close"
        logger.info("Info button functionality verified successfully.")
    def test_passive_sprite(self):
        logger=get_logger()
        actual_sprites=[
            passive.sprite.attr("texture").strip()
            for passive in self.popup.passives
        ]
        for i, actual_sprite in enumerate(actual_sprites):
            assert actual_sprite == expected_passive_sprites[i], f"Passive {i} sprite mismatch: {actual_sprite} != {expected_passive_sprites[i]}"
        logger.info("Passive sprite functionality verified successfully.")
    def test_passive_stat(self):
        logger=get_logger()
        actual_stats=[
            passive.passive_stat_text.rstrip("%")
            for passive in self.popup.passives
        ]
        actual_stats=[float(stat) for stat in actual_stats]
        actual_lv=self.popup.get_actual_level()
        expected_stats= self.popup.get_expected_stats_by_lv(actual_lv)
        assert actual_stats == expected_stats, f"Stats mismatch - Actual: {actual_stats}, Expected: {expected_stats}"
        logger.info("Passive stats  verified successfully.")
    def test_click_progress_info_button(self):
        logger=get_logger()
        self.popup.progress_info_btn.click(sleep_interval=1.5)
        panel=self.poco("PanelTooltipInfo").offspring("lDes")
        panel_text=panel.get_text().strip()
        assert panel_text=="Career Point", "Progress info button did not show correct text"
        self.popup.progress_info_btn.click(sleep_interval=1.5)
        panel=self.poco("PanelTooltipInfo").offspring("lDes")
        assert not panel.exists(), "Panel did not close after clicking again"
    def test_valid_progress_point_and_price(self):
        logger=get_logger()
        actual_current_point,actual_required_point= self.popup.get_progress_points()
        assert actual_current_point >= 0, f"Current point is negative: {actual_current_point}"
        expected_required_point= PopupMilitary.get_expected_required_point(self.popup.get_actual_level()+1)
        assert actual_required_point == expected_required_point, f"Required point mismatch: {actual_required_point} != {expected_required_point}"
        actual_price=int(self.popup.upgrade_price_text.replace(",",""))
        assert actual_price==PopupMilitary.get_expected_upgrade_price(self.popup.get_actual_level()+1), f"Upgrade price mismatch: {actual_price} != {PopupMilitary.get_expected_upgrade_price(self.popup.get_actual_level()+1)}"
        logger.info(f"Progress points and upgrade price verified successfully: Current Point: {actual_current_point}, Required Point: {actual_required_point}, Upgrade Price: {actual_price}")
    def test_deactive_upgrade_btn(self):
        logger=get_logger()
        current_point,required_point= self.popup.get_progress_points()
        upgrade_price=self.popup.upgrade_price_text
        initial_values = (current_point, required_point, upgrade_price)
        if current_point>required_point:
            logger.info("active upgrade button")
            return
        assert not self.popup.upgrade_btn_notice, "Upgrade button notice should not be active"
        assert self.popup.upgrade_btn_sprite=="UI5_Bottom_btn_9sl_Grey", f"Upgrade button sprite should be greyed out, found {self.popup.upgrade_btn_sprite}"
        self.popup.upgrade_btn.click()
        check_noti(self.poco,"Not enough currency")
        #verify state after click
        assert not self.popup.upgrade_btn_notice, "Upgrade button notice should not be active"
        assert self.popup.upgrade_btn_sprite == "UI5_Bottom_btn_9sl_Grey", f"Upgrade button sprite should be greyed out, found {self.popup.upgrade_btn_sprite}"
        refreshed_values = (
            *self.popup.get_progress_points(),
            self.popup.upgrade_price_text
        )
        assert initial_values == refreshed_values, (
            f"Upgrade button click should not change points or price, but got {refreshed_values}"
        )
        print(f"homenotice:{self.home_notice}")
        logger.info("Upgrade button deactivated successfully when points are insufficient.")
    def test_active_upgrade_btn(self):
        logger=get_logger()
        current_point,required_point= self.popup.get_progress_points()
        upgrade_price=int(self.popup.upgrade_price_text.replace(",",""))
        initial_values = (self.popup.get_actual_level(),current_point, required_point, upgrade_price)
        if current_point<required_point:
            logger.info("deactive upgrade button")
            return
        if upgrade_price>get_single_resource_amount(self.poco, "gold"):
            self.popup.upgrade_btn.click()
            popup_notice= self.poco("PopupNotice(Clone)") if self.poco("PopupNotice(Clone)").exists() else None
            assert popup_notice, "Popup Notice did not appear"
            popup_notice.offspring("bClose").click(sleep_interval=1)
            popup_notice= self.poco("PopupNotice(Clone)") if self.poco("PopupNotice(Clone)").exists() else None
            assert not popup_notice, "Popup Notice did not close after clicking close button"
            self.poco.invoke("add_gold", amount=upgrade_price)
            time.sleep(3)
            assert upgrade_price<get_single_resource_amount(self.poco, "gold"), f"Upgrade price {upgrade_price} is greater than gem amount {get_single_resource_amount(self.poco, 'gem')}"
        assert self.popup.upgrade_btn_notice, "Upgrade button notice should be active"
        assert self.popup.upgrade_btn_sprite=="UI5_Bottom_btn_9sl_Blue", f"Upgrade button sprite should be orange, found {self.popup.upgrade_btn_sprite}"
        self.popup.upgrade_btn.click(sleep_interval=3)
        expected_level= initial_values[0]+1
        expected_current_point= initial_values[1]- initial_values[2]
        expected_required_point = PopupMilitary.get_expected_required_point(expected_level + 1)
        expected_rank_category=rank_category[expected_level//10]
        expected_level_number= expected_level % 10
        expected_upgrade_price= PopupMilitary.get_expected_upgrade_price(expected_level+1)
        expected_passive_stats= self.popup.get_expected_stats_by_lv(expected_level)
        #verify state after click
        assert self.popup.get_actual_level() == expected_level, f"Level did not upgrade to {expected_level}"
        assert self.popup.get_progress_points()==(expected_current_point, expected_required_point), f"Progress points did not update correctly: {self.popup.get_progress_points()} != ({expected_current_point}, {expected_required_point})"
        assert self.popup.level_category_text== expected_rank_category, f"Rank category did not update to {expected_rank_category}"
        assert int(self.popup.level_number_text)== expected_level_number, f"Level number did not update to {expected_level_number}"
        assert int(self.popup.upgrade_price_text.replace(",",""))== expected_upgrade_price, f"Upgrade price did not update to {expected_upgrade_price}"
        actual_stats = [
            passive.passive_stat_text.rstrip("%")
            for passive in self.popup.passives
        ]
        actual_stats = [float(stat) for stat in actual_stats]
        assert actual_stats == expected_passive_stats, f"Passive stats did not update correctly: {actual_stats} != {expected_passive_stats}"
        self.test_deactive_upgrade_btn()
        logger.info(f"Upgrade button activated successfully. Level: {expected_level}, Current Point: {expected_current_point}, Required Point: {expected_required_point}, Upgrade Price: {expected_upgrade_price}")
    def test_home_notice(self):
        logger=get_logger()
        if not self.home_notice:
            logger.info("No home notice to check.")
            return
        assert self.home_notice.exists(), "Home notice not found"
        group_notice=[
            weapon_point.notice if weapon_point.notice.exists() else None
            for weapon_point in self.popup.weapon_points]
        assert any(notice is not None for notice in group_notice), "At least one notice should be visible"
        logger.info("Home notice and weapon point notices are present correctly.")
    def test_click_weapon_points(self):
        logger=get_logger()
        popup_get_point= None
        for i, weapon_point in enumerate(self.popup.weapon_points):
            weapon_point.root.click(sleep_interval=1)
            popup_get_point = PopupMilitaryGetPoint(self.poco,weapon_point._name)
            assert popup_get_point.root.exists(), f"Popup Military Get Point for {weapon_point.name} did not open"
            self.test_PopupMilitaryGetPoint(weapon_point._name, popup_get_point)
            popup_get_point.btn_back.click(sleep_interval=1)
    def test_PopupMilitaryGetPoint(self, name, popup_get_point):
        logger=get_logger()
        assert popup_get_point.middle_panel.exists(), "Middle panel not found"
        title= "Aircraft" if name =="Air" else name
        assert popup_get_point.title== title, f"Title text mismatch: {popup_get_point.title} != {title}"
        assert popup_get_point.generator.exists(), f"Generator {name} not found"
        assert len(popup_get_point.items) == len_of_weapon[title], f"Expected {len_of_weapon[title]} items, found {len(popup_get_point.items)}"
        for item in popup_get_point.items:
            assert item.root.exists(), f"Item {item.root.name} not found"
            if name == "Pilot":
                assert item.portrait.contains(f"{name}"), f"Item icon for {name} does not contain expected sprite"
                assert item.flag !="", f"Flag for {item.root.name} should not be empty"
                assert item.rarity_frame in ["R", "SR", "SSR"], f"Rarity frame for {item.root.name} should be R, SR, or SSR, found {item.rarity_frame}"
            else:
                assert item.item_icon.contains(f"{name}"), f"Item icon for {name} does not contain expected sprite"
            if title in ["Aircraft", "Drone", "Wing"]:
                assert int(item.star_text)>=2, f"Star text for {item.root.name} should be at least 2, found {item.star_text}"
            elif title == "Pilot":
                assert int(item.star_text)>=3, f"Star text for {item.root.name} should be at least 3, found {item.star_text}"
            elif title =="Engine":
                assert int(item.star_text)>=1, f"Star text for {item.root.name} should be at least 1, found {item.star_text}"
            else:
                raise ValueError(f"Unknown weapon type: {title}")
            assert item.star_icon.exists(), f"Star icon for {item.root.name} not found"
            if item.cover_BG:
                assert item.lock_icon.exists(), f"Lock icon for {item.root.name} not found"
                assert item.point_text is None,f"Point text for {item.root.name} should be None when locked"
                assert item.claimed_icon is None, f"Claimed icon for {item.root.name} should be None when locked"
            elif item.claimed_icon:
                assert item.point_text is None, f"Point text for {item.root.name} should be None when claimed"
                assert item.lock_icon is None, f"Lock icon for {item.root.name} should be None when claimed"
            elif item.point_text:
                assert int(item.point_text)>=1, f"Point text for {item.root.name} should be at least 1, found {item.point_text}"
                assert item.lock_icon is None, f"Lock icon for {item.root.name} should be None when point text is present"
                assert item.claimed_icon is None, f"Claimed icon for {item.root.name} should be None when point text is present"
