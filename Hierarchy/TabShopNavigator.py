from poco.drivers.unity3d import UnityPoco
from Hierarchy.tabCardShop import *
from Hierarchy.tabGemShop import *
from Hierarchy.tabHotShop import *

class TabShopNavigator:
    def __init__(self,poco):
        self.poco=poco
        self.root = poco("TabShopNavigator(Clone)")
        print("__init__ TabShopNavigator")

    def tabHot(self):
        return self.root.offspring("btnHot")
    def tabCard(self):
        return self.root.offspring("btnCard")
    def tabGem(self):
        return self.root.offspring("btnGem")
    def tabHotShop(self):
        return tabHotShop(self.root.child("TabHotShop"))
    def tabCardShop(self):
        return tabCardShop(self.root.child("TabCardShop"))
    def tabGemShop(self):
        print("______tabGemShop:"+str(self.root.child("TabGemShop")))
        # return tabGemShop(self.root)
        return tabGemShop(self.root.child("TabGemShop "))
    def is_tab_open(self, tab_name):
        return self.root.child(tab_name).exists()
    def open_tab(self, tab_name):
        if self.is_tab_open("TabHotShop"):
            return self.tabHotShop()
        elif self.is_tab_open("TabCardShop"):
            return self.tabCardShop()
        else:
            return self.tabGemShop() #default



