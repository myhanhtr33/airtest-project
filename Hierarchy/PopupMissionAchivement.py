class UIButtonUtils:
    @staticmethod
    def check_sprite_state(btn, expected_active):
        active_node= btn.offspring("Active")
        active_sprite= active_node if active_node.exists() else None
        deactive_node = btn.offspring("Deactive")
        deactive_sprite = deactive_node if deactive_node.exists() else None
        if expected_active:
            return active_sprite and not deactive_sprite
        else:
            return deactive_sprite and not active_sprite

    @staticmethod
    def check_sprite_btn_active(btn):
        return UIButtonUtils.check_sprite_state(btn, True)

    @staticmethod
    def check_sprite_btn_deactive(btn):
        return UIButtonUtils.check_sprite_state(btn, False)

class PopupMissionAchivement:
    def __init__(self,poco):
        self.poco = poco
        self.root = poco("Popup_MissionAchivement_2022(Clone)")
        self.btn_back = self.root.offspring("btnBack")
        self.btn_daily = self.root.offspring("btnDaily (1)")
        self.btn_weekly = self.root.offspring("btnDaily (2)")
        self.btn_achievement = self.root.offspring("btnDaily (3)")
    @property
    def daily_tab(self):
        node= self.root.child("DailyMission")
        return DailyTab(node)
    @property
    def weekly_tab(self):
        node= self.root.child("WeeklyMission")
        return WeeklyTab(node)
    @property
    def achievement_tab(self):
        node= self.root.child("Achivement")
        return AchievementTab(node)
    @property
    def battle_pass_panel(self):
        node = self.root.child("Pass")
        return BattlePassPanel(node)

class DailyTab:
    def __init__(self,node):
        self.root = node
    @property
    def title(self):
        return self.root.offspring("Title").get_text()  # Daily mission
    @property
    def swap_text(self):
        return self.root.offspring("lSub").get_text().strip()  # Complete daily quests and get rewards
    @property
    def btn_swap(self): #there is 2 times swap, btn disappear when run out of 2 times
        node = self.root.offspring("btnSwap")
        return node if node.exists() else None
    @property
    def progress_score(self): #0->5
        return self.root.offspring("progress").offspring("lMark").get_text().strip()
    @property
    def progress_fill(self):
        return self.root.offspring("progress").offspring("fill")
    @property
    def progress_rewards(self):
        return [
            ProgressReward(self.root.offspring("poses").offspring("reward"),0),
            ProgressReward(self.root.offspring("poses").offspring("reward (1)"),1),
            ProgressReward(self.root.offspring("poses").offspring("reward (2)"),2),
        ]
    @property
    def daily_missions(self):
        return [MissionItem(node) for node in self.root.offspring("Grid").children()]

class WeeklyTab:
    def __init__(self,node):
        self.root = node
        self.title = self.root.offspring("Title").get_text().strip() #Weekly mission
    @property
    def weekly_missions(self):
        return [MissionItem(node) for node in self.root.offspring("Grid").children()]

class AchievementTab:
    def __init__(self,node):
        self.root = node
        self.title = self.root.offspring("Title").get_text().strip() #Achievement
        self.description = self.root.offspring("lSub").get_text().strip()
    @property
    def achievement_missions(self):
        return [MissionItem(node) for node in self.root.offspring("Grid").children()]
class BattlePassPanel:
    def __init__(self,node):
        self.root= node
        self.title = self.root.offspring("lPassName").get_text().strip() #Battle Pass
        self.progress_fill= self.root.offspring("fill")
        self.level=self.root.offspring("lTier").get_text().strip()  # 0->45
        self.progress_text = self.root.offspring("lProgess").get_text().strip() # x/100
        self.countdown = self.root.offspring("lEndIn").get_text().strip()

class ProgressReward:
    def __init__(self,node, index=0):
        self.root = node
        self.box_icon= self.root.offspring("sIcon").attr("texture") # sprite contains "UI5_Pack_Art_Daily"
        self.index = index
    @property
    def claimed_icon(self):
        node = self.root.offspring("tick") if self.index==0 else self.root.offspring(f"tick ({self.index})")
        return node if node.exists() else None
class MissionItem:
    def __init__(self,node):
        self.root=node
    @property
    def name(self):
        node= self.root.offspring("lName")
        return node.get_text().strip()  if node.exists() else None
    @property
    def icon(self):
        return self.root.offspring("sFrame").child("sIcon")
    @property
    def progress_bar(self):
        return self.root.offspring("sfill")
    @property
    def progress_text(self): # x/y or Completed
        return self.root.offspring("lProgress").get_text().strip()
    @property
    def rewards(self): #not exists when progress_text is "Completed"
        nodes = [
            self.root.offspring("reward"),
            self.root.offspring("reward (1)"),
            self.root.offspring("reward (2)"),
        ]
        rewards = [MissionReward(node) if node.exists() else None for node in nodes]
        return rewards
    @property
    def achievement_reward(self):
        node= self.root.offspring("reward (2)")
        return MissionReward(node) if node.exists() else None
    @property
    def background(self):
        #incomplete: UI5_Target_BG_1
        #complete: UI5_Target_BG_2
        #claimed: UI5_Target_BG_3
        return self.root.offspring("sBg").attr("texture")
    @property
    def swap_BG(self): #exist only when click btn_swap in DailyTab
        return self.root.offspring("swap")
    @property
    def btn_swap(self): #exist only when click btn_swap in and mission is incomplete
        node = self.root.offspring("btnChange")
        return node if node.exists() else None

    @property
    def open_in_msg(self): #Open in 05:21:06:18, exists when name is None
        node = self.root.offspring("lMessage")
        return node.get_text().strip() if node.exists() else None
class MissionReward:
    #dailyreward: 3 gem, 2400 gold, 50 battle pass points
    #weeklyreward: 15 gem, 5500 gold, 250 battle pass points
    def __init__(self,node):
        self.root = node if node.exists() else None
        self.reward_icon = self.root.offspring("sIcon").attr("texture")
        self.reward_amount= self.root.child("lCount").get_text().strip()

class InfoBox:
    def __init__(self,poco):
        self.poco = poco
        self.root = poco("Popup_Info_Box(Clone)")
        title_node= self.root.offspring("lChestName")
        self.title = title_node.get_text() if title_node.exists() else None
        self.rewards = self.root.offspring("Grid").children()

class TierUpPopup:
    def __init__(self,poco):
        self.poco = poco
        self.root = poco("Popup_HBP_TierUp(Clone)")
        self.btn_go_to_BP = self.root.offspring("bGotoPass")
        self.btn_close = self.root.offspring("bClose")
    @property
    def level(self):
        node=self.root.offspring("lNumberTierUp")
        return node.get_text().strip() if node.exists() else None
#poco("Popup_HBP_Home(Clone)")


