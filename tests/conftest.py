import pytest
from airtest.core.api import connect_device, keyevent
from poco.drivers.android.uiautomation import AndroidUiautomationPoco
from poco.drivers.unity3d import UnityPoco
from utils.device_setup import PocoManager
from Hierarchy.ShopNavigator import ShopNavigator
import time
from logger_config import get_logger


@pytest.fixture(scope="session")
def poco() ->UnityPoco:
    # connect once per session
    dev = connect_device("android://127.0.0.1:5037/emulator-5554")
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

@pytest.fixture(scope="function", autouse=True)
def to_home(request):
    """
    Auto-applies to tests using the @pytest.mark.use_to_home(...) marker.
    """
    marker = request.node.get_closest_marker("use_to_home")
    if not marker:
        return  # No marker → do nothing

    before = marker.kwargs.get("before", False)
    after = marker.kwargs.get("after", False)
    back_button = marker.kwargs.get("back_button", None)
    logger_name = marker.kwargs.get("logger_name", request.node.cls.__name__ if request.node.cls else "Test")
    logger = get_logger(logger_name)
    poco = request.getfixturevalue("poco")

    def _go_home():
        if poco("HomeSquad_1").offspring("BtnAircraft").exists():
            logger.info("[to_home] Already at Home screen.")
            return

        if back_button and back_button.exists():
            logger.info("[to_home] Clicking back button proxy object")
            back_button.click()
            time.sleep(1)
        else:
            try:
                keyevent("BACK")
                logger.info("[to_home] Sent BACK keyevent.")
                time.sleep(1)
            except Exception:
                logger.warning("[to_home] BACK keyevent not supported.")

        for _ in range(5):
            if poco("HomeSquad_1").offspring("BtnAircraft").exists():
                logger.info("[to_home] Reached Home screen.")
                return
            time.sleep(0.5)

        logger.error("[to_home] ❌ Failed to return to Home screen.")
        raise RuntimeError("Could not return to Home screen.")

    if before:
        _go_home()

    if after:
        def finalize():
            _go_home()
        request.addfinalizer(finalize)




