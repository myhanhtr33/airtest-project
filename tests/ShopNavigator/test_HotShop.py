from airtest.core.api import *
from utils import base_test
from utils.base_test import BaseTest
from Hierarchy.ShopNavigator import *
import re
from poco.drivers.android.uiautomation import AndroidUiautomationPoco
from Hierarchy.IAP_pack import *
from image_templates.Image_IAPPack import *
PACK_TEMPLATES = {
    "UnlockWorldPack":unlock_pack_panel,
    "BossSlayerPack":boss_pack_panel,
    "EnginePack":engine_pack_panel,
    "RoyaltyPack": royal_pack_panel,
    "DailyPack":daiy_pack_panel,
}

class TestHotShop(BaseTest):
    def __init__(self,shop_navigator):
        super().__init__()
        self.shop_navigator = shop_navigator

    def run_all_test(self):
        self.check_pack_list_presence()
    def check_pack_list_presence(self):
        print("check_pack_list_presence")
        print(f"{self.shop_navigator.hot_shop.list.children()}")
        list_len=len(self.shop_navigator.hot_shop.list.children())
        assert list_len>2, f"only {list_len} pack is present in hotshop"
        for i, pack in enumerate(self.shop_navigator.hot_shop.list.children()):
            print(f"{i}: {pack.get_name()} position:{pack.get_position()}")
            matching_key = next((key for key in PACK_TEMPLATES.keys() if key in pack.get_name()), None)
            if matching_key:
                pack_template = PACK_TEMPLATES[matching_key]
                self.scroll_to_pack(pack_template)
                self.click_pack_then_back(matching_key)

    def click_pack_then_back(self,key):
        pack_panels = {
            "engine": self.shop_navigator.hot_shop.engine_pack_panel,
            "royal": self.shop_navigator.hot_shop.royal_pack_panel,
            "boss": self.shop_navigator.hot_shop.boss_slayer_pack_panel,
            "unlock": self.shop_navigator.hot_shop.unlock_world_pack_panel,
            "daily": self.shop_navigator.hot_shop.daily_pack_panel,
        }
        pack_popup_classes = {
            "engine": EnginePack,
            "royal": RoyalPack,
            "boss": BossSlayerPack,
            "daily": DailyPack,
        }

        for pack_type, panel in pack_panels.items():
            if pack_type in key.lower():
                assert panel.exists(), f"no {pack_type} panel found"
                if pack_type=="unlock":
                    return
                panel.click()
                if pack_type in pack_popup_classes:
                    popup = pack_popup_classes[pack_type](self.poco)
                    assert popup.root.exists(), f"no {pack_type} popup found after click panel"
                    popup.btnBack.click()

    def scroll_to_pack(self,template, MAX_SWIPES=5):
        x,y=self.shop_navigator.hot_shop.root.child("Scroll View").get_position()
        # For each template, swipe until we see it, then click the center of that template
        attempts = 0

        # If the template might lie above your current view, do a “scroll down” first:
        self.poco.swipe([x,y],direction=[0, 1], duration=0.5)
        # Now try swiping up to find it:
        while attempts < MAX_SWIPES:
            if exists(template):
                print(f"find out:{template} in attempt{attempts}")
                return
            else:
                self.poco.swipe([x, y], direction=[0, -0.2], duration=1)
                sleep(0.5)
            attempts += 1
        print(f"find out:{template} in attempt{attempts}. EXITTTT")
        if not exists(template):
            raise RuntimeError(f"Couldn’t find {template.filename}")
        sleep(0.5)