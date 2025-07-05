from poco.drivers.unity3d import UnityPoco

class tabGemShop:
    def __init__(self,root):
        self.root=root
        print("___init__ tabGemShop")
        self.list_element=self.root.child("Scroll View").child("listItem")
        print("list_element:"+str(self.list_element))
        for item in self.list_element.children():
            print("item:"+item.get_name())
    def gemShop(self):
        return [itemGemShop(item) for item in self.list_element.children() if "ItemGemShop" in item.get_name()]
    def energyShop(self):
        return [itemEnergyShop(item) for item in self.list_element.children() if "ItemEnergyShop" in item.get_name()]
    def goldShop(self):
        return [itemGoldShop(item) for item in self.list_element.children() if "ItemGoldShop" in item.get_name()]

class itemGemShop:
    def __init__(self,root):
        self.root=root
    def gem_sprite(self):
        return self.root.child("sItem")
    def gem_icon(self):
        return self.root.offspring("sGem")
    def gem_amount(self):
        return self.root.offspring("lReward")
    def buy_btn(self):
        return self.root.child("BtnBuy")
    def buy_btn_price(self):
        return self.buy_btn.offspring("lPrice")
    def buy_btn_oldPrice(self):
        return self.buy_btn.offspring("lOldPrice")
    def vip_text(self):
        return self.root.offspring("lVipPoint")
    def vip_icon(self):
        return self.root.offspring("sIcon")

class itemEnergyShop:
    def __init__(self,root):
        self.root=root
    def energy_sprite(self):
        return self.root.child("sItem")
    def energy_icon(self):
        return self.root.offspring("sEnergy")
    def energy_amount(self):
        return self.root.offspring("lReward")
    def exchange_btn(self):
        return self.root.child("BtnExchange")
    def exchange_btn_price(self):
        return self.exchange_btn.offspring("lPrice")
    def exchange_btn_gemIcon(self):
        return self.exchange_btn.offspring("sGem")

class itemGoldShop:
    def __init__(self,root):
        self.root=root
    def gold_sprite(self):
        return self.root.child("sItem")
    def gold_icon(self):
        return self.root.offspring("sGold")
    def gold_amount(self):
        return self.root.offspring("lReward")
    def exchange_btn(self):
        return self.root.child("BtnExchange")
    def exchange_btn_price(self):
        return self.exchange_btn().offspring("lPrice")
    def exchange_btn_gemIcon(self):
        return self.exchange_btn().offspring("sGem")