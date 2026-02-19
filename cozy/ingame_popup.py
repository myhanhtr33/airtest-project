class PopupWin:
    def __init__(self, poco):
        self.root = poco("PopupWin")
        self.btn_next = self.root.offspring("B_Continue")
        self.btn_ads = self.root.offspring("B_Ads")
        self.gold_next= self.btn_next.offspring("Text (TMP)").get_text()
        self.gold_ads = self.btn_ads.offspring("Text (TMP) (1)").get_text()
        self.gold_multiplier= self.btn_ads.offspring("Text (TMP)").get_text() #e.g: x3
