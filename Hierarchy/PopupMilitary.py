import datetime
import os
import datetime, time

import pandas as pd
from typing import Literal
current_dir=os.path.dirname(os.path.abspath(__file__))
file_path= os.path.join(os.path.dirname(current_dir),"Data","Military.xlsx")
type=["Aircraft", "Drone", "Wing", "Pilot", "Engine"]
rank_category = ["Sergeant",
                 "Second Lieutenant",
                 "First Lieutenant",
                 "Captain",
                 "Major",
                 "Lieutenant Colonel",
                 "Colonel",
                 "Brigadier General",
                 "Major General",
                 "General",
                 "General of the Air Force"]
expected_passive_sprites=["UI_Career_Pass",
                          "HP",
                          "Crit_Chance",
                          "Crit_Damage",
                          "Block_Damage",
                          "Reduce_Damage"]
class PopupMilitary:
    def __init__(self, poco):
        self.poco = poco
        self.root= self.poco("PopupMilitaryCareer(Clone)")
        self.btn_back = self.root.offspring("B_Back (1)")
        self.top_panel = self.root.offspring("TopDecord")
        self.title = self.top_panel.offspring("lTitle").get_text() if self.top_panel.offspring("lTitle").exists() else None
        self.rank_badge= self.top_panel.offspring("Spine GameObject (Career Rank)")
        self.info_btn= self.top_panel.offspring("bInfo")
        self.mid_panel = self.root.offspring("TopMiddle")
        self.mid_title = self.mid_panel.offspring("lTitle (1)").get_text() if self.mid_panel.offspring("lTitle (1)").exists() else None
        # self.passives=[]
        # for i in range(1,7):
        #     node=self.mid_panel.offspring(f"Passive{i}")
        #     if node.exists():
        #         _stat = {1: "lAtk", 2: "lHP", 3: "lCritChance", 4: "lCritDamage", 5: "lBlockDamage", 6: "lReduceDamage"}[i]
        #         self.passives.append(Passive(node,_stat))
        self.bot_panel = self.root.offspring("TopBottom")
        self.progress_fill = self.bot_panel.offspring("sFill")
        self.progress_info_btn = self.bot_panel.offspring("bInfo")
        self.upgrade_btn = self.bot_panel.offspring("BtnUpdate")
        # self.weapon_points = []
        # for i in range(5):
        #     _type= type[i]
        #     _name={1: "Air", 2: "Drone", 3: "Wing", 4: "Pilot", 5: "Engine"}[i+1]
        #     node= self.bot_panel.offspring(f"{_type}Point")
        #     if node.exists():
        #         self.weapon_points.append(WeaponPoint(node,_name))
    @property
    def passives(self):
        result = []
        for i in range(1, 7):
            node = self.mid_panel.offspring(f"Passive{i}")
            if node.exists():
                _stat = \
                {1: "lAtk", 2: "lHP", 3: "lCritChance", 4: "lCritDamage", 5: "lBlockDamage", 6: "lReduceDamage"}[i]
                result.append(Passive(node, _stat))
        return result
    @property
    def weapon_points(self):
        result = []
        for i in range(5):
            _type = type[i]
            _name = {1: "Air", 2: "Drone", 3: "Wing", 4: "Pilot", 5: "Engine"}[i + 1]
            node = self.bot_panel.offspring(f"{_type}Point")
            if node.exists():
                result.append(WeaponPoint(node, _name))
        return result
    @property
    def level_number_text(self):
        return self.rank_badge.offspring("lLevel").get_text().strip() if self.rank_badge.offspring("lLevel").exists() else None
    @property
    def level_category_text(self):
        return self.top_panel.offspring("lRank").get_text().strip() if self.top_panel.offspring("lRank").exists() else None
    @property
    def progress_text(self):
        return self.bot_panel.offspring("lProcess").get_text().strip() if self.bot_panel.offspring("lProcess").exists() else None
    @property
    def upgrade_price_text(self):
        return self.upgrade_btn.offspring("lUpgrade").get_text().strip() if self.upgrade_btn.offspring("lUpgrade").exists() else None
    @property
    def upgrade_btn_notice(self):
        return self.upgrade_btn.offspring("sNotice") if self.upgrade_btn.offspring("sNotice").exists() else None
    @property
    def upgrade_btn_sprite(self):
        return self.upgrade_btn.offspring("sBtnUpdate").attr("texture") if self.upgrade_btn.offspring("sBtnUpdate").exists() else None
    def get_actual_level(self):
        for i, category in enumerate(rank_category):
            if self.level_category_text == category:
                return i*10 + int(self.level_number_text)

    def get_expected_stats_by_lv(self,level:int)->list:
        df = pd.read_excel(file_path)
        row = df[df["Level"] == level]
        if row.empty:
            raise ValueError(f"Level {level} not found in the data.")
        stats = row[
            ["Atk", "hp", "crit chance", "crit dmg", "dodge chance", "reduce dmg taken"]].values.flatten().tolist()
        return stats
    @staticmethod
    def get_expected_required_point(level:int)->int:
        df = pd.read_excel(file_path)
        row = df[df["Level"] == level]
        if row.empty:
            raise ValueError(f"Level {level} not found in the data.")
        required_point = row["PointRequired"].values[0]
        return required_point
    @staticmethod
    def get_expected_upgrade_price(level:int)->int:
        df = pd.read_excel(file_path)
        row = df[df["Level"] == level]
        if row.empty:
            raise ValueError(f"Level {level} not found in the data.")
        upgrade_price = row["Gold Price"].values[0]
        return upgrade_price
    def get_progress_points(self):
        if not self.progress_text:
            return None
        current, required = map(int, self.progress_text.split('/'))
        return int(current), int(required)

class Passive:
    def __init__(self,node,_stat):
        self.root= node
        self.sprite = self.root.offspring("sPassive")
        self.stat = _stat
    @property
    def passive_stat_text(self):
        return self.root.offspring(self.stat).get_text().strip() if self.root.offspring(self.stat).exists() else None
class WeaponPoint:
    def __init__(self,node,name):
        self.root= node
        self._name = name
    @property
    def icon(self):
        return self.root.offspring("sIcon")
    @property
    def name(self):
        return self.root.offspring(f"l{self._name}").get_text().strip() if self.root.offspring(
            f"l{self._name}").exists() else None
    @property
    def accumulated_point(self):
        return self.root.offspring(f"lPoint{self._name}").get_text().strip() if self.root.offspring(f"lPoint{self._name}").exists() else None
    @property
    def notice(self):
        return self.root.offspring("sNotice") if self.root.offspring("sNotice").exists() else None
class WeaponPoint_PopupGetPoint(WeaponPoint):
    def __init__(self,node,name):
        super().__init__(node,name)
    @property
    def active_BG(self):
        return self.root.offspring("sBGActive") if self.root.offspring("sBGActive").exists() else None
    @property
    def deactive_BG(self):
        return self.root.offspring("sBGDeActive") if self.root.offspring("sBGDeActive").exists() else None
    @property
    def notice_icon(self):
        return self.deactive_BG.child("sNotice") if self.deactive_BG.child("sNotice").exists() else None
class PopupMilitaryGetPoint:
    def __init__(self,poco,type_name:Literal["Air", "Drone", "Wing", "Pilot", "Engine"]="Air"):
        self.poco = poco
        self._type_name = type_name
        self.root = self.poco("PopupMilitaryGetPoint(Clone)")
        self.btn_back = self.root.offspring("B_Back (1)")
        self.middle_panel = self.root.offspring("TopMiddle")
        self.title = self.middle_panel.offspring("title").get_text().strip() if self.middle_panel.offspring("sTitle").exists() else None
        self.generator=self.middle_panel.offspring("Generators").child(f"{type_name[0]}Generator")
        # self.items=[]
        # start_time=time.time()
        # for item in list(self.middle_panel.offspring("Grid").children())[:5]: # Limit to first 5 items for performance
        #     if type_name== "Pilot":
        #         self.items.append(PilotItem(item))
        #     else:
        #         self.items.append(HangarItem(item))
        # end_time = time.time()
        # print(f"Time taken to process Grid items: {end_time - start_time:.4f} seconds")
        self.weapon_points = []
        start_time = time.time()
        for i in range(5):
            _type = type[i]
            _name = {1: "Air", 2: "Drone", 3: "Wing", 4: "Pilot", 5: "Engine"}[i + 1]
            node = self.root.offspring(f"{_type}Point")
            if node.exists():
                self.weapon_points.append(WeaponPoint_PopupGetPoint(node, _name))
        end_time = time.time()
        print(f"Time taken to process weapon_points: {end_time - start_time:.4f} seconds")
    @property
    def items(self):
        result = []
        start_time = time.time()
        for item in list(self.middle_panel.offspring("Grid").children())[:5]:  # Limit to first 5 items for performance
            if self._type_name == "Pilot":
                result.append(PilotItem(item))
            else:
                result.append(HangarItem(item))
        end_time = time.time()
        print(f"Time taken to process Grid items: {end_time - start_time:.4f} seconds")
        return result
class HangarItem:
    def __init__(self,node):
        self.root=node
    @property
    def item_icon(self):
        return self.root.offspring("sIcon").attr("texture") if self.root.offspring("sIcon").exists() else None
    @property
    def star_text(self):
        return self.root.offspring("lStar").get_text().strip() if self.root.offspring("lStar").exists() else None
    @property
    def star_icon(self):
        return self.root.offspring("sStar")
    @property
    def cover_BG(self):
        return self.root.offspring("goCover") if self.root.offspring("goCover").exists() else None
    @property
    def lock_icon(self):
        return self.root.offspring("goLock") if self.root.offspring("goLock").exists() else None
    @property
    def point_text(self):
        return self.root.offspring("lPoint").get_text().strip() if self.root.offspring("lPoint").exists() else None
    @property
    def claimed_icon(self):
        return self.root.offspring("goClaimed") if self.root.offspring("goClaimed").exists() else None
class PilotItem(HangarItem):
    def __init__(self, node):
        super().__init__(node)
    @property
    def portrait(self):
        return self.root.offspring("sPortrait").attr("texture") if self.root.offspring("sPortrait").exists() else None
    @property
    def flag(self):
        return self.root.offspring("sNationFlag").attr("texture") if self.root.offspring(
            "sNationFlag").exists() else None
    @property
    def rarity_frame(self):
        return self.root.offspring("sFrame").attr("texture") if self.root.offspring("sFrame").exists() else None
class PopupMilitaryCareerInfo:
    def __init__(self,poco):
        self.poco=poco
        self.root = self.poco("PopupMilitaryCareerInfo(Clone)")
        self.title= self.root.offspring("sTitle")
        self.tab_rank= self.root.offspring("TabRank")
        self.tab_point= self.root.offspring("TabPoint")
        self.btn_back = self.root.offspring("B_Back")
        #tab Rank elements
        self.description= self.tab_rank.offspring("Info")
        self.rank_categories_text = [
            node.offspring("Info").get_text().strip if node.exists() else None
            for node in (self.tab_rank.offspring(f"Rank_{i}") for i in range(11))
        ]
        #tab Point elements
        self.star_point= self.tab_point.offspring("1.star point")
        self.star_point_text = self.star_point.get_text().strip() if self.star_point.exists() else None
        type= ["aircraft", "drone", "wing", "pilot", "engine"]
        self.star_points = [
            node if node.exists() else None
            for node in(self.star_point.offspring(f"{_type}")for _type in type)
        ]
        self.engine_rarity_point= self.tab_point.offspring("2.rarity point engine")
        self.engine_rarity_point_text = self.engine_rarity_point.get_text().strip() if self.engine_rarity_point.exists() else None
        rarity=["Common", "Uncommon", "Rare", "Epic", "Legendary","Immortal","Holy"]
        self.engine_rarity_points= [
            node if node.exists() else None
            for node in (self.engine_rarity_point.offspring(f"{_rarity}") for _rarity in rarity)
        ]
        self.pilot_rarity_point = self.tab_point.offspring("3.rarity point pilot")
        self.pilot_rarity_point_text = self.pilot_rarity_point.get_text().strip() if self.pilot_rarity_point.exists() else None
        pilot_rarity=["R","SR", "SSR"]
        self.pilot_rarity_points = [
            node if node.exists() else None
            for node in (self.pilot_rarity_point.offspring(f"{_rarity}") for _rarity in pilot_rarity)
        ]
        self.tab_rank_btn= self.root.offspring("BottomBtn").offspring("BtnRank")
        self.tab_point_btn = self.root.offspring("BottomBtn").offspring("BtnPoint")
    @property
    def tab_rank_active_sprite(self):
        return self.tab_rank_btn.offspring("SpriteActive") if self.tab_rank.offspring("SpriteActive").exists() else None
    @property
    def tab_rank_deactive_sprite(self):
        return self.tab_rank_btn.offspring("Sprite") if self.tab_rank.offspring("Sprite").exists() else None
    @property
    def tab_point_active_sprite(self):
        return self.tab_point_btn.offspring("SpriteActive") if self.tab_point.offspring("SpriteActive").exists() else None
    @property
    def tab_point_deactive_sprite(self):
        return self.tab_point_btn.offspring("Sprite") if self.tab_point.offspring("Sprite").exists() else None