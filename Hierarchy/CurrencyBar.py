from poco.drivers.unity3d import UnityPoco

class CurrencyBar:
    def __init__(self, poco):
        self.poco = poco
        self.root = poco("CurrencyBar")
        self.gold_home = gold_home(self.root)
        self.energy_home = energy_home(self.root)
        self.gem_home = gem_home(self.root)
        self.video_home= video_home(self.root)

class gold_home:
    def __init__(self,parent):
        self.root = parent.offspring("Gold_Home")
    def gold_icon(self):
        return self.root.child("IconGold")
    def gold_plus_btn(self):
        return self.root.child("IconPlus")
    def gold_amount(self):
        return self.root.child("lGold")

class energy_home:
    def __init__(self,parent):
        self.root = parent.offspring("Energy_Home")
    def energy_icon(self):
        return self.root.child("IconGold")
    def energy_plus_btn(self):
        return self.root.child("IconPlus")
    def energy_amount(self):
        return self.root.child("lEnergy")

class gem_home:
    def __init__(self, parent):
        self.root = parent.offspring("Gem_Home")
    def gem_icon(self):
        return self.root.child("IconGold")
    def gem_plus_btn(self):
        return self.root.child("IconPlus")
    def gem_amount(self):
        return self.root.child("lGem")

class video_home:
    def __init__(self, parent):
        self.root = parent.offspring("VideoReward_Home")
    def video_icon(self):
        return self.root.child("Icon")

