from Hierarchy.PopupExploration import *
import pytest
from logger_config import get_logger

@pytest.fixture(scope="class")
def PopupExplaration_back_btn(poco):
    try:
        button = poco("Popup_Exploration_Center(Clone)").offspring("BtnBack")
        return button if button.exists() else None
    except Exception as e:
        # Handle RPC timeout or other connection errors when screen is on different page
        logger = get_logger()
        logger.warning(f"Failed to access PopupExploration back button due to connection error: {e}")
        return None

@pytest.mark.use_to_home(before=True, after=True, logger_name="PopupExploration", back_button="PopupExplaration_back_btn")
class TestPopupExploration:
    @pytest.fixture(scope="function", autouse=True)
    def setup(self, poco):
        logger = get_logger("setup method")
        logger.info("Setting up PopupExploration test environment...")
        self.poco = poco

        # Navigate to Exploration popup - adjust the navigation path based on your app
        # This might be different depending on how you access exploration in your app
        exploration_icon = poco("SubFeatureTopLayer").offspring("Exploration_Home")
        if not exploration_icon.exists():
            # Alternative navigation if direct icon doesn't exist
            logger.warning("Direct exploration icon not found, trying alternative navigation...")
            # Add alternative navigation logic here if needed
            pytest.skip("Exploration icon not found - cannot access PopupExploration")
        exploration_icon.click(sleep_interval=1)
        self.popup = PopupExploration(poco)
        assert self.popup.root.exists(), "PopupExploration not found after click!"
        logger.info("PopupExploration initialized successfully")

    def test_12344(self):
        self.popup.btn_shop.click(sleep_interval=1)
        shop = PopupExplorationShop(self.poco)
        # n = self.poco("Popup_Exploration_Shop(Clone)").offspring("lDesception (1)")
        # print(n.get_text())
        daily_shop= shop.daily_shop_items
        print(f"lens of daily_shop: {len(daily_shop)}")
        for item in daily_shop:
            print(f"daily shop item: {item.amount}")
        weekly_shop= shop.weekly_shop_items
        print(f"lens of weekly_shop: {len(weekly_shop)}")
        for item in weekly_shop:
            print(f"weekly shop item: {item.amount}")
        monthly_shop= shop.monthly_shop_items
        print(f"lens of monthly_shop: {len(monthly_shop)}")
        for item in monthly_shop:
            print(f"monthly shop item: {item.amount}")
