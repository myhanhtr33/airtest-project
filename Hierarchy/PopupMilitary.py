class PopupMilitary:
    def __init__(self, poco):
        self.poco = poco
        self.root= poco("PopupMilitaryCareer(Clone)")
        self.btn_back = self.root.offspring("B_Back (1)")
        self.top_panel = self.root.offspring("TopDecord")
        self.title = self.topPanel.offspring("lTitle")
        self.rank_badge= self.top_panel.offspring("Spine GameObject (Career Rank)")

    @property
    def level_text(self):
        return self.rank_badge.offspring("lLevel").get_text()
