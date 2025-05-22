from poco.drivers.unity3d import UnityPoco

class PopupSpecialVideo:
    def __init__(self, poco):
        self.poco = poco
        self.root = poco("PopupSpecialVideoReward(Clone)")
        self.title= self.root.offspring("sTitle")
        self.description = self.root.offspring("lVideoReward")
        self.offer_wall= self.root.offspring("OfferWall")
        self.countdown= self.root.offspring("lNextVideo")
        self.popup_video_info= popup_video_info(self.poco)
        self.random_video= RandomVideo(self.root)
        self.gold_video= GoldVideo(self.root)
        self.gem_video= GemVideo(self.root)
        self.card_video= CardVideo(self.root)
        self.energy_video= EnergyVideo(self.root)
        self.back_btn= self.root.child("sBottom").child("B_Back")

class BaseVideo:
    def __init__(self, parent, video_type):
        self.root = parent.offspring(video_type)
        self.label_up_to = self.root.child("lUpTo") if self.root.child("lUpTo").exists() else None
        self.watch_btn = self.root.child("B_Watch") if self.root.child("B_Watch").exists() else None
        self.deactivate_watch_btn = self.root.child("B_WatchDeactive") if self.root.child("B_WatchDeactive").exists() else None
        self.watch_numb = self.root.child("lRate") if self.root.child("lRate").exists() else None
        self.royal_icon= self.root.offspring("sIconRoyalty") if self.root.child("sIconRoyalty").exists() else None
        self.reward_img= self.root

class RandomVideo(BaseVideo):
    def __init__(self, parent):
        super().__init__(parent, "sRandom")
        self.reward_img= self.root.child("sReward")
    def info_btn(self):
        return self.root.child("BInfo")

class GoldVideo(BaseVideo):
    def __init__(self, parent):
        super().__init__(parent, "sGoldNew")
        self.reward_img = self.root.child("sGold")

class GemVideo(BaseVideo):
    def __init__(self, parent):
        super().__init__(parent, "sGemNew")
        self.reward_img = self.root.child("sGem")

class CardVideo(BaseVideo):
    def __init__(self, parent):
        super().__init__(parent, "sCardNew")
        self.reward_img = self.root.child("sCard")

class EnergyVideo(BaseVideo):
    def __init__(self, parent):
        super().__init__(parent, "sEnergyNew")
        self.reward_img = self.root.child("sEnergy")

class popup_video_info:
    def __init__(self, parent):
        self.root = parent("PopupVideoReward(Clone)")
        self.icon_gold = self.root.offspring("sIconGold")
        self.icon_gem = self.root.offspring("sIconGem")
        self.icon_card = self.root.offspring("sIconCard")
        self.icon_life = self.root.offspring("sIconLife")
        self.icon_power = self.root.offspring("sIconPower")
        self.icon_power_duplicate = self.root.offspring("sIconPower (1)")
        self.icon_energy = self.root.offspring("sIconEnergy")
        self.btn_back = self.root.offspring("B_Back")



