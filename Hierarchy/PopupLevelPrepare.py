from utils.get_resource_amount import clean_number
class PopupLevelPrepare:
    def __init__(self, poco):
        self.root = poco("PopupLevelPrepareInfo(Clone)")
    @property
    def btn_start(self):
        return self.root.offspring("B_Start")
    @property
    def gold_reward_amount(self):
        node= self.root.offspring("panel_FirstRewards").offspring("lNumGift1")
        return clean_number(node.get_text().strip()) if node.exists() else None
    @property
    def gold_sprite(self):
        node = self.root.offspring("panel_FirstRewards").offspring("sItemGift1")
        return node.attr("texture") if node.exists() else None
    @property
    def gem_reward_amount(self):
        node = self.root.offspring("panel_FirstRewards").offspring("lNumGift2")
        return clean_number(node.get_text().strip()) if node.exists() else None
    @property
    def gem_sprite(self):
        node = self.root.offspring("panel_FirstRewards").offspring("sItemGift2")
        return node.attr("texture") if node.exists() else None
    @property
    def card_reward_amount(self):
        node = self.root.offspring("panel_FirstRewards").offspring("lNumGift3")
        return clean_number(node.get_text().strip()) if node.exists() else None
    @property
    def card_sprite(self):
        node = self.root.offspring("panel_FirstRewards").offspring("sItemGift3")
        return node.attr("texture") if node.exists() else None
    @property
    def level_number(self):
        node= self.root.offspring("L_NumLevel")
        return int(node.get_text().strip()) if node.exists() else None
