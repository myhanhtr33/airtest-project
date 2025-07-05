from typing import Literal
type=["Aircraft", "Drone", "Wing", "Pilot", "Engine"]
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
        self.passives=[]
        for i in range(1,7):
            node=self.mid_panel.offspring(f"Passive{i}")
            if node.exists():
                _stat = {1: "lAtk", 2: "lHP", 3: "lCritChance", 4: "lCritDamage", 5: "lBlockDamage", 6: "lReduceDamage"}[i]
                self.passives.append(Passive(node,_stat))
        self.bot_panel = self.root.offspring("TopBottom")
        self.process_fill = self.bot_panel.offspring("sFill")
        self.process_info_btn = self.bot_panel.offspring("bInfo")
        self.upgrade_btn = self.bot_panel.offspring("BtnUpdate")
        self.weapon_points = []
        for i in range(5):
            _type= type[i]
            _name={1: "Air", 2: "Drone", 3: "Wing", 4: "Pilot", 5: "Engine"}[i+1]
            node= self.bot_panel.offspring(f"{_type}Point")
            if node.exists():
                self.weapon_points.append(WeaponPoint(node,_name))
    @property
    def level_number_text(self):
        return self.rank_badge.offspring("lLevel").get_text() if self.rank_badge.offspring("lLevel").exists() else None
    @property
    def level_category_text(self):
        return self.top_panel.offspring("lRank").get_text() if self.top_panel.offspring("lRank").exists() else None
    @property
    def process_text(self):
        return self.bot_panel.offspring("lProcess").get_text() if self.bot_panel.offspring("lProcess").exists() else None
    @property
    def upgrade_price_text(self):
        return self.upgrade_btn.offspring("lUpgrade").get_text() if self.upgrade_btn.offspring("lUpgrade").exists() else None

class Passive:
    def __init__(self,node,stat):
        self.root= node
        self.sprite = self.root.offspring("sPassive")
        self.passive_stat_text= self.root.offspring(stat).get_text()
class WeaponPoint:
    def __init__(self,node,name):
        self.root= node
        self.icon = self.root.offspring("sIcon")
        self.name= self.root.offspring(f"l{name}").get_text()
        self._name = name
    @property
    def accumulated_point(self):
        return self.root.offspring(f"lPoint{self._name}").get_text()
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
        self.root = self.poco("PopupMilitaryGetPoint(Clone)")
        self.btn_back = self.root.offspring("B_Back (1)")
        self.middle_panel = self.root.offspring("TopMiddle")
        self.title = self.middle_panel.offspring("sTitle").get_text() if self.middle_panel.offspring("sTitle").exists() else None
        self.generator=self.middle_panel.offspring("Generator").child(f"{type_name[0]}Generator")
        self.items=[]
        for item in self.middle_panel.offspring("Grid").children():
            if type_name== "Pilot":
                self.items.append(PilotItem(item))
            else:
                self.items.append(HangarItem(item))
        self.weapon_points = []
        for i in range(5):
            _type = type[i]
            _name = {1: "Air", 2: "Drone", 3: "Wing", 4: "Pilot", 5: "Engine"}[i + 1]
            node = self.root.offspring(f"{_type}Point")
            if node.exists():
                self.weapon_points.append(WeaponPoint_PopupGetPoint(node, _name))
class HangarItem:
    def __init__(self,node):
        self.root=node
        self.item_icon= self.root.offspring("sIcon").attr("texture") if self.root.offspring("sIcon").exists() else None
        self.star_text = self.root.offspring("lStar").get_text() if self.root.offspring("lStar").exists() else None
        self.star_icon= self.root.offspring("sStar")
        self.cover_BG = self.root.offspring("goCover") if self.root.offspring("goCover").exists() else None
        self.lock_icon= self.root.offspring("goLock") if self.root.offspring("goLock").exists() else None
    @property
    def point_text(self):
        return self.root.offspring("lPoint").get_text() if self.root.offspring("lPoint").exists() else None
class PilotItem(HangarItem):
    def __init__(self,node):
        super().__init__(node)
        self.portrait = self.root.offspring("sPortrait").attr("texture") if self.root.offspring("sPortrait").exists() else None
        self.flag= self.root.offspring("sNationFlag").attr("texture") if self.root.offspring("sNationFlag").exists() else None
        self.rarity_frame = self.root.offspring("sFrame").attr("texture") if self.root.offspring("sFrame").exists() else None