class PopupExploration:
    def __init__(self,poco):
        self.poco=poco
        self.root = poco("Popup_Exploration_Center(Clone)")
        self.btn_back = self.root.offspring("BtnBack")
        self.title= self.root.offspring("lTitle")
        self.btn_info = self.root.offspring("btnExplorationInfo")
        self.score = self.root.offspring("lResource").get_text().strip()
        self.score_icon = self.root.offspring("sResource")
        self.btn_shop = self.root.offspring("btnExplorationShop")