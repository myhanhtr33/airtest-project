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
    def collected_gold_text(self):
        node = self.root.offspring("l_Coin")
        return int(node.get_text().strip()) if node.exists() else None
    @property
    def collected_gem_text(self):
        node = self.root.offspring("l_Gem")
        return node.get_text().strip() if node.exists() else None
    @property
    def collected_weekly_medal_text(self):
        node = self.root.offspring("l_WeeklyEvent")
        return node.get_text().strip() if node.exists() else None

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
        return self.root.offspring("B_Next")

class PopupGameLose(PopupGameResult):
    def __init__(self, poco):
        super().__init__(poco, "PopupGameLose(Clone)")

class PopupGameWin(PopupGameResult):
    def __init__(self, poco):
        super().__init__(poco, "PopupGameComplete(Clone)")
