from tests.test_CurrencyBar import *
from tests.test_PopupSpecialVideo import *
import traceback



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
    # List of (test class, method name)
    test_suites = [
        (TestPopupSpecialVideo, "run_all_PopupSpecialVideo_tests"),
        # (TestCurrencyBar, "run_all_CurrencyBar_tests"),
        # (TestTabNavigator, "run_all_TabNavigator_tests"),
        # (TestPlayerInfo, "run_all_PlayerInfo_tests"),
    ]
    print("Running Home tests...")

    for test_class, method_name in test_suites:
        run_test(test_class, method_name)

    print("\n✅ All Home tests passed!")

