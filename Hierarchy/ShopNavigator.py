class ShopNavigator:
    def __init__(self, poco):
        self.poco = poco
        self.root= poco("TabShopNavigator(Clone)")
        self.tabHot= self.root.offspring("btnHot")
        self.tabCard= self.root.offspring("Tabs").offspring("btnCard")
        self.tabGem= self.root.offspring("Tabs").offspring("btnGem")
        self._gem_shop=None
        self._card_shop=None
        self._hot_shop=None
    @property
    def gem_shop(self):
        if self._gem_shop is None and self.root.offspring("TabGemShop").exists():
            self._gem_shop=GemShop(self.root)
        return self._gem_shop
    @property
    def card_shop(self):
        if self._card_shop is None and self.root.offspring("TabCardShop").exists():
            self._card_shop=CardShop(self.root)
        return self._card_shop
    @property
    def hot_shop(self):
        if self._hot_shop is None and self.root.offspring("TabHotShop").exists():
            self._hot_shop=HotShop(self.root)
        return self._hot_shop

class GemShop:
    def __init__(self, parent):
        self.root=parent.offspring("TabGemShop")
        self.item_gem=[] #item_gem[0]->ItemGemShop, item_gem[1]->ItemGemShop(1), item_gem[2]->ItemGemShop(2)
        for i in range(6):
            node=self.root.offspring(f"ItemGemShop ({i})") if i>0 else self.root.offspring("ItemGemShop")
            self.item_gem.append(ItemGemShop(node))


class ItemGemShop:
    def __init__(self, node):
        self.root=node
        self.gem_img=self.root.offspring("sItem")
        self.gem_icon=self.root.offspring("Reward").child("sGem")
        self.gem_amount=self.root.offspring("Reward").child("lReward")
        self.btn_buy=self.root.offspring("BtnBuy")
        self.actual_price=self.root.offspring("BtnBuy").offspring("lPrice")
        self.vip_point=self.root.offspring("lVipPoint")
        self.vip_icon=self.root.offspring("sVipPoin").child("sIcon")
        self.old_price=self.root.offspring("lOldPrice")if self.root.offspring("lOldPrice").exists() else None

class CardShop:
    def __init__(self, parent):
        self.root=parent.offspring("TabCardShop")

class HotShop:
    def __init__(self, parent):
        self.root=parent.offspring("TabHotShop")

