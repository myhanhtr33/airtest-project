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
img_path= os.path.join(os.path.dirname(current_dir),"image","btnCampaign1.png")
btnCampaign_img = Template(img_path, record_pos=(0.254, 0.511), resolution=(900, 1800), rgb= True, scale_max=800, scale_step=0.005)
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
def dev():
    # connect once per session and provide device fixture
    # dev = connect_device("android://127.0.0.1:5037/emulator-5554")
    # dev = connect_device("android://127.0.0.1:5037/emulator-5564")
    dev = connect_device("Windows:///265226")
    print(f"Connected to Unity device: {dev}")
    return dev

@pytest.fixture(scope="session")
def poco(dev,setup_unity_gameview) ->UnityPoco:
    # create UnityPoco while depending on the shared dev fixture
    _poco=UnityPoco()
    screen=_poco.get_screen_size()
    print(f"SSSSSSSScreen size: {screen}")
    return _poco

@pytest.fixture(scope="session")
def poco_android()-> AndroidUiautomationPoco:
    # connect once per session
    return AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False)

@pytest.fixture(scope="session")
def setup_unity_gameview(dev):
    device_uri = str(dev)
    if "android" in device_uri.lower():
        # For Android devices, no special setup needed
        print("Android device detected; no special game view setup required.")
        return dev
    elif "windows" in device_uri.lower():
        # For Windows devices, set focus_rect to exclude internal toolbar
        print("Windows device detected; setting up game view.")
        # Remove the internal toolbar (the row with Display / Aspect / Scale)
        dev.focus_rect = (0, 40, 0, 0)  # start with 40, adjust 35~60 if needed
        # Debug
        w, h = dev.get_current_resolution()
        print("Resolution:", w, h)
        print("focus_rect:", dev.focus_rect)
        return dev


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
def fixture_orchestrator(request, poco, dev):
    """
    Orchestrates the execution order of to_home and to_campaign_select_lv markers.
    """
    # Check for markers
    def get_markers():
        markers = {}
        if hasattr(request.node, 'cls') and request.node.cls:
            class_markers = getattr(request.node.cls, 'pytestmark', [])
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
            campaign_result = exists(btnCampaign_img)
            if campaign_result:
                # existing handling (screenshot + marking when found)
                try:
                    from airtest.core.api import snapshot
                    import cv2
                    import os

                    screenshot_result = snapshot(msg="Campaign button found")
                    if isinstance(screenshot_result, dict) and 'screen' in screenshot_result:
                        screenshot_filename = screenshot_result['screen']
                        screenshot_path = os.path.join(ST.LOG_DIR, screenshot_filename)
                    else:
                        screenshot_path = screenshot_result

                    logger.info(f"[to_home] Screenshot path: {screenshot_path}")

                    img = cv2.imread(screenshot_path)
                    if img is not None:
                        x, y = campaign_result
                        rect_width, rect_height = 100, 50
                        top_left = (int(x - rect_width // 2), int(y - rect_height // 2))
                        bottom_right = (int(x + rect_width // 2), int(y + rect_height // 2))

                        cv2.rectangle(img, top_left, bottom_right, (0, 0, 255), 3)
                        cv2.putText(img, "Campaign Button", (top_left[0], top_left[1] - 10),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

                        marked_screenshot_dir = os.path.join(os.path.dirname(screenshot_path), "marked_screenshots")
                        os.makedirs(marked_screenshot_dir, exist_ok=True)
                        marked_screenshot_path = os.path.join(marked_screenshot_dir,
                                                              f"campaign_button_marked_{attempt}.png")
                        cv2.imwrite(marked_screenshot_path, img)

                        logger.info(f"[to_home] Marked screenshot saved: {marked_screenshot_path}")
                        logger.info(f"[to_home] Campaign button found at position: {campaign_result}")
                    else:
                        logger.warning(f"[to_home] Could not load image from: {screenshot_path}")
                except Exception as e:
                    logger.warning(f"[to_home] Failed to create marked screenshot: {e}")
                break
            else:
                # not found: capture screenshot and try a lower threshold to get an approximate position,
                # then mark and save for debugging (useful when keypoint matches are below default threshold)
                try:
                    from airtest.core.api import snapshot
                    import cv2
                    import os

                    screenshot_result = snapshot(msg="Campaign button NOT found - capture for analysis")
                    if isinstance(screenshot_result, dict) and 'screen' in screenshot_result:
                        screenshot_filename = screenshot_result['screen']
                        screenshot_path = os.path.join(ST.LOG_DIR, screenshot_filename)
                    else:
                        screenshot_path = screenshot_result

                    logger.info(f"[to_home] Saved failure screenshot: {screenshot_path}")

                    img = cv2.imread(screenshot_path)

                    screen = cv2.imread(screenshot_path)
                    if screen is not None:
                        btnCampaign_img.threshold = 0.45  # Lower threshold
                        approx = btnCampaign_img._cv_match(screen)
                    else:
                        approx = None
                    if approx and img is not None:
                        print(f"approx template match: {approx}")
                        center_x, center_y = approx['result']
                        rect_width, rect_height = 120, 60
                        rectangle = approx['rectangle']

                        # Draw the rectangle using the 4 corner points
                        pts = [(int(x), int(y)) for x, y in rectangle]
                        for i in range(4):
                            cv2.line(img, pts[i], pts[(i + 1) % 4], (0, 0, 255), 3)

                        # Draw center point
                        cv2.circle(img, (int(center_x), int(center_y)), 5, (0, 255, 0), -1)

                        # Add label
                        cv2.putText(img, f"fail (conf={approx.get('confidence', 0):.2f})",
                                    (pts[0][0], pts[0][1] - 10),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

                        marked_screenshot_dir = os.path.join(os.path.dirname(screenshot_path), "marked_screenshots")
                        os.makedirs(marked_screenshot_dir, exist_ok=True)
                        marked_screenshot_path = os.path.join(marked_screenshot_dir,
                                                              f"campaign_button_mismatch_{attempt}.png")
                        cv2.imwrite(marked_screenshot_path, img)

                        logger.info(f"[to_home] Marked mismatch screenshot saved: {marked_screenshot_path}")
                        logger.info(f"[to_home] Approximate match position (low threshold): {approx}")
                    else:
                        logger.info("[to_home] No approximate match found; raw screenshot saved for analysis.")
                except Exception as e:
                    logger.warning(f"[to_home] Failed to capture/mark mismatch screenshot: {e}")

                logger.info(f"[to_home] Attempt {attempt + 1}/4 to go to home screen")
                try:
                    send_back(dev)
                    logger.info("[to_home] Sent BACK/ESC keyevent.")
                    time.sleep(1)
                except Exception as e:
                    logger.warning(f"[to_home] BACK/ESC keyevent failed: {e}")
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
                    send_back(dev)
                    logger.info("[to_home] Sent BACK/ESC keyevent.")
                    time.sleep(1)
                except Exception as e:
                    logger.warning(f"[to_home] BACK/ESC keyevent failed: {e}")
            else:
                logger.error("[to_home] ❌ Failed to return to Home screen after 4 attempts.")
                raise RuntimeError("Could not return to Home screen after 4 attempts.")

    if any(marker.kwargs.get("after", False) for marker in markers.values()):
        request.addfinalizer(cleanup)

def send_back(dev):
    """
    Send a "back" action to the connected device.
    - For Android devices: send BACK keyevent
    - For Windows devices: send ESC key via Win32 API
    Args:
        dev: The device fixture from connect_device()
    """
    import ctypes
    import time

    # Check if it's an Android device by inspecting the device type
    device_uri = str(dev)
    if "android" in device_uri.lower():
        # Android device - use BACK keyevent
        keyevent("BACK")
        print("[send_back] Sent BACK keyevent to Android device.")
    elif "windows" in device_uri.lower():
        # Windows device - send ESC key using Win32 API
        # This directly simulates pressing ESC key on the active window
        VK_ESCAPE = 0x1B
        KEYEVENTF_KEYUP = 0x0002
        # Press ESC
        ctypes.windll.user32.keybd_event(VK_ESCAPE, 0, 0, 0)
        time.sleep(0.05)  # Small delay between press and release
        # Release ESC
        ctypes.windll.user32.keybd_event(VK_ESCAPE, 0, KEYEVENTF_KEYUP, 0)
        print("[send_back] Sent ESC key to Windows device via Win32 API.")
    else:
        raise RuntimeError(f"Unknown device type: {device_uri}")


