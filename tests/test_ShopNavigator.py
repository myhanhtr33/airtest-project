from airtest.core.api import *
from utils import base_test
from utils.base_test import BaseTest
from Hierarchy.ShopNavigator import *
import re
from poco.drivers.android.uiautomation import AndroidUiautomationPoco

class TestShopNavigator(BaseTest):
    def __init__(self):
        super().__init__()
        self.shop_navigator = ShopNavigator(self.poco)
        # self.shop_navigator.setup()
        # self.shop_navigator.teardown()

    def run_all_test(self):
        self.test_shop_navigator_ui_elements()

    def test_shop_navigator_ui_elements(self):
        # Test if the Shop Navigator UI elements are present
        assert self.shop_navigator.tabHot.exists(), "tabHot not found!"
        assert self.shop_navigator.tabCard.exists(), "tabCard not found!"
        assert self.shop_navigator.tabGem.exists(), "tabGem not found!"
        self.shop_navigator.tabCard.click(sleep_interval=1)
        assert self.poco("TabCardShop").exists(), "TabCardShop not found!"
        assert self.shop_navigator.card_shop.exists(), "card_shop not found!"
