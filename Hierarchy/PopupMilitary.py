class PopupMilitary:
    def __init__(self, poco):
        self.poco = poco
        self.root= self.poco("PopupMilitaryCareer(Clone)")
        self.btn_back = self.root.offspring("B_Back (1)")
        self.top_panel = self.root.offspring("TopDecord")
        self.title = self.top_panel.offspring("lTitle").get_text()
        self.rank_badge= self.top_panel.offspring("Spine GameObject (Career Rank)")
        self.info_btn= self.top_panel.offspring("bInfo")
        self.mid_panel = self.root.offspring("TopMiddle")
        self.mid_title = self.mid_panel.offspring("lTitle (1)").get_text()
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
            _type= {1: "Aircraft", 2: "Drone", 3: "Wing", 4: "Pilot", 5: "Engine"}[i+1]
            _name={1: "Air", 2: "Drone", 3: "Wing", 4: "Pilot", 5: "Engine"}[i+1]
            node= self.bot_panel.offspring(f"{_type}Point")
            if node.exists():
                self.weapon_points.append(WeaponPoint(node,_name))
    @property
    def level_number_text(self):
        return self.rank_badge.offspring("lLevel").get_text()
    @property
    def level_category_text(self):
        return self.rank_badge.offspring("lRank").get_text()
    @property
    def process_text(self):
        return self.bot_panel.offspring("lProcess").get_text()
    @property
    def upgrade_price_text(self):
        return self.upgrade_btn.offspring("lUpgrade").get_text()

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
        @property
        def accumulated_point(self):
            return self.root.offspring(f"lPoint{name}").get_text()
        @property
        def notice(self):
            return self.root.offspring("sNotice") if self.root.offspring("sNotice").exists() else None


