class PopupExploration:
    def __init__(self,poco):
        self.poco=poco
        self.root = poco("Popup_Exploration_Center(Clone)")
    @property
    def btn_back(self):
        return self.root.offspring("BtnBack")
    @property
    def title(self):
        return self.root.offspring("lTitle")
    @property
    def btn_info(self):
        return self.root.offspring("btnExplorationInfo")
    @property
    def score(self):
        return self.root.offspring("lResource").get_text().strip()
    @property
    def score_icon(self):
        return self.root.offspring("sResource")
    @property
    def btn_shop(self):
        return self.root.offspring("btnExplorationShop")
    @property
    def btn_level(self):
        return self.root.offspring("btnExplorationLevel")
    @property
    def level_sprite(self):
        return self.btn_level.child("Sprite").attr("texture")
    @property
    def energy(self):
        return self.root.offspring("lText").get_text().strip()
    @property
    def energy_icon(self):
        return self.root.offspring("sEnergy")
    @property
    def solar_system(self):
        nodes = ["Sun", "sArrow", "Mercury", "Venus", "Earth",
                 "Mars", "Jupiter", "Saturn", "Uranus", "Neptune", "Pluto"]
        return [self.root.offspring(name) for name in nodes]
    @property
    def missions(self):
        return [Mission(self.root.offspring(f"Mission(Clone)00{i}")) for i in range(1, 8)]
    @property
    def btn_requested(self):
        return self.root.offspring("btnRequest")
    @property
    def btn_invitation(self):
        return self.root.offspring("btnInvitation")
    @property
    def reward_panel(self):
        node = self.root.offspring("panelMissionDetail").child("Reward")
        return RewardPanel(node) if node.exists() else None
    @property
    def mission_panel(self):
        node = self.root.offspring("panelMissionDetail").child("Mission")
        return MissionPanel(node) if node.exists() else None

class Mission:
    def __init__(self,node):
        self.root = node
        self.rank_sprite = node.offspring("R1")
        self.status= node.offspring("lStatus").get_text().strip()
class RewardPanel:
    def __init__(self,node):
        self.root = node
        self.btn_claim = node.offspring("btnClaim")
        self.group_rewards = node.offspring("GroupReward")
class MissionPanel:
    def __init__(self,node):
        self.root = node
    @property
    def aircraft_btn(self):
        return self.root.offspring("Aircraft (0)")
    @property
    def aircraft_star_numb(self):
        tmp = self.root.offspring("lNumberStar")
        return tmp.get_text().strip() if tmp.exists() else None
    @property
    def aircraft_star_icon(self):
        tmp = self.root.offspring("sStar")
        return tmp.attr("texture") if tmp.exists() else None
    @property
    def aircraft_plus_icon(self): # not added aircraft
        return self.root.offspring("sPlus")
    @property
    def aircraft_lock_icon(self): # aircraft added and mission already started
        return self.root.offspring("sLock")
    @property
    def aircraft_icon(self): # aircraft added
        return self.root.offspring("sAircraft")
    @property
    def group_rewards(self):
        return self.root.offspring("GroupReward")
    @property
    def start_button(self): # not started mission
        tmp = self.root.offspring("btnStart")
        return StartButton(tmp) if tmp.exists() else None
    @property
    def exploring_button(self): # mission started
        tmp = self.root.offspring("btnExploring")
        return ExploringBtn(tmp) if tmp.exists() else None
class StartButton:
    def __init__(self, node):
        self.root = node
    @property
    def texture(self):
        bg = self.root.child("bg (0)")
        return bg.attr("texture") if bg.exists() else None  # UI5_Exp_Btn_Grey, "UI5_Exp_Btn_Yellow"
    @property
    def time(self):
        time_node = self.root.child("lTime")
        return time_node.get_text().strip() if time_node.exists() else None  # 00:20:05
    @property
    def text(self):
        start_node = self.root.child("lStart")
        return start_node.get_text().strip() if start_node.exists() else None  # Start
    @property
    def energy_cost(self):
        return self.root.child("sEnergy")
class ExploringBtn:
    def __init__(self, node):
        self.root = node
    @property
    def text(self):
        node = self.root.child("lExploring")
        return node.get_text().strip() if node.exists() else None  # Exploring
    @property
    def time(self):
        node = self.root.child("lTime")
        return node.get_text().strip() if node.exists() else None  # 00:20:05

class PopupExplorationInfo:
    def __init__(self, poco):
        self.poco = poco
        self.root = poco("Popup_Exploration_CenterInfo(Clone)")
        self.btn_back = self.root.offspring("BtnBack")
        self.title = self.root.offspring("lTitle")
        self.description = self.root.offspring("lDescription").get_text().strip()
        self.rule = self.root.offspring("GroupRule")
class PopupExplorationLevelInfo:
    def __init__(self, poco):
        self.poco = poco
        self.root = poco("Popup_Exploration_LevelInfo(Clone)")
        self.btn_back = self.root.offspring("BtnBack")
        self.title = self.root.offspring("lTitle")
        self.current_level_group = self.root.offspring("Level (0)")
        self.next_level_group = self.root.offspring("Level (1)")
        self.requirement_grid = self.root.offspring("Grid")
class PopupInvitation:
    def __init__(self, poco):
        self.poco = poco
        self.root = poco("Popup_Exploration_MyInvitation(Clone)")
        self.btn_back = self.root.offspring("BtnBack")
        self.title = self.root.offspring("lTitle")
        self.description = self.root.offspring("lText (1)").get_text().strip()
        self.score = self.root.offspring("lPoint")
        self.invitation_amount = self.root.offspring("lInvitationOnMax")
class PopupExplorationShop:
    def __init__(self, poco):
        self.poco = poco
        self.root = poco("Popup_Exploration_Shop(Clone)")
        self.btn_back = self.root.offspring("BtnBack")
        self.title = self.root.offspring("sTitle (1)")
        self.description = self.root.offspring("lDesception (1)").get_text().strip()
        self.daily_shop = self.root.offspring("Shop (1)")
        self.daily_shop_title = self.daily_shop.offspring("lTitle")
        self.daily_shop_items = [
            ItemShop(self.daily_shop.offspring("ElementPack" if i == 0 else f"ElementPack ({i})"))
            for i in range(0, 3)
        ]
        self.weekly_shop = self.root.offspring("Shop (2)")
        self.weekly_shop_title = self.weekly_shop.offspring("lTitle")
        self.weekly_shop_items = [
            ItemShop(self.weekly_shop.offspring(f"ElementPack ({i})")) for i in range(3, 6)
        ]
        self.monthly_shop = self.root.offspring("Shop (3)")
        self.monthly_shop_title = self.monthly_shop.offspring("lTitle")
        self.monthly_shop_items = [
            ItemShop(self.monthly_shop.offspring(f"ElementPack ({i})")) for i in range(6, 9)
        ]
class ItemShop:
    def __init__(self, node):
        self.root = node
    @property
    def icon(self):
        return self.root.offspring("sIcon")
    @property
    def amount(self):
        tmp = self.root.offspring("lAmount")
        return tmp.get_text().strip() if tmp.exists() else None
    @property
    def btn_buy(self):
        return self.root.offspring("btnBuy")
    @property
    def btn_buy_price(self):
        tmp = self.root.offspring("lPrice")
        return tmp.get_text().strip() if tmp.exists() else None
    @property
    def btn_buy_price_icon(self):
        btn = self.btn_buy
        return btn.child("sIcon") if btn.exists() else None
    @property
    def time_buy(self):
        tmp = self.root.offspring("lTime")
        return tmp.get_text().strip() if tmp.exists() else None