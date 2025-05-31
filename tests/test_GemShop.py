from airtest.core.api import *
from utils import base_test
from utils.base_test import BaseTest
from Hierarchy.ShopNavigator import *
import re
from poco.drivers.android.uiautomation import AndroidUiautomationPoco
from utils.get_resource_amount import clean_number

gem_amount=[160,460,1000,2500,7000,16000]
vip_point=[2,5,10,20,50,100]
vip_point_sale=[1,2,5,10,25,50]
item_on_sale=[]

class TestGemShop(BaseTest):
    def __init__(self, shop_navigator):
        super().__init__()
        self.shop_navigator = shop_navigator

    def run_all_test(self):
        self.check_presence_all_element()
        self.check_gem_amount()
        self.get_index_item_on_sale()
        self.check_vip_point()

    def check_presence_all_element(self):
        # Test if the Gem Shop is present
        self.shop_navigator.tabGem.click(sleep_interval=1)
        assert self.shop_navigator.gem_shop.root.exists(), "Gem Shop not found!"
        for item in self.shop_navigator.gem_shop.item_gem:
            print(f"checking item: {item.root.get_name()}")
            assert item.gem_img.exists(), "Gem image not found!"
            assert item.gem_icon.exists(), "Gem icon not found!"
            assert item.gem_amount.exists(), "Gem amount not found!"
            assert item.btn_buy.exists(), "Buy button not found!"
            assert item.actual_price.exists(), "Actual price not found!"
        print("gem_shop_check_presence passed!")

    def check_gem_amount(self):
        #Check if the gem amounts in the Gem Shop match the expected values
        for i, item in enumerate(self.shop_navigator.gem_shop.item_gem):
            assert clean_number(item.gem_amount.get_text())==gem_amount[i], f"Gem amount for item {i} does not match expected value!"
            print(f"Item {i} gem amount: {item.gem_amount.get_text()} matches expected value: {gem_amount[i]}")

    def get_index_item_on_sale(self):
        for i, item in enumerate(self.shop_navigator.gem_shop.item_gem):
            if item.old_price is not None:
                item_on_sale.append(i)
                print(f"Item {i} is on sale with old price: {item.old_price.get_text()}")

    def check_vip_point(self):
        #Check if the VIP points in the Gem Shop match the expected values
        for i, item in enumerate(self.shop_navigator.gem_shop.item_gem):
            if item.old_price is not None:
                assert item.vip_point.get_text() == str(vip_point_sale[i]), f"VIP point for item {i} does not match expected value!"
                print(f"Item {i} is on sale with VIP point: {item.vip_point.get_text()} matches expected value: {vip_point_sale[i]}")
            else:
                assert item.vip_point.get_text()==str(vip_point[i]), f"VIP point for item {i} does not match expected value!"
                print(f"Item {i} VIP point: {item.vip_point.get_text()} matches expected value: {vip_point[i]}")
        print("check_vip_point passed!")

