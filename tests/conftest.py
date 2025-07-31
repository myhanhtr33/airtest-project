import pytest
from airtest.core.api import *
from poco.drivers.android.uiautomation import AndroidUiautomationPoco
from poco.drivers.unity3d import UnityPoco
from utils.device_setup import PocoManager
from Hierarchy.ShopNavigator import ShopNavigator
import time
from logger_config import get_logger
from Hierarchy.PopupMilitary import *

current_dir=os.path.dirname(os.path.abspath(__file__))
img_path= os.path.join(os.path.dirname(current_dir),"image","btnCampaign.png")
btnCampaign_img = Template(img_path, record_pos=(-0.003, 0.815), resolution=(720, 1280))

def pytest_configure(config):
    config.addinivalue_line(
        "markers",
        "use_to_home: mark test to return to home screen before/after execution"
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
def to_home(request):
    """
    Auto-applies to tests using the @pytest.mark.use_to_home(...) marker.
    """
    print("110000000000011")

    def get_marker():
        # Try to get marker from class first
        if hasattr(request.node, 'cls') and request.node.cls:
            marker = request.node.cls.pytestmark
            print(f"Class markers: {marker}")
            if marker:
                for m in marker:
                    if m.name == 'use_to_home':
                        return m
        # Try to get marker from module
        marker = request.node.get_closest_marker('use_to_home')
        print(f"Module markers: {marker}")
        return marker

    marker = get_marker()
    print(f"Found marker: {marker}")
    if not marker:
        print("skip")
        return  # No marker → do nothing
    print("1111111111111")
    before = marker.kwargs.get("before", False)
    after = marker.kwargs.get("after", False)
    back_button_func = marker.kwargs.get("back_button", None)
    back_button= request.getfixturevalue(back_button_func) if back_button_func else None
    popup_func= marker.kwargs.get("popup", None)
    popup= request.getfixturevalue(popup_func) if popup_func else None
    logger_name = marker.kwargs.get("logger_name", request.node.cls.__name__ if request.node.cls else "Test")
    logger = get_logger(logger_name)
    poco = request.getfixturevalue("poco")
    logger.info("to home fixture initialized.")
    def _go_home():
        print("to_home called")

        # Try up to 4 times to get to the home screen
        for attempt in range(5):
            if exists(btnCampaign_img):
                print("btnCampaign_img found")
                logger.info("[to_home] Already at Home screen.")
                return
            logger.info(f"[to_home] Attempt {attempt + 1}/4 to go to home screen")

            print(f"back_button: {back_button}")
            print(f"back_button_func: {back_button_func}")
            if back_button:
                # logger.info("[to_home] Clicking back button proxy object")
                # back_button.click()
                # time.sleep(1)
                try:
                    keyevent("BACK")
                    logger.info("[to_home] Sent BACK keyevent.")
                    time.sleep(1)
                except Exception:
                    logger.warning("[to_home] BACK keyevent not supported.")
            else:
                try:
                    keyevent("BACK")
                    logger.info("[to_home] Sent BACK keyevent.")
                    time.sleep(1)
                except Exception:
                    logger.warning("[to_home] BACK keyevent not supported.")
        logger.error("[to_home] ❌ Failed to return to Home screen after 4 attempts.")
        raise RuntimeError("Could not return to Home screen after 4 attempts.")

    if before:
        _go_home()

    if after:
        def finalize():
            _go_home()
        request.addfinalizer(finalize)
