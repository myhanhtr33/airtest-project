class EnginePack:
    def __init__(self, poco):
        self.poco = poco
        self.root= poco("PopupEngine3Pack(Clone)")
        self.btnBack=self.root.offspring("B_Back")
class RoyalPack:
    def __init__(self, poco):
        self.poco = poco
        # root=poco("PopupRoyaltyVer2(Clone)")
        # self.root= root if root.exists() else None
        self.root= poco("PopupRoyaltyVer2(Clone)")
    @property
    def btnBack(self):
        return self.root.offspring("B_Back")
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


class Popup_StarterPack:
    def __init__(self, poco):
        root = poco("PopupStarterPack(Clone)")
        self.root = root if root.exists() else None
    @property
    def btn_back(self):
        return self.root.offspring("BtnBack")

class Popup_VipPack:
    def __init__(self, poco):
        # root = poco("PopupVipPack(Clone)")
        # self.root = root if root.exists() else None
        self.root = poco("PopupVipPack(Clone)")
    @property
    def btn_back(self):
        return self.root.offspring("BtnBack")

class Popup_PremiumPack:
    def __init__(self, poco):
        # root = poco("PopupPremiumPack(Clone)")
        # self.root = root if root.exists() else None
        self.root = poco("PopupPremiumPack(Clone)")
    @property
    def btn_back(self):
        return self.root.offspring("BtnBack")
