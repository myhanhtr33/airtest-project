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
        node= self.root.offspring("l_KilledEnemyPercentage")
        return node.get_text().strip() if node.exists() else None
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
        self.root = poco("Popup_Revival(Clone)")
    @property
    def btn_gem(self):
        return self.root.offspring("B_UseGem")
    @property
    def btn_ads(self):
        return self.root.offspring("B_ViewAds")
    @property
    def btn_next(self): #to popup select level
        return self.root.offspring("B_ReStart")

class EndGameVideoPopup:
    def __init__(self, poco):
        self.root = poco("PopupEndGameVideo(Clone)")
    @property
    def tap_close_text(self):
        return self.root.offspring("lTapClose")
    @property
    def btn_watch_video(self):
        return self.root.offspring("B_WatchVideo")
    @property
    def icon_template(self):
        return Template(EndGameVideo_icon_path)

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
