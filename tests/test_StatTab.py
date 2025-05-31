from airtest.core.api import *
from utils.base_test import BaseTest
from Hierarchy.PopupPlayerProfile import *
from utils.get_resource_amount import clean_number
import re

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
        # self.check_campaign_group()
        self.check_pvpT1()

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

    def check_pvp_group(self):
        print("checking pvp group...")
        assert self.popup.stat_tab.pvp_group.root.exists(), "pvp_group not found!"
        assert self.popup.stat_tab.pvp_group.title.exists(), "pvp_group title not found!"
        assert self.popup.stat_tab.pvp_group.title.child("lPVP").get_text() == "PvP", "pvp title text invalid!"
        self.check_pvpT1()

    def check_pvpT1(self):
        print("checking pvp T1...")
        assert self.popup.stat_tab.pvp_group.tier1_label.exists(), "pvp T1 label not found!"
        assert self.popup.stat_tab.pvp_group.tier1_split.exists(), "pvp T1 split not found!"
        assert self.popup.stat_tab.pvp_group.tier1_rank.exists(), "pvp T1 rank not found!"
        assert self.popup.stat_tab.pvp_group.tier1_elo.exists(), "pvp T1 elo not found!"
        assert self.popup.stat_tab.pvp_group.tier1_rank_icon.exists(), "pvp T1 rank icon not found!"
        assert self.popup.stat_tab.pvp_group.tier1_total_win.exists(), "pvp T1 total win not found!"
        assert self.popup.stat_tab.pvp_group.tier1_win_rate.exists(), "pvp T1 win rate not found!"
        t1Stat= self.popup.stat_tab.pvp_group.get_t1_stats()
        print("pvp T1 stats: ", t1Stat)
        print("pvpT2 stats:", self.popup.stat_tab.pvp_group.get_t2_stats())
        print("pvp 2v2 stats:", self.popup.stat_tab.pvp_group.get_vs2_stats())

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

def clean_stats(raw_stats):
# Clean out the "[123456]" and "[-]" tokens so you end up with
# e.g. "ELO: 1176", "Total win: 16", etc.
    cleaned={}
    for key, val in raw_stats.items():
        # remove [digits] and standalone [-]
        s = re.sub(r"\[\d+\]", "", val)
        s = s.replace("[-]", "")
        cleaned[key] = s.strip()
    return cleaned

def validate_pvp_stats(stats):
    #allowed values
    allowed_labels = {"PvP Tier 1", "PvP Tier 2", "2 vs 2"}
    roman=["I", "II", "III", "IV", "V"]
    categories=["Bronze", "Silver", "Gold", "Platinum", "Diamond", "Master", "Challenger", "Legendary"]
    allowed_ranks= {"Not ranked yet"} | {f"{cat} {lv}" for cat in categories for lv in roman}





