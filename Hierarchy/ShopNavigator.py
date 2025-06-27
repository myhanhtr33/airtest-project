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
        if self._gem_shop is None and self.root.offspring("TabGemShop ").exists():
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
        self.root=parent.offspring("TabGemShop ")
        self.item_gem=[] #item_gem[0]->ItemGemShop, item_gem[1]->ItemGemShop(1), item_gem[2]->ItemGemShop(2)
        for i in range(6):
            node=self.root.offspring(f"ItemGemShop ({i})") if i>0 else self.root.offspring("ItemGemShop")
            self.item_gem.append(ItemGemShop(node))
        self.item_energy=[]
        for i in range(3):
            node=self.root.offspring(f"ItemEnergyShop ({i})") if i>0 else self.root.offspring("ItemEnergyShop")
            self.item_energy.append(ItemEnergyShop(node))
        self.item_gold=[]
        for i in range(3):
            node=self.root.offspring(f"ItemGoldShop ({i})") if i>0 else self.root.offspring("ItemGoldShop")
            self.item_gold.append(ItemGoldShop(node))

class ItemGemShop:
    def __init__(self, node):
        self.root=node
        self.gem_img=self.root.offspring("sItem")
        self.gem_icon=self.root.offspring("Reward").child("sGem")
        self.gem_amount=self.root.offspring("Reward").child("lReward")
        self.btn_buy=self.root.offspring("BtnBuy")
        self.actual_price=self.root.offspring("BtnBuy").offspring("lPrice")
        self._vip_point=self.vip_point
        self.vip_icon=self.root.offspring("sVipPoin").child("sIcon")
        self._old_price= self.old_price
    @property
    def old_price(self):
        node= self.root.offspring("OldPrice")
        return node if node.exists() else None
    @property
    def vip_point(self):
        return self.root.offspring("lVipPoint")
class ItemEnergyShop:
    def __init__(self, node):
        self.root=node
        self.energy_img=self.root.offspring("sItem")
        self.energy_icon=self.root.child("sEnergy")
        self.energy_amount=self.root.child("lReward")
        self.btn_exchange=self.root.child("BtnExchange")
        self.price=self.btn_exchange.offspring("lPrice")
        self.price_icon=self.btn_exchange.offspring("sGem")
class ItemGoldShop:
    def __init__(self, node):
        self.root=node
        self.gold_img=self.root.offspring("sItem")
        self.gold_icon=self.root.child("sGold")
        self.gold_amount=self.root.child("lReward")
        self.btn_exchange=self.root.child("BtnExchange")
        self.price=self.btn_exchange.offspring("lPrice")
        self.price_icon=self.btn_exchange.offspring("sGem")

class CardShop:
    def __init__(self, parent):
        self.root=parent.offspring("TabCardShop")
        # Day panel elements
        self.day_panel=self.root.offspring("PanelResetDay")
        self._day_countdown= self.day_countdown
        self.btn_day_reset= self.day_panel.child("B_Reset")
        self._btn_day_reset_BG= self.btn_day_reset_BG
        self.btn_day_reset_gemIcon=self.btn_day_reset.child("sGemIcon")
        self.btn_day_reset_gemPrice=self.btn_day_reset.child("lPrice")
        self.btn_day_reset_resetIcon=self.btn_day_reset.child("sRefresh")
        self._btn_day_reset_resetCount= self.btn_day_reset_resetCount
        self._day_items=self.day_items
        # Week panel elements
        self.week_panel=self.root.offspring("PanelResetWeek")
        self._week_countdown= self.week_countdown
        self.btn_week_reset= self.week_panel.child("B_Reset")
        self._btn_week_reset_BG= self.btn_week_reset_BG
        self.btn_week_reset_gemIcon=self.btn_week_reset.child("sGemIcon")
        self.btn_week_reset_gemPrice=self.btn_week_reset.child("lPrice")
        self.btn_week_reset_resetIcon=self.btn_week_reset.child("sRefresh")
        self._btn_week_reset_resetCount=self.btn_week_reset_resetCount
        self.week_items=[]
        for i in range(6,9):
            node=self.root.offspring("listItemsWeek").child(f"ItemShopSupply ({i})")
            self.week_items.append(ItemShopSupply(node))
    @property
    def day_items(self):
        self._day_items=[]
        for i in range(6):
            node=self.root.offspring("DayItems").child(f"ItemShopSupply ({i})")\
                if i>0 else self.root.offspring("DayItems").child("ItemShopSupply")
            self._day_items.append(ItemShopSupply(node))
        return self._day_items

    @property
    def day_countdown(self):
        return self.day_panel.child("lDayTime")
    @property
    def btn_day_reset_BG(self):
        return self.btn_day_reset.child("sBG")
    @property
    def btn_day_reset_resetCount(self):
        return self.btn_day_reset.child("lResetCount")
    @property
    def week_countdown(self):
        return self.week_panel.child("lWeekTime")
    @property
    def btn_week_reset_BG(self):
        return self.btn_week_reset.child("sBG")
    @property
    def btn_week_reset_resetCount(self):
        return self.btn_week_reset.child("lResetCount")

class ItemShopSupply:
    def __init__(self,node):
        self.root=node
        self._reward_img=self.reward_img
        self.reward_amount=self.root.offspring("lQuantity")
        self.btn_buy=self.root.offspring("btnBuy")
        self._active_btn_buy=None
        self._price= None
        self._price_icon=None
        self._deactive_btn_buy=None
        self._sold_out_label=None
    @property
    def reward_img(self):
        self._reward_img=self.root.offspring("sIcon")
        return self._reward_img
    @property
    def active_btn_buy(self):
        self._active_btn_buy = self.btn_buy.child("Enable") if self.btn_buy.child("Enable").exists() else None
        return self._active_btn_buy
    @property
    def price(self):
        self._price=self.btn_buy.offspring("lPrice") if self._active_btn_buy is not None else None
        return self._price
    @property
    def price_icon(self):
        self._price_icon=self.btn_buy.offspring("sGem") if self._active_btn_buy is not None else None
        return self._price_icon
    @property
    def deactive_btn_buy(self):
        self._deactive_btn_buy= self.btn_buy.child("Disable") if self.btn_buy.child("Disable").exists() else None
        return self._deactive_btn_buy
    @property
    def sold_out_label(self):
        self._sold_out_label=self.btn_buy.offspring("lNumGem") if self._deactive_btn_buy is not None else None
        return self._sold_out_label

class HotShop:
    def __init__(self, parent):
        self.root=parent.offspring("TabHotShop")
    @property
    def list(self):
        return self.root.offspring("ListElement")
    @property
    def engine_pack_panel(self):
        _engine_pack=self.list.offspring("ElementEnginePack(Clone)") if self.list.offspring("ElementEnginePack(Clone)") else None
        return _engine_pack
    @property
    def royal_pack_panel(self):
        _royal_pack=self.list.offspring("ElementRoyaltyPackVer2(Clone)") if self.list.offspring("ElementRoyaltyPackVer2(Clone)") else None
        return _royal_pack
    @property
    def boss_slayer_pack_panel(self):
        _boss_slayer_pack=self.list.offspring("ElementBossSlayerPack(Clone)") if self.list.offspring("ElementBossSlayerPack(Clone)") else None
        return _boss_slayer_pack
    @property
    def unlock_world_pack_panel(self):
        _unlock_world_pack=self.list.offspring("ElementUnlockWorldPack(Clone)") if self.list.offspring("ElementUnlockWorldPack(Clone)") else None
        return _unlock_world_pack
    @property
    def daily_pack_panel(self):
        _daily_pack=self.list.offspring("ElementDailyPack(Clone)") if self.list.offspring("ElementDailyPack(Clone)") else None
        return _daily_pack
