class EnginePack:
    def __init__(self, poco):
        self.poco = poco
        self.root= poco("PopupEngine3Pack(Clone)")
        self.btnBack=self.root.offspring("B_Back")
class RoyalPack:
    def __init__(self, poco):
        self.poco = poco
        self.root= poco("PopupRoyaltyVer2(Clone)")
        self.btnBack=self.root.offspring("B_Back")
class BossSlayerPack:
    def __init__(self, poco):
        self.poco = poco
        self.root= poco("PopupSlayerBoss(Clone)")
        self.btnBack=self.root.offspring("lTapToClose")
class DailyPack:
    def __init__(self, poco):
        self.poco = poco
        self.root= poco("PopupDailyPack(Clone)")
        self.btnBack=self.root.offspring("BtnBack")