import pytest
from airtest.core.api import *
from airtest.core.settings import Settings as ST
from poco.drivers.android.uiautomation import AndroidUiautomationPoco
from poco.drivers.unity3d import UnityPoco
from utils.device_setup import PocoManager
from Hierarchy.ShopNavigator import ShopNavigator
from logger_config import get_logger
from Hierarchy.PopupMilitary import *
import os

current_dir=os.path.dirname(os.path.abspath(__file__))
img_path= os.path.join(os.path.dirname(current_dir),"image","btnCampaign.png")
btnCampaign_img = Template(img_path, record_pos=(-0.003, 0.815), resolution=(720, 1280), rgb= True)

# Set up airtest log directory for screenshots
log_dir = os.path.join(os.path.dirname(current_dir), "LogFiles", "screenshot")
os.makedirs(log_dir, exist_ok=True)
ST.LOG_DIR = log_dir
ST.SAVE_IMAGE = True

def pytest_configure(config):
    config.addinivalue_line(
        "markers",
        "use_to_home: mark test to return to home screen before/after execution"
    )
    config.addinivalue_line(
        "markers",
        "use_to_campaign_select_lv: mark test to click campaign button and verify popup"
    )

@pytest.fixture(scope="session")
def poco() ->UnityPoco:
    # connect once per session
    # dev = connect_device("android://127.0.0.1:5037/emulator-5554")
    dev = connect_device("android://127.0.0.1:5037/emulator-5562")
    print(f"Connected to Unity device: {dev}")
    _poco=UnityPoco()
    return _poco

@pytest.fixture(scope="session")
def poco_android()-> AndroidUiautomationPoco:
    # connect once per session
    return AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False)

@pytest.fixture(scope="function")
def shop_navigator(poco)-> ShopNavigator:
    """
       For each test function, give me a freshly
       instantiated ShopNavigator rooted at the current UI.
       """
    return ShopNavigator(poco)
@pytest.fixture(scope="function")
def popup_military_info(poco)-> PopupMilitaryCareerInfo:
    return PopupMilitaryCareerInfo(poco)

@pytest.fixture(scope="function", autouse=True)
def fixture_orchestrator(request, poco):
    """
    Orchestrates the execution order of to_home and to_campaign_select_lv markers.
    """
    # Check for markers
    def get_markers():
        markers = {}
        if hasattr(request.node, 'cls') and request.node.cls:
            class_markers = request.node.cls.pytestmark or []
            for m in class_markers:
                if m.name in ['use_to_home', 'use_to_campaign_select_lv']:
                    markers[m.name] = m

        # Also check function-level markers
        for marker_name in ['use_to_home', 'use_to_campaign_select_lv']:
            func_marker = request.node.get_closest_marker(marker_name)
            if func_marker:
                markers[marker_name] = func_marker

        return markers

    markers = get_markers()
    if not markers:
        return  # No relevant markers found

    poco = request.getfixturevalue("poco")

    # Execute to_home first if it exists and has before=True
    to_home_marker = markers.get('use_to_home')
    if to_home_marker and to_home_marker.kwargs.get("before", False):
        logger_name = to_home_marker.kwargs.get("logger_name", request.node.cls.__name__ if request.node.cls else "Test")
        logger = get_logger(logger_name)
        back_button_func = to_home_marker.kwargs.get("back_button", None)
        back_button = request.getfixturevalue(back_button_func) if back_button_func else None

        logger.info("to home fixture initialized.")

        # Try up to 4 times to get to the home screen
        for attempt in range(5):
            if exists(btnCampaign_img):
                logger.info("[to_home] Already at Home screen.")
                # Take screenshot and mark the Campaign button
                # try:
                #     from airtest.core.api import snapshot
                #     import cv2
                #     import os
                #
                #     campaign_result = exists(btnCampaign_img)
                #     print(f"::::::::::::::::::: {campaign_result}  ")
                #     if campaign_result:
                #         # Take screenshot
                #         screenshot_result = snapshot(msg="Campaign button found")
                #         logger.info(f"[to_home] Screenshot taken: {screenshot_result}")
                #
                #         # Extract the actual file path from the result
                #         if isinstance(screenshot_result, dict) and 'screen' in screenshot_result:
                #             screenshot_filename = screenshot_result['screen']
                #             screenshot_path = os.path.join(ST.LOG_DIR, screenshot_filename)
                #         else:
                #             screenshot_path = screenshot_result
                #
                #         logger.info(f"[to_home] Screenshot path: {screenshot_path}")
                #
                #         # Load the screenshot and mark the campaign button
                #         img = cv2.imread(screenshot_path)
                #         if img is not None:
                #             # campaign_result contains the position (x, y) of the found object
                #             x, y = campaign_result
                #
                #             # Draw a rectangle around the button (approximate size)
                #             # Adjust the rectangle size based on your button dimensions
                #             rect_width, rect_height = 100, 50  # Adjust as needed
                #             top_left = (int(x - rect_width//2), int(y - rect_height//2))
                #             bottom_right = (int(x + rect_width//2), int(y + rect_height//2))
                #
                #             # Draw red rectangle around the button
                #             cv2.rectangle(img, top_left, bottom_right, (0, 0, 255), 3)
                #
                #             # Add text label
                #             cv2.putText(img, "Campaign Button", (top_left[0], top_left[1] - 10),
                #                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                #
                #             # Save the marked screenshot
                #             marked_screenshot_dir = os.path.join(os.path.dirname(screenshot_path), "marked_screenshots")
                #             os.makedirs(marked_screenshot_dir, exist_ok=True)
                #             marked_screenshot_path = os.path.join(marked_screenshot_dir, f"campaign_button_marked_{attempt}.png")
                #             cv2.imwrite(marked_screenshot_path, img)
                #
                #             logger.info(f"[to_home] Marked screenshot saved: {marked_screenshot_path}")
                #             logger.info(f"[to_home] Campaign button found at position: {campaign_result}")
                #         else:
                #             logger.warning(f"[to_home] Could not load image from: {screenshot_path}")
                # except Exception as e:
                #     logger.warning(f"[to_home] Failed to create marked screenshot: {e}")
                break
            logger.info(f"[to_home] Attempt {attempt + 1}/4 to go to home screen")

            try:
                keyevent("BACK")
                logger.info("[to_home] Sent BACK keyevent.")
                time.sleep(1)
            except Exception:
                logger.warning("[to_home] BACK keyevent not supported.")
        else:
            logger.error("[to_home] ❌ Failed to return to Home screen after 4 attempts.")
            raise RuntimeError("Could not return to Home screen after 4 attempts.")

    # Execute to_campaign_select_lv after to_home if it exists and has before=True
    campaign_marker = markers.get('use_to_campaign_select_lv')
    if campaign_marker and campaign_marker.kwargs.get("before", False):
        logger_name = campaign_marker.kwargs.get("logger_name", request.node.cls.__name__ if request.node.cls else "Test")
        logger = get_logger(logger_name)

        logger.info("[to_campaign_select_lv] Clicking Campaign button...")
        campaign_btn = poco("BtnCampaign")
        if not campaign_btn.exists():
            logger.error("[to_campaign_select_lv] ❌ Campaign button not found!")
            raise RuntimeError("Campaign button not found")

        campaign_btn.click()
        time.sleep(1)  # Wait for the popup to appear

        # Check if PopupSelectLevelHome exists
        popup = poco("PopupSelectLevelHome(Clone)")
        if not popup.exists():
            logger.error("[to_campaign_select_lv] ❌ PopupSelectLevelHome not found after clicking Campaign!")
            raise RuntimeError("PopupSelectLevelHome(Clone) not found after clicking Campaign button")

        logger.info("[to_campaign_select_lv] ✓ Campaign popup opened successfully")

    # Handle after cleanup
    def cleanup():
        if to_home_marker and to_home_marker.kwargs.get("after", False):
            logger_name = to_home_marker.kwargs.get("logger_name", request.node.cls.__name__ if request.node.cls else "Test")
            logger = get_logger(logger_name)

            for attempt in range(5):
                if exists(btnCampaign_img):
                    logger.info("[to_home] Already at Home screen.")
                    break
                logger.info(f"[to_home] Attempt {attempt + 1}/4 to go to home screen")

                try:
                    keyevent("BACK")
                    logger.info("[to_home] Sent BACK keyevent.")
                    time.sleep(1)
                except Exception:
                    logger.warning("[to_home] BACK keyevent not supported.")
            else:
                logger.error("[to_home] ❌ Failed to return to Home screen after 4 attempts.")
                raise RuntimeError("Could not return to Home screen after 4 attempts.")

    if any(marker.kwargs.get("after", False) for marker in markers.values()):
        request.addfinalizer(cleanup)
