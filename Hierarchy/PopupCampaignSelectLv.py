import re
from enum import Enum
class PopupCampaignSelectLv:
    def __init__(self,poco):
        self.root= poco("PopupSelectLevelHome(Clone)")
        self.poco = poco
        self.btn_select_world = self.root.offspring("B_Worlds")
    @property
    def btn_worlds(self):
        return self.root.offspring("PanelButtonWorld").offspring("B_Worlds")
    @property
    def current_world(self):
        tmp = self.btn_worlds.offspring("lTitleWorld")
        text = re.search(r"World\s+(\d+)", tmp.get_text().strip()).group(1) if tmp.exists() else None
        print(f"current_worldcurrent_worldcurrent_worldcurrent_world:{text}")
        return text
    @property
    def mode_normal(self):
        return self.root.offspring("bNormal")
    @property
    def mode_hard(self):
        return self.root.offspring("bHard")
    @property
    def mode_hell(self):
        return self.root.offspring("bHell")
    def _scan(self, level_type= "normal"): #mode normal
        node=[]
        for tab_level in ["TabLevel1", "TabLevel2", "TabLevel3"]:
            for n in self.poco("PopupSelectLevelHome(Clone)").offspring(tab_level).children():
                if not n.attr("name"):
                    continue
                name= n.attr("name")
                norm= re.match(r"posLevel(\d+)", name)
                extra= re.match(r"posLevelExtra(\d+)", name)
                if level_type=="normal" and norm:
                    node.append(LevelItem(n))
                if level_type=="extra" and extra:
                    node.append(LevelItem(n))
                # print(f"_scan  lv:{n.attr('name')} index:{n.offspring("lLevel").get_text().strip() if n.offspring("lLevel").exists() else None}")
        # print(f"nodes found: {node}")
        return node
    @property
    def list_level_normal(self):
        normal= self._scan("normal")
        # for n in normal:
        #     print(f"normal level: {n.root.attr('name')}, index: {n.index}")
        return normal
        # return self._scan("normal")
    @property
    def list_level_extra(self):
        return self._scan("extra")
class PanelWorlds:
    def __init__(self,poco):
        self.root = poco("PanelWorldInfo")
    @property
    def title(self):
        return  self.root.offspring("lWorld")
    @property
    def list_world(self):
        return [WorldItem(node) for node in self.root.offspring("GridElement").children()]
class WorldItem:
    def __init__(self,node):
        self.root = node
    @property
    def index(self):
        tmp = self.root.offspring("lTitleWorld")
        return tmp.get_text().strip() if tmp.exists() else None
    @property
    def btn_go(self):
        return self.root.offspring("ButtonGo")

class LevelItem:
    def __init__(self,node):
        self.root = node
    @property
    def index(self):
        tmp = self.root.offspring("lLevel")
        return tmp.get_text().strip() if tmp.exists() else None
class LevelType(Enum):
    NORMAL = "normal"
    EXTRA = "extra"

