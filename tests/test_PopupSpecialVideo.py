from Hierarchy.PopupSpecialVideo import PopupSpecialVideo
from image_templates.Image_PopupSpecialVideo import *
from airtest.core.api import *
from utils import base_test
from utils.base_test import BaseTest
import re


class TestPopupSpecialVideo(BaseTest):
    def __init__(self):
        super().__init__()
        self.main_popup = PopupSpecialVideo(self.poco)

    def run_all_PopupSpecialVideo_tests(self):
        self.check_popup_exist()
        self.verify_top_elements()
        self.verify_video_blocks()
        self.test_click_back_btn()

    def check_popup_exist(self):
        assert self.main_popup.root.exists(), "PopupSpecialVideoReward popup not found!"
        print("✅ Popup root exists.")

    def verify_top_elements(self):
        assert self.main_popup.title.exists(), "Title element missing"
        assert self.main_popup.description.exists(), "Description element missing"
        assert self.main_popup.offer_wall.exists(), "OfferWall element missing"
        assert self.main_popup.countdown.exists(), "Countdown element missing"
        print("init "+self.main_popup.countdown.get_text())
        self.test_countdown()
        print("✅ Top-level elements verified.")

    def verify_popup_video_info(self):
        pvi=self.main_popup.popup_video_info
        assert pvi.root.exists(), "PopupVideoReward popup not found!"
        require_icon=[
            ("sIconGold", pvi.icon_gold),
            ("sIconGem", pvi.icon_gem),
            ("sIconCard", pvi.icon_card),
            ("sIconLife", pvi.icon_life),
            ("sIconPower", pvi.icon_power),
            ("sIconPower (1)", pvi.icon_power_duplicate),
            ("sIconEnergy", pvi.icon_energy),
            ("B_Back", pvi.btn_back)
        ]
        for name, icon in require_icon:
            assert icon.exists(), f"{name} icon not found!"
        print("✅ PopupVideoInfo elements verified.")
        pvi.btn_back.click() #back to main popup
        assert self.main_popup.root.exists(), "PopupSpecialVideoReward popup not found!"
        print("✅ Back to main popup.")

    def verify_video_blocks(self):
        video_blocks = [
            ("RandomVid", self.main_popup.random_video),
            ("GoldVid", self.main_popup.gold_video),
            ("GemVid", self.main_popup.gem_video),
            ("CardVid", self.main_popup.card_video),
            ("EnergyVid", self.main_popup.energy_video)
        ]
        for name, block in video_blocks:
            print(f"checking {name} block...")
            assert block.root.exists(), f"{name} video block not found!"
            assert block.label_up_to.exists(), f"{name} label_up_to not found!"
            assert block.watch_btn.exists(), f"{name} watch button not found!"
            assert block.watch_numb.exists(), f"{name} watch number not found!"
            assert block.reward_img.exists(), f"{name} Reward image not found!"
            if name == "RandomVid":
                assert block.info_btn().exists(), "Info button not found!"
                block.info_btn().click()
                self.verify_popup_video_info()
        print("✅ Video blocks verified.")

    def test_countdown(self):
        second1 = self.get_current_countdown()
        time.sleep(2)
        second2 = self.get_current_countdown()
        assert second2 < second1, "Countdown not decreasing!"
        print("✅ Countdown works correctly.")


    def get_current_countdown(self):
        """Get the current countdown value from the UI."""
        text = self.main_popup.root.offspring("lNextVideo").get_text()
        match = re.search(r'(\d+):(\d+):(\d+)', text)
        if not match:
            raise ValueError(f"Could not extract countdown from text: {text}")
        hours, minutes, seconds = map(int, match.groups())
        return hours * 3600 + minutes * 60 + seconds

    def test_click_back_btn(self):
        assert self.main_popup.back_btn.exists(), "Back button not found!"
        self.main_popup.back_btn.click()
        assert self.poco("HomeSquad_1").offspring("BtnAircraft").exists(), "Failed to return to home!"
        print("✅ Back button works correctly.")

    def test_offer_wall(self):
        assert self.main_popup.offer_wall.exists(), "OfferWall element missing"
        self.main_popup.offer_wall.click()
        assert wait(offer_wall, timeout=5, interval=3), "OfferWall not found!"
        poco(texture="btn_back").click()