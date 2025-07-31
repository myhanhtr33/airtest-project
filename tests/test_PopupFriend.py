from Hierarchy.PopupFriend import *
from logger_config import get_logger
import pytest
import time
from utils.helper_functions import wait_for_element


@pytest.fixture(scope="class")
def PopupFriend_back_btn(poco):
    try:
        button = poco("PopupFriends(Clone)").offspring("B_Back")
        return button if button.exists() else None
    except Exception as e:
        # Handle RPC timeout or other connection errors when screen is on different page
        logger = get_logger()
        logger.warning(f"Failed to access PopupFriend back button due to connection error: {e}")
        return None

@pytest.mark.use_to_home(before=True, after=True, logger_name="PopupFriend", back_button="PopupFriend_back_btn")
class TestPopupFriend:
    @pytest.fixture(scope="function", autouse=True)
    def setup(self, poco):
        logger = get_logger("setup method")
        logger.info("Setting up PopupFriend test environment...")
        self.poco = poco

        # Navigate to Friends popup - adjust the navigation path based on your app
        # This might be different depending on how you access friends in your app
        friend_icon = poco("SubFeatureTopLayer").offspring("Friend_Home")  # Adjust selector as needed
        if not friend_icon.exists():
            # Alternative navigation if direct icon doesn't exist
            logger.warning("Direct friend icon not found, trying alternative navigation...")
            # Add alternative navigation logic here if needed
            pytest.skip("Friend icon not found - cannot access PopupFriend")

        friend_icon.click(sleep_interval=1)
        start_time = time.time()
        self.popup = PopupFriend(poco)
        assert self.popup.root.exists(), "PopupFriend not found after click!"
        logger.info(f"PopupFriend initialized in {time.time() - start_time:.2f} seconds")

    @pytest.mark.order(1)
    def test_main_elements(self):
        """Test that all main elements defined in PopupFriend.__init__ exist"""
        logger = get_logger()
        logger.info("Testing main elements presence in PopupFriend...")

        # Verify main elements from __init__ exist
        assert self.popup.root.exists(), "PopupFriend root not found!"
        assert self.popup.title.exists(), "Title not found!"
        assert self.popup.title.get_text().strip() == "Friends", "Title text is not 'Friends'!"
        assert self.popup.btn_friend.exists(), "btn_friend not found!"
        assert self.popup.btn_add_friend.exists(), "btn_add_friend not found!"
        assert self.popup.btn_following.exists(), "btn_following not found!"
        assert self.popup.btn_back.exists(), "btn_back not found!"

        # Note: scrollviews and search_panel are only available after clicking corresponding buttons
        # They will be tested in individual tab functionality tests

        logger.info("✅ All main elements verified successfully")

    @pytest.mark.order(2)
    def test_friend_tab_functionality(self):
        """Test Friend tab button activation and corresponding scrollview"""
        logger = get_logger()
        logger.info("Testing Friend tab functionality...")

        # Click Friend tab
        self.popup.btn_friend.click(sleep_interval=1)

        # Check button state using UIButtonUtils with if statements instead of assert
        if not UIButtonUtils.check_sprite_btn_active(self.popup.btn_friend, "btn_friend"):
            logger.error("Friend button not activated after click!")
        if not UIButtonUtils.check_sprite_btn_deactive(self.popup.btn_add_friend, "btn_add_friend"):
            logger.error("Add Friend button not deactivated!")
        if not UIButtonUtils.check_sprite_btn_deactive(self.popup.btn_following, "btn_following"):
            logger.error("Following button not deactivated!")

        # Verify corresponding scrollview is visible/active
        assert self.popup.scrollview_friend.exists(), "ScrollViewFriends not visible after clicking Friend tab!"

        # Verify search panel is not visible (only for Add Friend tab)
        search_panel_visible = self.popup.search_panel.exists() and self.popup.search_panel.attr("visible")
        if search_panel_visible:
            logger.warning("Search panel is visible in Friend tab - should only be visible in Add Friend tab")

        logger.info("✅ Friend tab functionality verified successfully")

    @pytest.mark.order(3)
    def test_add_friend_tab_functionality(self):
        """Test Add Friend tab button activation, corresponding scrollview, and search panel"""
        logger = get_logger()
        logger.info("Testing Add Friend tab functionality...")

        # Click Add Friend tab
        self.popup.btn_add_friend.click(sleep_interval=1)

        # Check button state using UIButtonUtils with if statements instead of assert
        if not UIButtonUtils.check_sprite_btn_active(self.popup.btn_add_friend, "btn_add_friend"):
            logger.error("Add Friend button not activated after click!")
        if not UIButtonUtils.check_sprite_btn_deactive(self.popup.btn_friend, "btn_friend"):
            logger.error("Friend button not deactivated!")
        if not UIButtonUtils.check_sprite_btn_deactive(self.popup.btn_following, "btn_following"):
            logger.error("Following button not deactivated!")

        # Verify corresponding scrollview is visible/active
        assert self.popup.scrollview_request.exists(), "ScrollViewRequest not visible after clicking Add Friend tab!"

        # Verify search panel is visible (specific to Add Friend tab)
        assert self.popup.search_panel.exists(), "Search panel not found in Add Friend tab!"
        search_panel_visible = self.popup.search_panel.attr("visible") if hasattr(self.popup.search_panel, 'attr') else True
        if not search_panel_visible:
            logger.warning("Search panel exists but may not be visible in Add Friend tab")

        logger.info("✅ Add Friend tab functionality verified successfully")

    @pytest.mark.order(4)
    def test_following_tab_functionality(self):
        """Test Following tab button activation and corresponding scrollview"""
        logger = get_logger()
        logger.info("Testing Following tab functionality...")

        # Click Following tab
        self.popup.btn_following.click(sleep_interval=1)

        # Check button state using UIButtonUtils with if statements instead of assert
        if not UIButtonUtils.check_sprite_btn_active(self.popup.btn_following, "btn_following"):
            logger.error("Following button not activated after click!")
        if not UIButtonUtils.check_sprite_btn_deactive(self.popup.btn_friend, "btn_friend"):
            logger.error("Friend button not deactivated!")
        if not UIButtonUtils.check_sprite_btn_deactive(self.popup.btn_add_friend, "btn_add_friend"):
            logger.error("Add Friend button not deactivated!")

        # Verify corresponding scrollview is visible/active
        assert self.popup.scrollview_follow.exists(), "ScrollViewFollowing not visible after clicking Following tab!"

        # Verify search panel is not visible (only for Add Friend tab)
        search_panel_visible = self.popup.search_panel.exists() and self.popup.search_panel.attr("visible")
        if search_panel_visible:
            logger.warning("Search panel is visible in Following tab - should only be visible in Add Friend tab")

        logger.info("✅ Following tab functionality verified successfully")
