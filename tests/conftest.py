import pytest
from airtest.core.api import connect_device
from poco.drivers.android.uiautomation import AndroidUiautomationPoco
from poco.drivers.unity3d import UnityPoco
from utils.device_setup import PocoManager
from Hierarchy.ShopNavigator import ShopNavigator



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




