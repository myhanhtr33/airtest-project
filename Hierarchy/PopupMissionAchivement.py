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
        node= self.root.child("Achievement")
        return AchievementTab(node)
    @property
    def battle_pass_panel(self):
        node = self.root.child("Pass")
        return BattlePassPanel(node)

class DailyTab:
    def __init__(self,node):
        self.root = node
        self.title = self.root.offspring("Title").get_text() #Daily mission
        self.swap_text = self.root.offspring("lSub").get_text().strip() #Complete daily quests and get rewards
    @property
    def btn_swap(self): #there is 2 times swap, btn disappear when run out of 2 times
        node = self.root.offspring("btnSwap")
        return node if node.exists() else None
    @property
    def progress_score(self):
        return self.root.offspring("progress").offspring("lMark").get_text().strip()
    @property
    def progress_fill(self):
        return self.root.offspring("progress").offspring("fill")
    @property
    def progress_rewards(self):
        return [
            ProgressReward(self.root.offspring("progress").offspring("reward")),
            ProgressReward(self.root.offspring("progress").offspring("reward (1)")),
            ProgressReward(self.root.offspring("progress").offspring("reward (2)")),
        ]
    @property
    def daily_missions(self):
        return [MissionItem(node) for node in self.root.offspring("ScrollView").children()]

class WeeklyTab:
    def __init__(self,node):
        self.root = node
        self.title = self.root.offspring("Title").get_text().strip() #Weekly mission
    @property
    def weekly_missions(self):
        return [MissionItem(node) for node in self.root.offspring("ScrollView").children()]

class AchievementTab:
    def __init__(self,node):
        self.root = node
class BattlePassPanel:
    def __init__(self,node):
        self.root= node
        self.title = self.root.offspring("lPassName").get_text().strip() #Battle Pass
        self.progress_fill= self.root.offspring("fill")
        self.level=self.root.offspring("lTier").get_text().strip()  # 0->45
        self.progress_text = self.root.offspring("lProgess").get_text().strip() # x/100

class ProgressReward:
    def __init__(self,node):
        self.root = node
        self.box_icon= self.root.offspring("sIcon").attr("texture") # sprite contains "UI5_Pack_Art_Daily"
        node=self.root.offspring("tick")
        self.claimed_icon= node if node.exists() else None
class MissionItem:
    def __init__(self,node):
        self.root=node
        self.name = self.root.offspring("lName").get_text().strip()
        self.icon= self.root.offspring("sIcon")
        self.progress_bar = self.root.offspring("sfill")
        self.progress_text= self.root.offspring("lProgress").get_text().strip() #x/y
        self.rewards=[
            MissionReward(self.root.offspring("reward")),
            MissionReward(self.root.offspring("reward (1)")),
            MissionReward(self.root.offspring("reward (2)")),
        ]
class MissionReward:
    #dailyreward: 3 gem, 2400 gold, 50 battle pass points
    #weeklyreward: 15 gem, 5500 gold, 250 battle pass points
    def __init__(self,node):
        self.root = node if node.exists() else None
        self.reward_icon = self.root.offspring("sIcon").attr("texture")
        self.reward_amount= self.root.child("lCount").get_text().strip()




