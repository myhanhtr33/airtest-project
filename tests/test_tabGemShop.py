import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")
# from Hierarchy.tabGemShop import *
from Hierarchy.TabShopNavigator import *
from airtest.core.api import *
from utils.device_setup import PocoManager
from base.baseTest import BaseTest
from poco.drivers.unity3d import UnityPoco



class TestTabGemShop(BaseTest):
    def __init__(self):
        super().__init__()

        # Ensure we're on the home screen and open the shop
        if not self.poco("TabNavigator").offspring("BtnShop").exists():
            self.back_to_home()  # Your own method to navigate to home

        self.poco("TabNavigator").offspring("BtnShop").click()
        self.shop_navigator = TabShopNavigator(self.poco)
        self.gem_shop = self.shop_navigator.tabGemShop()

    def test_gem_shop_items_exist(self):
        gem_items = self.gem_shop.gemShop()
        for item in gem_items:
            print(item)
        assert len(gem_items) > 0, "No gem items found in the shop"

    def test_each_gem_item_elements(self):
        gem_items = self.gem_shop.gemShop()
        assert gem_items, "No gem items found to test"

        item = gem_items[0]
        assert item.gem_sprite().exists(), "Gem sprite not found"
        assert item.gem_icon().exists(), "Gem icon not found"
        assert item.gem_amount().exists(), "Gem amount not found"
        assert item.buy_btn().exists(), "Buy button not found"
        assert item.buy_btn_price().exists(), "Buy price not found"
        assert item.vip_icon().exists(), "VIP icon not found"

    def test_energy_items_exist(self):
        energy_items = self.gem_shop.energyShop()
        assert len(energy_items) > 0, "No energy items found in the shop"

    def test_gold_items_exist(self):
        gold_items = self.gem_shop.goldShop()
        assert len(gold_items) > 0, "No gold items found in the shop"

    def run_all(self):
        print("🔍 Running test_gem_shop_items_exist...")
        self.test_gem_shop_items_exist()
        print("✅ Passed test_gem_shop_items_exist")

        print("🔍 Running test_each_gem_item_elements...")
        self.test_each_gem_item_elements()
        print("✅ Passed test_each_gem_item_elements")

        print("🔍 Running test_energy_items_exist...")
        self.test_energy_items_exist()
        print("✅ Passed test_energy_items_exist")

        print("🔍 Running test_gold_items_exist...")
        self.test_gold_items_exist()
        print("✅ Passed test_gold_items_exist")

if __name__ == "__main__":
    test = TestTabGemShop()
    test.run_all()
    print("🎉 All Tab Gem Shop tests passed!")
