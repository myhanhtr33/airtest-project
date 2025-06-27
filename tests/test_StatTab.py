from turtledemo.paint import switchupdown

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
        # self.check_pvp_group()
        self.check_endless_group()
        self.check_champion_group()

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
        assert self.popup.stat_tab.pvp_group.icon.exists(), "pvp_group title not found!"
        assert self.popup.stat_tab.pvp_group.icon.child("lPVP").get_text() == "PvP", "pvp title text invalid!"
        self.check_pvpT1()
        self.check_pvpT2()
        self.check_pvp_vs2()
        stats = [("t1", self.popup.stat_tab.pvp_group.get_t1_stats()),
                 ("t2", self.popup.stat_tab.pvp_group.get_t2_stats()),
                 ("vs2", self.popup.stat_tab.pvp_group.get_vs2_stats())]
        for type, raw in stats:
            print(f"checking stats for type: {type}...")
            raw = clean_stats(raw)
            validate_pvp_stats(raw, type)

    def check_endless_group(self):
        print("checking endless group...")
        assert self.popup.stat_tab.endless_group.root.exists(), "endless_group not found!"
        assert self.popup.stat_tab.endless_group.icon.exists(), "endless_group title not found!"
        assert self.popup.stat_tab.endless_group.title.get_text().strip() == "Endless", "endless title text invalid!"
        assert self.popup.stat_tab.endless_group.text.get_text().strip() == "Longest run all the time", "endless text invalid!"
        score= int(self.popup.stat_tab.endless_group.best_score.get_text().strip())
        assert score in range(0,700), "endless best score text invalid!"

    def check_champion_group(self):
        print("checking champion group...")
        assert self.popup.stat_tab.champion_group.root.exists(), "champion_group not found!"
        assert self.popup.stat_tab.champion_group.icon.exists(), "champion_group icon not found!"
        assert self.popup.stat_tab.champion_group.title.get_text().strip() == "Champions League", "champion title text invalid!"
        stat= clean_stats(self.popup.stat_tab.champion_group.get_stats())
        validate_champion_stats(stat)


    def check_pvpT1(self):
        print("checking pvp T1...")
        assert self.popup.stat_tab.pvp_group.tier1_label.exists(), "pvp T1 label not found!"
        assert self.popup.stat_tab.pvp_group.tier1_split.exists(), "pvp T1 split not found!"
        assert self.popup.stat_tab.pvp_group.tier1_rank.exists(), "pvp T1 rank not found!"
        assert self.popup.stat_tab.pvp_group.tier1_elo.exists(), "pvp T1 elo not found!"
        assert self.popup.stat_tab.pvp_group.tier1_rank_icon.exists(), "pvp T1 rank icon not found!"
        assert self.popup.stat_tab.pvp_group.tier1_total_win.exists(), "pvp T1 total win not found!"
        assert self.popup.stat_tab.pvp_group.tier1_win_rate.exists(), "pvp T1 win rate not found!"

    def check_pvpT2(self):
        print("checking pvp T2...")
        assert self.popup.stat_tab.pvp_group.tier2_label.exists(), "pvp T2 label not found!"
        assert self.popup.stat_tab.pvp_group.tier2_split.exists(), "pvp T2 split not found!"
        assert self.popup.stat_tab.pvp_group.tier2_rank.exists(), "pvp T2 rank not found!"
        assert self.popup.stat_tab.pvp_group.tier2_elo.exists(), "pvp T2 elo not found!"
        assert self.popup.stat_tab.pvp_group.tier2_rank_icon.exists(), "pvp T2 rank icon not found!"
        assert self.popup.stat_tab.pvp_group.tier2_total_win.exists(), "pvp T2 total win not found!"
        assert self.popup.stat_tab.pvp_group.tier2_win_rate.exists(), "pvp T2 win rate not found!"

    def check_pvp_vs2(self):
        print("checking 2VS2 ...")
        assert self.popup.stat_tab.pvp_group.vs2_label.exists(), "2VS2 label not found!"
        assert self.popup.stat_tab.pvp_group.vs2_split.exists(), "2VS2 split not found!"
        assert self.popup.stat_tab.pvp_group.vs2_rank.exists(), "2VS2 rank not found!"
        assert self.popup.stat_tab.pvp_group.vs2_score.exists(), "2VS2 score not found!"
        assert self.popup.stat_tab.pvp_group.vs2_rank_icon.exists(), "2VS2 rank icon not found!"
        assert self.popup.stat_tab.pvp_group.vs2_total_win.exists(), "2VS2 total win not found!"
        assert self.popup.stat_tab.pvp_group.vs2_win_rate.exists(), "2VS2 win rate not found!"

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
    print(f"cleaned stats: {cleaned}")
    return cleaned

def validate_pvp_stats(stats, type):
    """
        Given a cleaned stats-dict, assert each field meets your requirements:
          - label in {"PvP Tier 1", "PvP Tier 2", "2 vs 2"}
          - rank ∈ {"Not ranked yet"} ∪ {Bronze I..V, Silver I..V, Gold I..V, …} ∪ {"Master", "Challenger", "Legendary"}
          - elo matches "ELO: {number}" with 1000 ≤ number ≤ 6000
          - rank_icon contains "PVP_rank" for PvP tiers, "2vs2Chest" for 2 vs 2
          - total_win matches "Total win: {positive int}"
          - win_rate matches either "Win rate: N/A" or "Win rate: {number}%"
        """
    #allowed values
    allowed_labels = {"PvP Tier 1", "PvP Tier 2", "2 vs 2"}
    roman=["I", "II", "III", "IV", "V"]
    categories=["Bronze", "Silver", "Gold", "Platinum", "Diamond", "Master", "Challenger", "Legendary"]
    allowed_ranks= {"Not ranked yet"} | {f"{cat} {lv}" for cat in categories for lv in roman}
    # Validate label
    label = stats["label"]
    type_to_label = {"t1": "PvP Tier 1", "t2": "PvP Tier 2", "vs2": "2 vs 2"}
    expected_label = type_to_label[type]
    if type in type_to_label.keys():
        assert label == expected_label, f"Label for {expected_label} invalid: {label}"
    else:
        raise ValueError(f"Invalid type: {type}. Expected 't1', 't2', or 'vs2'.")
    # Validate rank
    if type == "t1" or type == "t2":
        m = re.match(r"ELO:\s*(\d+)", stats["elo"])
        assert m, f"ELO format invalid: {stats['elo']}"
    elif type == "vs2":
        m= re.match(r"Score:\s*(\d+)", stats["elo"])
        assert m, f"Score format invalid: {stats['elo']}"
    elo= int(m.group(1))
    assert 1000 <= elo <= 6000, f"ELO value out of range: {elo}"
    # Validate rank icon
    icon=stats["rank_icon"]
    if label.startswith("PvP Tier"):
        assert "PVP_rank" in icon, f"Rank icon texture invalid for {label}: {icon}"
    elif label.startswith("2 vs 2"):
        assert "2vs2Chest" in icon, f"Rank icon texture invalid for {label}: {icon}"
    else:
        raise ValueError(f"Invalid label for rank icon validation: {label}")
    # Validate total win
    m2=re.match(r"Total win:\s*(\d+)", stats["total_win"])
    assert m2, f"Total win format invalid: {stats['total_win']}"
    wins= int(m2.group(1))
    assert wins>=0, f"Total win cannot be negative: {wins}"
    # Validate win rate
    win_field=stats["win_rate"]
    if win_field=="[999999]Win rate:[-] N/A[-]":
        pass
    else:
        m3=re.match(r"Win rate:\s*(\d+)%", win_field)
        assert m3, f"Win rate format invalid: {win_field}"
        win_rate= int(m3.group(1))
        assert 0 <= win_rate <= 100, f"Win rate out of range: {win_rate}"

def validate_champion_stats(stats):
    print("START validate_champion_stats")
    # Validate best points
    m1=re.match(r"Best point:\s*(\d+)", stats["best"])
    assert m1, f"Best point format invalid: {stats['best']}"
    best_points = int(m1.group(1))
    assert best_points >= 0, f"Best points cannot be negative: {best_points}"
    #validate total points
    m = re.match(r"Total points:\s*(\d+)", stats["total"])
    assert m, f"Total points format invalid: {stats['total']}"
    total_points = int(m.group(1))
    assert total_points >= best_points, f"Total points {total_points} cannot be less than best points {best_points}"
    # Validate winning times
    m2 = re.match(r"Winning times:\s*(\d+)", stats["top1"])
    assert m2, f"Winning times format invalid: {stats['top1']}"
    winning_times = int(m2.group(1))
    assert winning_times >= 0, f"Winning times cannot be negative: {winning_times}"





