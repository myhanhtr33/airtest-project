from airtest.core.api import *
from utils.base_test import BaseTest
from Hierarchy.PopupPlayerProfile import *
from utils.get_resource_amount import clean_number

maxLevel= 301
minLevel= 1
starNormal_sprite="UI5_SelectLevel_Normal_Star_1"
starHard_sprite="UI5_SelectLevel_Hard_Star_1"
starHell_sprite="UI5_SelectLevel_Hell_Star_1"

class TestStatTab(BaseTest):
    def __init__(self, popup_player_profile):
        super().__init__()
        self.popup = popup_player_profile

    def run_all_tests(self):
        print("running all StatTab tests...")
        self.check_campaign_group()


    def check_campaign_group(self):
        print("checking campaign group...")
        assert self.popup.stat_tab.campaign_group.root.exists(), "campaign_group not found!"
        assert self.popup.stat_tab.campaign_group.title.exists(), "campaign_group title not found!"
        assert self.popup.stat_tab.campaign_group.title.child("lCampaign").get_text() == "Campaign", "campaign title text invalid!"
        normal_star=self.check_normal_campaign()
        hard_star=self.check_hard_campaign()
        hell_star=self.check_hell_campaign()
        total_star = normal_star + hard_star + hell_star
        assert self.popup.stat_tab.campaign_group.total_star_title.get_text().strip() == "Total star", "total star title text invalid!"
        assert self.popup.stat_tab.campaign_group.total_star_amount.get_text() == str(total_star), f"total star amount text invalid! Expected: {total_star}, Found: {self.popup.stat_tab.campaign_group.total_star_amount.get_text()}"
        print(f"total star text valid: {self.popup.stat_tab.campaign_group.total_star_amount.get_text()}")

    def check_normal_campaign(self):
        print("checking normal campaign...")
        assert self.popup.stat_tab.campaign_group.normal_title.get_text().strip() == "Normal", "normal campaign title text invalid!"
        assert self.popup.stat_tab.campaign_group.normal_lv.exists(), "normal campaign level not found!"
        assert self.popup.stat_tab.campaign_group.normal_star.exists(), "normal campaign star not found!"
        assert self.popup.stat_tab.campaign_group.normal_star_icon.exists(), "normal campaign star icon not found!"
        assert self.popup.stat_tab.campaign_group.normal_star_icon.attr("texture") == starNormal_sprite, "normal campaign star icon texture invalid!"
        normal_lv_text = self.popup.stat_tab.campaign_group.normal_lv.get_text()
        assert clean_number(normal_lv_text) in range(minLevel, maxLevel + 1), f"Normal Campaign Level '{normal_lv_text}' is out of range!"
        print(f"normal campaign level text valid: {normal_lv_text}")
        normal_star_text = self.popup.stat_tab.campaign_group.normal_star.get_text()
        assert clean_number(normal_star_text)>= clean_number(normal_lv_text), f"Normal Campaign Star '{normal_star_text}' is less than Level '{normal_lv_text}'!"
        print(f"normal campaign star text valid: {normal_star_text}")
        return clean_number(normal_star_text)

    def check_hard_campaign(self):
        print("checking hard campaign...")
        assert self.popup.stat_tab.campaign_group.hard_title.get_text().strip() == "Hard", "hard campaign title text invalid!"
        assert self.popup.stat_tab.campaign_group.hard_lv.exists(), "hard campaign level not found!"
        assert self.popup.stat_tab.campaign_group.hard_star.exists(), "hard campaign star not found!"
        assert self.popup.stat_tab.campaign_group.hard_star_icon.exists(), "hard campaign star icon not found!"
        assert self.popup.stat_tab.campaign_group.hard_star_icon.attr("texture") == starHard_sprite, "hard campaign star icon texture invalid!"
        hard_lv_text = self.popup.stat_tab.campaign_group.hard_lv.get_text()
        assert clean_number(hard_lv_text) in range(minLevel, maxLevel + 1), f"Hard Campaign Level '{hard_lv_text}' is out of range!"
        print(f"hard campaign level text valid: {hard_lv_text}")
        hard_star_text = self.popup.stat_tab.campaign_group.hard_star.get_text()
        assert clean_number(hard_star_text)>= clean_number(hard_lv_text), f"Hard Campaign Star '{hard_star_text}' is less than Level '{hard_lv_text}'!"
        print(f"hard campaign star text valid: {hard_star_text}")
        return clean_number(hard_star_text)

    def check_hell_campaign(self):
        print("checking hell campaign...")
        assert self.popup.stat_tab.campaign_group.hell_title.get_text().strip() == "Hell", "hell campaign title text invalid!"
        assert self.popup.stat_tab.campaign_group.hell_lv.exists(), "hell campaign level not found!"
        assert self.popup.stat_tab.campaign_group.hell_star.exists(), "hell campaign star not found!"
        assert self.popup.stat_tab.campaign_group.hell_star_icon.exists(), "hell campaign star icon not found!"
        assert self.popup.stat_tab.campaign_group.hell_star_icon.attr("texture") == starHell_sprite, "hell campaign star icon texture invalid!"
        hell_lv_text = self.popup.stat_tab.campaign_group.hell_lv.get_text()
        assert clean_number(hell_lv_text) in range(minLevel, maxLevel + 1), f"Hell Campaign Level '{hell_lv_text}' is out of range!"
        print(f"hell campaign level text valid: {hell_lv_text}")
        hell_star_text = self.popup.stat_tab.campaign_group.hell_star.get_text()
        assert clean_number(hell_star_text)>= clean_number(hell_lv_text), f"Hell Campaign Star '{hell_star_text}' is less than Level '{hell_lv_text}'!"
        print(f"hell campaign star text valid: {hell_star_text}")
        return clean_number(hell_star_text)



