from Hierarchy.PopupSpecialVideo import PopupSpecialVideo
from image_templates.Image_PopupSpecialVideo import *
from utils.sprite_mapping import *
from utils.get_resource_amount import *
from utils.helper_functions import *
from airtest.core.api import *
from utils import base_test
from utils.base_test import BaseTest
from Hierarchy.CurrencyBar import *
import re
from poco.drivers.android.uiautomation import AndroidUiautomationPoco


class TestPopupSpecialVideo(BaseTest):
    def __init__(self):
        super().__init__()
        self.main_popup = PopupSpecialVideo(self.poco)
        self.pocoAndroid = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False)

    def run_all_PopupSpecialVideo_tests(self):
        self.check_popup_exist()
        self.verify_top_elements()
        self.verify_video_blocks()
        self.test_click_video_block()
        self.test_click_back_btn() #head back to homes


    def check_popup_exist(self):
        assert self.main_popup.root.exists(), "PopupSpecialVideoReward popup not found!"
        print("✅ Popup root exists.")

    def verify_top_elements(self):
        assert self.main_popup.title.exists(), "Title element missing"
        assert self.main_popup.description.exists(), "Description element missing"
        self.test_offer_wall()
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
            assert (block.watch_btn is None) is not (block.deactivate_watch_btn is None), f"{name} both watch buttons are activated or deactivated!"
            assert block.watch_numb.exists(), f"{name} watch number not found!"
            assert block.reward_img.exists(), f"{name} Reward image not found!"
            if name == "RandomVid":
                assert block.info_btn().exists(), "Info button not found!"
                block.info_btn().click()
                self.verify_popup_video_info()
        print("✅ Video blocks verified.")

    def test_countdown(self):
        assert self.main_popup.countdown.exists(), "Countdown element missing"
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
        close_btn_offerwall = self.pocoAndroid("android.widget.Button")
        assert wait(offer_wall, timeout=3, interval=1), "OfferWall not found!"
        assert close_btn_offerwall.exists(), "Close button in offerwall not found!"
        close_btn_offerwall.click()
        assert wait(top_element_PopupSpecialVideo, timeout=3, interval=1), "successfull back to main popup!"
        print("✅ OfferWall works correctly.")

    def test_click_video_block(self):
        video_blocks = [
            ("RandomVid", self.main_popup.random_video),
            ("GoldVid", self.main_popup.gold_video),
            ("GemVid", self.main_popup.gem_video),
            ("CardVid", self.main_popup.card_video),
            ("EnergyVid", self.main_popup.energy_video)
        ]
        for name, block in video_blocks:
            print(f"checking {name} block...")
            if self.get_watch_number(block) == 3:
                print("checking deactive watch button...")
                self.check_deactive_watch_btn(block,name )
            else:
                print("checking active watch button...")
                self.check_active_watch_btn(block,name, self.get_watch_number(block))
        print("✅ Video blocks clickable.")

    def get_watch_number(self,block):
        # Re-query the block's root and locate watch_numb again
        root = block.root  # or self.poco().offspring("block_root_name")
        watch_numb = root.offspring("lRate")  # Assuming this is always "lRate"
        watch_numb_text= watch_numb.get_text()
        try:
            watched, total = map(int, watch_numb_text.split("/"))
        except ValueError:
            raise ValueError(f"Invalid watch_numb format: {watch_numb_text}")
        print (f"Watched: {watched}, Total: {total}")
        assert total==3, "Total number of videos not 3!"
        assert watched in range(0,4), "Number of watched videos not in range 0-3!"
        return watched

    def check_deactive_watch_btn(self, block,name):
        assert block.deactivate_watch_btn.exists(), "Deactivated watch button not found!"
        block.deactivate_watch_btn.click()
        # 1. Wait for appearance
        noti = self.poco("PanelNotification").offspring("lNotification")
        assert wait_for_element(noti, condition="appear"), "Notification not found!"
        print("✅ Notification appeared.")
        # 2. Check exact text
        actual_text = noti.get_text().strip()
        assert actual_text == "Sold out", f"Unexpected notification text: '{actual_text}'"
        # 3. Wait for disappearance
        assert wait_for_element(noti,condition="disappear"), "Notification did not disappear!"
        print("✅ Notification disappeared.")
        print(f"{name} deactivated watch button works correctly.")

    def check_active_watch_btn(self, block,name, before_watch_numb):
        #1: Click Watch Button
        before_resource= self._click_watch(block)
        #2: Wait for and parse reward popup
        reward, sprite, amount=self._get_reward_data()
        #3: Determine expected item from reward
        item,buffer= self._resolve_reward_item(sprite, name)
        #4: Check reward sprite
        if item:
            check_sprite_known_resource(item, sprite)
        #5: claim reward
        self._claim_reward()
        #6: verify resource amount change
        if item:
            self._verify_resource_amount_change(item,amount,buffer, before_resource)
        #7: validate watch number increment
        self._validate_watch_number_increment(block, before_watch_numb)

    def _click_watch(self,block):
        assert block.watch_btn.exists(), "Active watch button not found!"
        before_resource = get_all_resource_amounts(self.poco)
        block.watch_btn.click(sleep_interval=0.5)
        return before_resource
        #assume the video is played

    def _get_reward_data(self):
        popup = self.poco("PopupRewardItem(Clone)")
        assert popup.exists(), "popup reward not found!"
        reward = self.poco("PopupRewardItem(Clone)").offspring("single").offspring("UIItemIcon")
        sprite = str(reward.offspring("sIcon").attr("texture"))
        amount = clean_number(reward.offspring("lQuantity").get_text())
        return reward, sprite, amount

    def _resolve_reward_item(self, sprite, name):
        item, buffer = None, 2
        if name == "GoldVid":
            return "gold", 1000
        elif name == "GemVid":
            return "gem", buffer
        elif name == "EnergyVid":
            return "energy", buffer
        elif name == "RandomVid":
            key = next((k for k, v in RESOURCE_SPRITE_MAPPING.items() if v == sprite),
                       None)  # find the key if sprite is in the value
            if key:
                return key, buffer
            else:
                print(f"No matching key found for sprite: {sprite}")
        return item, buffer

    def _verify_resource_amount_change(self, item, amount, buffer, beforeResource):
         afterResource = get_all_resource_amounts(self.poco)
         expectResource = beforeResource.get(item) + amount
         if abs(expectResource - afterResource.get(item)) in range(buffer):
             print(f"expect {item} amount: {expectResource}, after {item} amount: {afterResource}")
         else:
             raise AssertionError(
                 f"❌ Resource mismatch for {item}: expected {expectResource}, got {afterResource.get(item)}")

    def _validate_watch_number_increment(self, block, before_watch_numb):
         after_watch_numb = self.get_watch_number(block)
         assert after_watch_numb == before_watch_numb + 1, f"Watch number did not increment: before={before_watch_numb}, after={after_watch_numb}"
         print("✅ Watch number incremented correctly.")

    def _claim_reward(self):
            btnClaim = self.poco("PopupRewardItem(Clone)").offspring("bClaim")
            btnClaim.click(sleep_interval=0.5)



