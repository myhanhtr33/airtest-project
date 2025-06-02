from airtest.core.api import *
from utils import base_test
from utils.base_test import BaseTest
from Hierarchy.ShopNavigator import *
from tests.test_GemShop import *
from tests.test_HotShop import *
from tests.test_CardShop import *
import re
from poco.drivers.android.uiautomation import AndroidUiautomationPoco

class TestShopNavigator(BaseTest):
    def __init__(self):
        super().__init__()
        self.shop_navigator = ShopNavigator(self.poco)
        self.test_gem_shop= TestGemShop(self.shop_navigator)
        self.test_hot_shop = TestHotShop(self.shop_navigator)
        self.test_card_shop = TestCardShop(self.shop_navigator)
        # self.shop_navigator.setup()
        # self.shop_navigator.teardown()

    def run_all_test(self):
        # self.test_shop_navigator_ui_elements()
        # self.gem_shop_check_presence()
        self.test_gem_shop.run_all_test()

    def test_shop_navigator_ui_elements(self):
        # Test if the Shop Navigator UI elements are present
        assert self.shop_navigator.tabHot.exists(), "tabHot not found!"
        assert self.shop_navigator.tabCard.exists(), "tabCard not found!"
        assert self.shop_navigator.tabGem.exists(), "tabGem not found!"
        self.shop_navigator.tabCard.click(sleep_interval=1)
        assert self.shop_navigator.card_shop.root.exists(), "card_shop not found!"
        self.shop_navigator.tabGem.click(sleep_interval=1)
        assert self.shop_navigator.gem_shop.root.exists(), "gem_shop not found!"
        self.shop_navigator.tabHot.click(sleep_interval=1)
        assert self.shop_navigator.hot_shop.root.exists(), "hot_shop not found!"
        print("test_shop_navigator_ui_elements passed!")


