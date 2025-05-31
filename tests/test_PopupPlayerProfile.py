from airtest.core.api import *
from utils.base_test import BaseTest
from Hierarchy.PopupPlayerProfile import *
from tests.test_AssetTab import *
from tests.test_StatTab import *

class TestPopupPlayerProfile(BaseTest):
    def __init__(self):
        super().__init__()
        self.popup = PopupPlayerProfile(self.poco)
        self.test_asset_tab = TestAssetTab(self.popup)
        self.test_stat_tab = TestStatTab(self.popup)

    def run_all_tests(self):
        # self.check_all_elements_exist()
        # self.check_navigating_asset_and_stat_tabs()
        # self.test_asset_tab.run_all_tests()
        self.test_stat_tab.run_all_tests()
        # Add more tests as needed


    def check_all_elements_exist(self):
        # Check if all main elements exist
        assert self.popup.root.exists(), "PopupPlayerProfile root not found!"
        assert self.popup.btnBack.exists(), "btnBack not found!"
        assert self.popup.title.exists(), "title not found!"
        assert self.popup.player_ava.exists(), "player_ava not found!"
        assert self.popup.player_flag.exists(), "player_flag not found!"
        assert self.popup.player_name.exists(), "player_name not found!"
        assert self.popup.player_id.exists(), "player_id not found!"
        self.check_valid_id()
        assert self.popup.btn_name_clan.exists(), "btn_name_clan not found!"
        assert self.popup.vip_icon.exists(), "vip_icon not found!"
        assert self.popup.btn_edit_profile.exists(), "btn_edit_profile not found!"
        assert self.popup.btn_asset.exists(), "btn_asset not found!"
        assert self.popup.btn_stat.exists(), "btn_stat not found!"
        print("✅ All main elements exist in PopupPlayerProfile!")

    def check_navigating_asset_and_stat_tabs(self):
        # Check if navigating to Asset and Stat tabs works
        btn_asset_activeBG = self.popup.btn_asset.child("BackgroundActive")
        btn_asset_deactiveBG = self.popup.btn_asset.child("BackgroundDeactive")
        btn_stat_activeBG = self.popup.btn_stat.child("BackgroundActive")
        btn_stat_deactiveBG = self.popup.btn_stat.child("BackgroundDeactive")
        self.popup.btn_asset.click()
        assert btn_asset_activeBG.exists(), "btn_asset_active not found!"
        assert btn_stat_deactiveBG.exists(), "btn_asset_deactive not found!"
        print("✅ Navigated to Asset tab successfully!")

        self.popup.btn_stat.click(sleep_interval=1)
        assert btn_stat_activeBG.exists(), "btn_stat_active not found!"
        assert btn_asset_deactiveBG.exists(), "btn_stat_deactive not found!"
        print("✅ Navigated to Stat tab successfully!")

    def head_to_asset_tab(self):
        # Navigate to Asset tab
        self.popup.btn_asset.click(sleep_interval=1)
        assert self.popup.asset_tab.root.exists(), "AssetTab root not found!"
        print("✅ Navigated to Asset tab successfully!")

    def head_to_stat_tab(self):
        # Navigate to Stat tab
        self.popup.btn_stat.click(sleep_interval=1)
        assert self.popup.stat_tab.root.exists(), "StatTab root not found!"
        print("✅ Navigated to Stat tab successfully!")

    def check_valid_id(self):
        # Check if player ID is valid
        id, id_numb = self.popup.player_id.get_text().split(" ")
        assert id_numb.isdigit() and len(id_numb) == 8, f"id_numb is not a valid 8-digit number: '{id_numb}'"
        assert id.startswith("id:"), f"id does not start with 'id:': '{id}'"
        print(f"✅ Player ID is valid: {id} {id_numb}")


