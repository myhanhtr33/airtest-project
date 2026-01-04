import concurrent
import time
import pytest
from Hierarchy.PopupMilitary import *
from utils.device_setup import PocoManager
from airtest.core.api import *
from logger_config import get_logger
from utils.helper_functions import check_noti
from utils.get_resource_amount import get_single_resource_amount
from concurrent.futures import ThreadPoolExecutor
from functools import partial
import pdb
len_of_weapon={
    "Aircraft": 24,
    "Drone": 24,
    "Wing":24,
    "Pilot": 20,
    "Engine":18
}

@pytest.fixture(params=["Air", "Drone", "Wing", "Pilot", "Engine"])
def name(request) -> Literal["Air", "Drone", "Wing", "Pilot", "Engine"]:
    """Fixture that provides the name parameter for testing different military point types"""
    return request.param
@pytest.fixture(scope="class")
def military_popup(poco):
    try:
        popup = poco("PopupMilitaryCareer(Clone)") if poco("PopupMilitaryCareer(Clone)").exists() else None
        return popup
    except Exception as e:
        logger = get_logger()
        logger.warning(f"Failed to access PopupMilitary due to connection error: {e}")
        return None

@pytest.fixture(scope="class")
def military_back_button(poco):
    try:
        button = poco("PopupMilitaryCareer(Clone)").offspring("B_Back (1)")
        return button if button.exists() else None
    except Exception as e:
        logger = get_logger()
        logger.warning(f"Failed to access PopupMilitary back button due to connection error: {e}")
        return None
@pytest.mark.use_to_home(before=True, after=True, logger_name="PopupMilitary", back_button="military_back_button")
class TestPopupMilitary:
    popup= None
    weapon_point_notices = []
    @pytest.fixture(scope="function", autouse=True)
    def setup(cls, poco):
        logger = get_logger("setup method")
        logger.info("Setting up PopupMilitary test environment...")
        cls.poco = poco
        cls.home_notice = poco("SubFeatureTopLayer").offspring("sNotice") if poco("SubFeatureTopLayer").offspring(
            "sNotice").exists() else None
        military_home_icon = cls.poco("SubFeatureTopLayer").offspring("Military_Home")
        assert military_home_icon.exists(), "Military home icon not found"
        military_home_icon.click(sleep_interval=1)
        cls.popup = PopupMilitary(cls.poco)
        print(f"PopupMilitary instance created: {cls.popup}")
        assert cls.popup.root.exists(), "Military popup did not open"
        logger.info("PopupMilitary test environment setup complete.")

    def test_concurrent_exists(self,poco):
        import threading
        import time
        results = {}
        with poco.freeze() as fp:
            freeze_popup = PopupMilitary(fp)

        def check_back_button():
            nodes = {
                "frozen_btn_back": freeze_popup.btn_back,
                "frozen_top_panel": freeze_popup.top_panel,
                "frozen_upgrade_btn": freeze_popup.upgrade_btn,
                # "btn_back": self.popup.btn_back,
                # "top_panel": self.popup.top_panel,
            }
            for k, n in nodes.items():
                try:
                    # presence/visibility from snapshot
                    results[k] = n.exists()  # or n.exists()
                    print(f"Node {k} visibility: {results[k]}")
                except Exception as e:
                    results[k] = str(e)
                    print(f"Error accessing node {k}: {e}")
        def check_top_panel():
            nodes = {
                "frozen_rank_badge": freeze_popup.rank_badge,
                "frozen_upgrade_btn": freeze_popup.upgrade_btn,
                # "rank_badge": self.popup.rank_badge,
                # "upgrade_btn": self.popup.upgrade_btn,
            }
            for k, n in nodes.items():
                try:
                    # presence/visibility from snapshot
                    results[k] = n.exists()  # or n.exists()
                    print(f"Node {k} visibility: {results[k]}")
                except:
                    results[k] = "error"
                    print(f"Error accessing node {k}")
        t1 = threading.Thread(target=check_back_button)
        t2 = threading.Thread(target=check_top_panel)

        start_time = time.time()
        t1.start()
        t2.start()
        t1.join()
        t2.join()
        total = time.time() - start_time

        print(f"Total time: {total:.3f}s")
        # print(f"btn_back took: {results['btn_back']}")
        # print(f"top_panel took: {results['top_panel']}")
        for key, value in results.items(): print(f"{key}: {value}")

    def test_frozen_UI(self,poco):
        logger=get_logger()
        screen=poco.get_screen_size()
        print("::::BACKScreen size:",screen)

    def test_frozen_element_presence(self,poco):
        logger=get_logger()
        with poco.freeze() as fp:
            freeze_popup = PopupMilitary(fp)
        assert freeze_popup.btn_back.exists(), "Back button not found"
        assert freeze_popup.top_panel.exists(), "Top panel not found"
        assert freeze_popup.title.strip() == "Military Career", "Title text mismatch"
        assert freeze_popup.rank_badge.exists(), "Rank badge not found"
        assert freeze_popup.info_btn.exists(), "Info button not found"
        assert freeze_popup.mid_panel.exists(), "Mid panel not found"
        assert freeze_popup.mid_title.strip() == "All squads get", "Mid title text mismatch"
        assert len(freeze_popup.passives) == 6, "Expected 6 passives, found {}".format(len(freeze_popup.passives))
        for i, passive in enumerate(freeze_popup.passives):
            assert passive.root.exists(), f"Passive {i} not found"
            assert passive.sprite.exists(), f"Passive {i} sprite not found"
            assert passive.passive_stat_text != "", f"Passive {i} stat text is empty"
            assert passive.passive_stat_text.endswith("%"), f"Passive {i} stat text does not end with '%': {passive.passive_stat_text}"
        assert freeze_popup.bot_panel.exists(), "Bottom panel not found"
        assert freeze_popup.progress_fill.exists(), "Process fill not found"
        assert freeze_popup.progress_info_btn.exists(), "Process info button not found"
        assert freeze_popup.upgrade_btn.exists(), "Upgrade button not found"
        assert len(freeze_popup.weapon_points) == 5, "Expected 5 weapon points, found {}".format(len(freeze_popup.weapon_points))
        for i, weapon_point in enumerate(freeze_popup.weapon_points):
            assert weapon_point.root.exists(), f"Weapon point {i} not found"
            assert weapon_point.icon.exists(), f"Weapon point {i} icon not found"
            assert weapon_point.name not in ["", None], f"Weapon point {i} name is empty or None"
            assert int(weapon_point.accumulated_point) >=0, f"Weapon point {i} accumulated point is empty"
            if weapon_point.notice:
                self.weapon_point_notices.append(True)
            else:
                self.weapon_point_notices.append(False)
        assert freeze_popup.level_number_text.strip() != "", "Level number text is empty"
        assert freeze_popup.level_category_text.strip() != "", "Level category text is empty"
        assert freeze_popup.progress_text.strip() != "", "Process text is empty"
        assert freeze_popup.upgrade_price_text.strip() != "", "Upgrade price text is empty"
        logger.info("All elements are present and verified successfully.")

    @pytest.mark.order(1)
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
            assert weapon_point.name not in ["", None], f"Weapon point {i} name is empty or None"
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
    @pytest.mark.order(2)
    def test_valid_rank_category(self):
        logger=get_logger()
        actual_rank=self.popup.level_category_text
        assert actual_rank in rank_category, f"Invalid rank category: {actual_rank}"
        logger.info(f"rank category '{actual_rank}' is valid.")
    @pytest.mark.order(3)
    def test_click_info_button(self):
        logger=get_logger()
        self.popup.info_btn.click(sleep_interval=1)
        popup_info= PopupMilitaryCareerInfo(self.poco)
        assert popup_info.root.exists(), "Popup Military Career Info did not open"
        popup_info.btn_back.click(sleep_interval=1)
        assert not popup_info.root.exists(), "Popup Military Career Info did not close"
        logger.info("Info button functionality verified successfully.")
    @pytest.mark.order(4)
    def test_passive_sprite(self):
        logger=get_logger()
        actual_sprites=[
            passive.sprite.attr("texture").strip()
            for passive in self.popup.passives
        ]
        for i, actual_sprite in enumerate(actual_sprites):
            assert actual_sprite == expected_passive_sprites[i], f"Passive {i} sprite mismatch: {actual_sprite} != {expected_passive_sprites[i]}"
        logger.info("Passive sprite functionality verified successfully.")
    @pytest.mark.order(5)
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
    @pytest.mark.order(6)
    def test_click_progress_info_button(self):
        logger=get_logger()
        self.popup.progress_info_btn.click(sleep_interval=1.5)
        panel=self.poco("PanelTooltipInfo").offspring("lDes")
        panel_text=panel.get_text().strip()
        assert panel_text=="Career Point", "Progress info button did not show correct text"
        self.popup.progress_info_btn.click(sleep_interval=1.5)
        panel=self.poco("PanelTooltipInfo").offspring("lDes")
        assert not panel.exists(), "Panel did not close after clicking again"
    @pytest.mark.order(7)
    def test_valid_progress_point_and_price(self):
        logger=get_logger()
        actual_current_point,actual_required_point= self.popup.get_progress_points()
        assert actual_current_point >= 0, f"Current point is negative: {actual_current_point}"
        expected_required_point= PopupMilitary.get_expected_required_point(self.popup.get_actual_level()+1)
        assert actual_required_point == expected_required_point, f"Required point mismatch: {actual_required_point} != {expected_required_point}"
        actual_price=int(self.popup.upgrade_price_text.replace(",",""))
        assert actual_price==PopupMilitary.get_expected_upgrade_price(self.popup.get_actual_level()+1), f"Upgrade price mismatch: {actual_price} != {PopupMilitary.get_expected_upgrade_price(self.popup.get_actual_level()+1)}"
        logger.info(f"Progress points and upgrade price verified successfully: Current Point: {actual_current_point}, Required Point: {actual_required_point}, Upgrade Price: {actual_price}")

    @pytest.mark.order(8)
    def test_deactive_upgrade_btn(self):
        logger=get_logger()
        current_point,required_point= self.popup.get_progress_points()
        upgrade_price=self.popup.upgrade_price_text
        initial_values = (current_point, required_point, upgrade_price)
        if current_point>=required_point:
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
    @pytest.mark.order(9)
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

    @pytest.mark.order(10)
    def test_home_notice(self):
        logger=get_logger()
        if not self.home_notice:
            logger.info("No home notice to check.")
            return
        assert self.home_notice.exists(), "Home notice not found"
        group_notice=[
            weapon_point.notice
            for weapon_point in self.popup.weapon_points]
        assert any(notice is not None for notice in group_notice), "At least one notice should be visible"
        logger.info("Home notice and weapon point notices are present correctly.")
    @pytest.mark.order(11)
    def test_click_weapon_points(self):
        logger=get_logger()
        popup_get_point= None
        for i, weapon_point in enumerate(self.popup.weapon_points):
            logger.info(f"Clicking on weapon point {i+1}: {weapon_point.name}")
            weapon_point.root.click(sleep_interval=1)
            popup_get_point = PopupMilitaryGetPoint(self.poco,weapon_point._name)
            logger.info(f"Popup Military Get Point opened for {weapon_point.name}")
            assert popup_get_point.root.exists(), f"Popup Military Get Point for {weapon_point.name} did not open"
            expected_weapon_point=self.verify_PopupMilitaryGetPoint(weapon_point._name, popup_get_point)
            logger.info(f"Expected weapon point for {weapon_point._name}: {expected_weapon_point}")
            popup_get_point.btn_back.click(sleep_interval=1)
            actual_weapon_point=[int(wp.accumulated_point) for wp in self.popup.weapon_points ]
            logger.info(f"Actual weapon point after closing popup: {actual_weapon_point}")
            assert actual_weapon_point == expected_weapon_point, f"Weapon point for {weapon_point._name} did not update correctly: {actual_weapon_point} != {expected_weapon_point}"
    def verify_PopupMilitaryGetPoint(self, name:str, popup_get_point:PopupMilitaryGetPoint)->list[int]:
        """Helper method to test popup get point functionality
            Args:
                name: The weapon point name (Air, Drone, Wing, Pilot, Engine)
                popup_get_point: Instance of PopupMilitaryGetPoint created in test_click_weapon_points
            Returns:
                list[int]: List of accumulated points for each weapon
        """
        logger=get_logger()
        list_point=[(point._name,int(point.accumulated_point)) for point in popup_get_point.weapon_points ]
        logger.info(f"Popup Military Get Point {name} opened")
        assert popup_get_point.middle_panel.exists(), "Middle panel not found"
        title= "Aircraft" if name =="Air" else name
        assert popup_get_point.title== title, f"Title text mismatch: {popup_get_point.title} != {title}"
        assert popup_get_point.generator.exists(), f"Generator {name} not found"
        # assert len(popup_get_point.items) == len_of_weapon[title], f"Expected {len_of_weapon[title]} items, found {len(popup_get_point.items)}"
        def check_item(item):
            logger.info(f"Item {item.root} checking")
            assert item.root.exists(), f"Item {item.root} not found"

            if name == "Pilot":
                assert name.lower() in item.portrait.lower(), f"Item icon for {name} does not contain expected sprite"
                assert item.flag != "", f"Flag for {item.root.name} should not be empty"
                assert any(r in item.rarity_frame for r in ["R", "SR", "SSR"]), \
                    f"Rarity frame for {item.root.name} should contain R, SR, or SSR, found {item.rarity_frame}"
            else:
                icon = name.lower() if name.lower() != "drone" else "wingman"
                assert icon in item.item_icon.lower(), f"Item icon for {name} does not contain expected sprite"

            if title in ["Aircraft", "Drone", "Wing"]:
                assert int(
                    item.star_text) >= 2, f"Star text for {item.root.name} should be at least 2, found {item.star_text}"
            elif title == "Pilot":
                assert int(
                    item.star_text) >= 3, f"Star text for {item.root.name} should be at least 3, found {item.star_text}"
            elif title == "Engine":
                assert int(
                    item.star_text) >= 1, f"Star text for {item.root.name} should be at least 1, found {item.star_text}"
            else:
                raise ValueError(f"Unknown weapon type: {title}")

            assert item.star_icon.exists(), f"Star icon for {item.root.name} not found"

            if item.cover_BG:
                assert item.lock_icon.exists(), f"Lock icon for {item.root.name} not found"
                assert item.point_text is None, f"Point text for {item.root.name} should be None when locked"
                assert item.claimed_icon is None, f"Claimed icon for {item.root.name} should be None when locked"
            elif item.claimed_icon:
                assert item.point_text is None, f"Point text for {item.root.name} should be None when claimed"
                assert item.lock_icon is None, f"Lock icon for {item.root.name} should be None when claimed"
            elif item.point_text:
                assert int(
                    item.point_text) >= 1, f"Point text for {item.root.name} should be at least 1, found {item.point_text}"
                assert item.lock_icon is None, f"Lock icon for {item.root.name} should be None when point text is present"
                assert item.claimed_icon is None, f"Claimed icon for {item.root.name} should be None when point text is present"
            logger.info(f"Item {item.root} done checking")
        def claim_point(item):
            point=int(item.point_text)
            item.root.click(sleep_interval=1)
            assert item.point_text is None, f"Point text for {item.root.name} should be None after claiming"
            item.root.click()
            check_noti(self.poco,"You have already claimed the reward")
            return point
        for item in popup_get_point.items:
            check_item(item)
            if item.point_text: # if item has point text to be claimed
                logger.info(f"Claiming point for item {item.root}")
                initial_point=next(point.accumulated_point for point in popup_get_point.weapon_points if point._name == name)
                logger.info(f"Initial accumulated point for {name}: {initial_point}")
                increased_point=claim_point(item)
                logger.info(f"Increased point for {name}: {increased_point}")
                sleep(1)
                updated_point = next(point.accumulated_point for point in popup_get_point.weapon_points if point._name == name)
                logger.info(f"Updated accumulated point for {name}: {updated_point}")
                assert int(updated_point) == int(initial_point) + increased_point, \
                    f"Accumulated point for {name} did not update correctly: {updated_point} != {initial_point} + {increased_point}"
                list_point = [(point[0], point[1] + (increased_point if point[0] == name else 0)) for point in list_point]
                logger.info(f"List of points after claiming: {list_point}")
        return [int(point[1]) for point in list_point]

    @pytest.mark.order(12)
    def test_persistence_after_reopening(self):
        logger = get_logger()
        logger.info("Capturing initial state before closing popup")

        # Capture initial state
        initial_state = {
            'level_number': self.popup.level_number_text,
            'level_category': self.popup.level_category_text,
            'progress_text': self.popup.progress_text,
            'upgrade_price': self.popup.upgrade_price_text,
            'passive_stats': [passive.passive_stat_text for passive in self.popup.passives],
            'weapon_points': [point.accumulated_point for point in self.popup.weapon_points]
        }

        logger.info(f"Initial state: {initial_state}")

        # Close popup
        logger.info("Closing PopupMilitary")
        self.popup.btn_back.click(sleep_interval=1)
        assert not self.popup.root.exists(), "Popup did not close properly"

        # Reopen popup
        logger.info("Reopening PopupMilitary")
        military_home_icon = self.poco("SubFeatureTopLayer").offspring("Military_Home")
        assert military_home_icon.exists(), "Military home icon not found"
        military_home_icon.click(sleep_interval=1)

        # Wait for popup to fully load
        time.sleep(1)

        # Create new popup instance
        self.popup = PopupMilitary(self.poco)
        assert self.popup.root.exists(), "Military popup did not reopen"

        # Capture new state
        reopened_state = {
            'level_number': self.popup.level_number_text,
            'level_category': self.popup.level_category_text,
            'progress_text': self.popup.progress_text,
            'upgrade_price': self.popup.upgrade_price_text,
            'passive_stats': [passive.passive_stat_text for passive in self.popup.passives],
            'weapon_points': [point.accumulated_point for point in self.popup.weapon_points]
        }

        logger.info(f"Reopened state: {reopened_state}")

        # Compare states
        assert initial_state['level_number'] == reopened_state['level_number'], \
            f"Level number changed: {initial_state['level_number']} -> {reopened_state['level_number']}"

        assert initial_state['level_category'] == reopened_state['level_category'], \
            f"Level category changed: {initial_state['level_category']} -> {reopened_state['level_category']}"

        assert initial_state['progress_text'] == reopened_state['progress_text'], \
            f"Progress text changed: {initial_state['progress_text']} -> {reopened_state['progress_text']}"

        assert initial_state['upgrade_price'] == reopened_state['upgrade_price'], \
            f"Upgrade price changed: {initial_state['upgrade_price']} -> {reopened_state['upgrade_price']}"

        for i, (initial_stat, reopened_stat) in enumerate(
                zip(initial_state['passive_stats'], reopened_state['passive_stats'])):
            assert initial_stat == reopened_stat, \
                f"Passive stat {i} changed: {initial_stat} -> {reopened_stat}"

        for i, (initial_point, reopened_point) in enumerate(
                zip(initial_state['weapon_points'], reopened_state['weapon_points'])):
            assert initial_point == reopened_point, \
                f"Weapon point {i} accumulated point changed: {initial_point} -> {reopened_point}"

        logger.info("All elements persisted correctly after reopening the popup")