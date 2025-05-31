from tests.test_CurrencyBar import *
from tests.test_PopupSpecialVideo import *
from tests.test_ShopNavigator import *
from tests.test_PopupPlayerProfile import *
from utils.device_setup import *
import traceback
from utils.get_resource_amount import *


poco = PocoManager.get_poco()
currency_bar = CurrencyBar(poco)

def run_test(test_class, test_method_name):
    test_instance = test_class()
    print(f"\n🔹 Running {test_class.__name__}.{test_method_name}...")
    try:
        getattr(test_instance, test_method_name)()
    except AssertionError as e:
        print(f"❌ {test_class.__name__} failed: {e}")
    except Exception as e:
        print(f"💥 Unexpected error in {test_class.__name__}: {e}")
        traceback.print_exc()  # Log the full traceback for debugging
    finally:
        test_instance.teardown()

def run_all_home_tests():
    # result = get_all_card_amounts(poco)
    # print("All resource amounts:", result)
    # result=poco.invoke("get_card_amount", cardType="ITEM_CARD_PLANE_GENERAL")
    # if result and result.get("status") == "success":
    #     amount = result.get("amount")
    #     name= result.get("card_id")
    #     print(f"✅ Card {name} amount is:", amount)
    #     print(f"full result: {result}")
    # else:
    #     raise RuntimeError(f"❌ Command failed: {result}")

    #List of (head to target method, test class, method name)
    test_suites = [
        # (TestPopupSpecialVideo, "run_all_PopupSpecialVideo_tests", head_to_PopupSpecialVideo),
        # (TestCurrencyBar, "run_all_CurrencyBar_tests"),
        # (TestShopNavigator, "run_all_test", ""),
        (TestPopupPlayerProfile, "run_all_tests", "")
    ]
    print("Running Home tests...")

    for test_class, method_name, navigate_method in test_suites:
        # check_in_home()
        if navigate_method!="":
            navigate_method()
        run_test(test_class, method_name)
    print("\n✅ All Home tests passed!")

def check_in_home():
    # Check if we are in the home screen
    assert poco("HomeSquad_1").offspring("BtnAircraft").exists(), "Not in Home screen!"
    print("✅ In Home screen!")

def head_to_PopupSpecialVideo():
    video_icon_home = CurrencyBar(poco).video_home.video_icon()
    assert video_icon_home.exists(), "Video icon not found!"
    video_icon_home.click()
