import time

from utils.get_resource_amount import clean_number
import os
from airtest.core.api import Template
current_dir = os.path.dirname(os.path.abspath(__file__))
EndGameVideo_icon_path= os.path.join(os.path.dirname(current_dir), "image","UI_ingame", "EndGameVideo_icon.png")

class UI_Ingame:
    def __init__(self, poco):
        self.root = poco("UI INGAME (1)")
    @property
    def btn_pause(self):
        return self.root.offspring("btn_Pause")
    @property
    def btn_wing_skill(self):
        return self.root.offspring("btn_WingSkill")
    @property
    def wing_skill_amount(self):
        return self.root.offspring("btn_WingSkill").offspring("l_NumWingSkill")
    @property
    def btn_plane_skill(self):
        return self.root.offspring("btn_ActiveSkill")
    @property
    def plane_skill_amount(self):
        return self.root.offspring("btn_ActiveSkill").offspring("l_NumActiveSkill")
    @property
    def btn_switch_squad(self):
        return self.root.offspring("btn_Switch")
    @property
    def survive_stat(self):
        node= self.root.offspring("NumWaveSurvive")
        return node.get_text().strip() if node.exists() else None
    @property
    def survive_panels(self):
        panels= []
        for i in range(1,4):
            panel_node=self.root.offspring("panelItemBonus").offspring(f"Item{i}")
            panels.append(SurvivePanel(panel_node))
        return panels

class SurvivePanel:
    def __init__(self,root):
        self.root= root if root.exists() else None
    @property
    def title(self):
        node=self.root.offspring("lLabelTitle")
        return node.get_text().strip() if node.exists() else None
    @property
    def description(self):
        node=self.root.offspring("lLabelDescription")
        return node.get_text().strip() if node.exists() else None

class UITop:
    def __init__(self, poco):
        self.root = poco("UI_INGAME_TOP")
    @property
    def hp_text(self):
        return self.root.offspring("l_Life")
    @property
    def hp_fill(self):
        return self.root.offspring("sHpFill")
    @property
    def shield_fill(self):
        return self.root.offspring("sShieldFill")
    @property
    def current_squad_sprite(self):
        return self.root.offspring("sSquadCurrent")
    @property
    def squad_elements(self):
        nodes = [
            self.root.offspring("Element1"),
            self.root.offspring("Element2"),
            self.root.offspring("Element3"),
        ]
        return [node if node.exists() else None for node in nodes]
    @property
    def killed_enemies_percentage(self): #campaign, 63%
        node= self.root.offspring("lNumberPercent")
        if node.exists():
            percent = node.get_text().strip().replace("%","")
            return int(percent)
        else:
            return None
    @property
    def collected_gold(self):
        node = self.root.offspring("l_Coin")
        return clean_number(node.get_text().strip()) if node.exists() else None
    @property
    def collected_gem(self):
        node = self.root.offspring("l_Gem")
        return clean_number(node.get_text().strip()) if node.exists() else None
    @property
    def collected_weekly_medal(self):
        node = self.root.offspring("l_WeeklyEvent")
        print("collected_weekly_medal text:", node.get_text().strip())
        return clean_number(node.get_text().strip()) if node.exists() else None

    def get_current_hp(self) -> int:
        import re
        text = self.hp_text.get_text()
        match = re.match(r'([\d,]+) \((\d+)%\)', text)
        if match:
            return int(match.group(1).replace(',', ''))
        return 0
    def get_current_hp_percentage(self) -> int:
        import re
        text = self.hp_text.get_text()
        match = re.match(r'([\d,]+) \((\d+)%\)', text)
        if match:
            return int(match.group(2))
        return 0

class PausePopup:
    def __init__(self, poco):
        self.root = poco("Popup_Pause(Clone)")
    @property
    def btn_resume(self):
        return self.root.offspring("B_Continue")
    @property
    def btn_restart(self):
        return self.root.offspring("B_ReStart (2)")
    @property
    def btn_back(self):
        return self.root.offspring("B_Back")

class RevivalPopup:
    def __init__(self, poco):
        self.root = poco("PopupRevival(Clone)")
    @property
    def btn_gem(self):
        return self.root.offspring("B_UseGem")
    @property
    def btn_ads(self):
        return self.root.offspring("B_ViewAds")
    @property
    def btn_next(self): #to popup select level
        return self.root.offspring("B_ReStart")
    @property
    def gem_amount(self):
        return int(self.root.offspring("numGem").get_text().strip())

class EndGameVideoPopup:
    def __init__(self, poco):
        root=poco("PopupEndGameVideo(Clone)")
        self.root = root if root.exists() else None
        # self.root= poco("PopupEndGameVideo(Clone)")
    @property
    def tap_close_text(self):
        return self.root.offspring("lTapClose")
    @property
    def btn_watch_video(self):
        return self.root.offspring("B_WatchVideo")
    @property
    def icon_template(self):
        return Template(EndGameVideo_icon_path)

class PopupRate:
    def __init__(self,poco):
        root=poco("PopupRate(Clone)")
        self.root= root if root.exists() else None
    @property
    def btn_back(self):
        return self.root.offspring("BtnBack")
    @property
    def btn_rate_1to4(self):
        return self.root.offspring("Btn1_4Stars")
    @property
    def btn_rate_5(self):
        return self.root.offspring("Btn5Stars")

class CurrencyBarIngame:
    def __init__(self, poco):
        self.root = poco("CurrencyBarInGame")
    @property
    def btn_ads(self):
        return self.root.offspring("BtnVideoAds")
    @property
    def gold_amount(self):
        node = self.root.offspring("lGold")
        return clean_number(node.get_text().strip()) if node.exists() else None
    @property
    def gem_amount(self):
        node = self.root.offspring("lGem")
        return clean_number(node.get_text().strip()) if node.exists() else None
    @property
    def energy_amount(self):
        node = self.root.offspring("lEnergy")
        return clean_number(node.get_text().strip()) if node.exists() else None

class PopupGameResult:
    """Base class for game result popups with common properties."""
    def __init__(self, poco, root_selector):
        self.root = poco(root_selector)
    @property
    def level_text(self):
        node = self.root.offspring("L_NumLevel")
        return node.get_text().strip() if node.exists() else None
    @property
    def mode_text(self):
        node = self.root.offspring("L_Mode")
        return node.get_text().strip() if node.exists() else None
    @property
    def result(self):
        node = self.root.offspring("L_Result")
        return node.get_text().strip() if node.exists() else None
    @property
    def gold_text(self):
        node = self.root.offspring("L_NumCoin")
        return node.get_text().strip() if node.exists() else None
    @property
    def collected_gold_amount(self) -> int:
        """Extract the base collected gold amount (before bonus)."""
        import re
        text = self.gold_text
        if not text:
            return 0
        match = re.match(r'([\d,]+)', text)
        if match:
            return clean_number(match.group(1).replace(',', ''))
        return 0
    @property
    def bonus_gold_amount(self) -> int:
        """Extract the bonus gold amount from parentheses."""
        import re
        text = self.gold_text
        if not text:
            return 0
        match = re.search(r'\(\+?([\d,]+)\)', text)
        if match:
            return clean_number(match.group(1))
        return 0
    @property
    def gold_limit_text(self):
        node = self.root.offspring("L_NumCoinLimit")
        return node.get_text().strip() if node.exists() else None
    @property
    def btn_ads(self):
        return self.root.offspring("B_X2Gold (1)")
    @property
    def btn_next(self):
        tmp= self.root.offspring("B_NextLevel")
        return tmp if tmp.exists() else None
    @property
    def btn_back(self):
        tmp= self.root.offspring("B_Back")
        return tmp if tmp.exists() else None

class PopupGameLose(PopupGameResult):
    def __init__(self, poco):
        super().__init__(poco, "PopupGameLose(Clone)")

class PopupGameWin(PopupGameResult):
    def __init__(self, poco):
        super().__init__(poco, "PopupGameComplete(Clone)")

class LevelManager:
    def __init__(self, poco):
        self.root = poco("LevelManager")
    @property
    def waves(self):
        return self.root.children()
    def wave_count(self):
        return len(self.waves)
    def is_rescue_levelmanager(self):
        rescue_waves= []
        for wave in self.waves:
            if "rescue" in wave.attr("name").lower():
                rescue_waves.append(wave)
        if len(rescue_waves) !=3:
            print(f"rescue wave count not 3, found: {len(rescue_waves)}")
            return False
        rescue_objs=0
        for w in rescue_waves:
            objs=w.children()
            for obj in objs:
                if "PilotRescue" in obj.attr("name"):
                    rescue_objs+=1
                    print(f"found pilot rescue obj: {obj.attr('name')}")
        if rescue_objs==3:
            return True
        print(f"rescue obj count not 3, found: {rescue_objs}")
        return False
    def is_survival_levelmanager(self):
        if self.wave_count() ==10:
            return True
        return False



