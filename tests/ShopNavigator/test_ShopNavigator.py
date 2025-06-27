# from typing import TYPE_CHECKING
#
# if TYPE_CHECKING:
#     from logging import Logger
#     logger: Logger
# from poco.drivers.android.uiautomation import AndroidUiautomationPoco

class TestShopNavigator:
    # def __init__(self):
    #     super().__init__()
    #     self.shop_navigator = ShopNavigator(self.poco)
    #     self.test_gem_shop= TestGemShop(self.shop_navigator)
    #     self.test_hot_shop = TestHotShop(self.shop_navigator)
    #     self.test_card_shop = TestCardShop(self.shop_navigator)
    #     # self.shop_navigator.setup()
    #     # self.shop_navigator.teardown()
    # def run_all_test(self):
    #     self.test_shop_navigator_ui_elements()
    #     self.head_to_gem_shop()
    #     self.test_gem_shop.run_all_test()
    #     self.head_to_card_shop()
    #     self.test_card_shop.run_all_test()
    #     self.head_to_hot_shop()
    #     self.test_hot_shop.run_all_test()

    def test_shop_navigator_ui_elements(self,shop_navigator):
        # Test if the Shop Navigator UI elements are present
        assert shop_navigator.tabHot.exists(), "tabHot not found!"
        assert shop_navigator.tabCard.exists(), "tabCard not found!"
        assert shop_navigator.tabGem.exists(), "tabGem not found!"
        shop_navigator.tabCard.click(sleep_interval=1)
        assert shop_navigator.card_shop.root.exists(), "card_shop not found!"
        shop_navigator.tabGem.click(sleep_interval=1)
        assert shop_navigator.gem_shop.root.exists(), "gem_shop not found!"
        shop_navigator.tabHot.click(sleep_interval=1)
        assert shop_navigator.hot_shop.root.exists(), "hot_shop not found!"
        print("test_shop_navigator_ui_elements passed!")
        logger.info("test_shop_navigator_ui_elements passed!")
    def head_to_gem_shop(self,shop_navigator):
        # Navigate to Gem Shop
        shop_navigator.tabGem.click(sleep_interval=1)
        assert shop_navigator.gem_shop.root.exists(), "Gem Shop root not found!"
        print("✅ Navigated to Gem Shop successfully!")
    def head_to_hot_shop(self, shop_navigator):
        # Navigate to Hot Shop
        shop_navigator.tabHot.click(sleep_interval=1)
        assert shop_navigator.hot_shop.root.exists(), "Hot Shop root not found!"
        print("✅ Navigated to Hot Shop successfully!")
        logger.info("Navigated to Hot Shop successfully!")
    def head_to_card_shop(self,shop_navigator):
        # Navigate to Card Shop
        shop_navigator.tabCard.click(sleep_interval=1)
        assert shop_navigator.card_shop.root.exists(), "Card Shop root not found!"
        print("✅ Navigated to Card Shop successfully!")
        logger.info("Navigated to Card Shop successfully!")


