from airtest.core.api import *
# from utils import base_test
# from utils.base_test import BaseTest
from Hierarchy.ShopNavigator import *
import re
from poco.drivers.android.uiautomation import AndroidUiautomationPoco
from utils.get_resource_amount import clean_number
from utils.helper_functions import *
from utils.sprite_mapping import *
from utils.get_resource_amount import *

gem_amount=[160,460,1000,2500,7000,16000]
vip_point=[2,5,10,20,50,100]
vip_point_sale=[1,2,5,10,25,50]
item_on_sale=[]
item_prices = []
gem_price=[50,200,1000]
enery_amount=[6450,28380,148350]
gold_amount=[12900,56760,296700]

class TestGemShop(BaseTest):
    def __init__(self, shop_navigator):
        super().__init__()
        self.shop_navigator = shop_navigator

    def run_all_test(self):
        logger.info("TestGemShop- run all test")
        self.check_presence_all_element()
        self.check_ItemGemShop()
        self.check_ItemEneryShop()
        self.check_ItemGoldShop()

    def check_presence_all_element(self):
        for itemGem in self.shop_navigator.gem_shop.item_gem:
            print(f"checking item: {itemGem.root.get_name()}")
            logger.info(f"checking Gemitem: {itemGem.root.get_name()}")
            assert itemGem.gem_img.exists(), "Gem image not found!"
            assert itemGem.gem_icon.exists(), "Gem icon not found!"
            assert itemGem.gem_amount.exists(), "Gem amount not found!"
            assert itemGem.btn_buy.exists(), "Buy button not found!"
            assert itemGem.actual_price.exists(), "Actual price not found!"
            assert itemGem.vip_point.exists(), "VIP point not found!"
            assert itemGem.vip_icon.exists(), "VIP icon not found!"
        for itemEnergy in self.shop_navigator.gem_shop.item_energy:
            print(f"checking item: {itemEnergy.root.get_name()}")
            logger.info(f"checking itemEnergy: {itemEnergy.root.get_name()}")
            assert itemEnergy.energy_img.exists(), "Energy image not found!"
            assert itemEnergy.energy_icon.exists(), "Energy icon not found!"
            assert itemEnergy.energy_amount.exists(), "Energy amount not found!"
            assert itemEnergy.btn_exchange.exists(), "Exchange button not found!"
            assert itemEnergy.price.exists(), "Price not found!"
            assert itemEnergy.price_icon.exists(), "Price icon not found!"
        for itemGold in self.shop_navigator.gem_shop.item_gold:
            print(f"checking itemGold: {itemGold.root.get_name()}")
            assert itemGold.gold_img.exists(), "Gold image not found!"
            assert itemGold.gold_icon.exists(), "Gold icon not found!"
            assert itemGold.gold_amount.exists(), "Gold amount not found!"
            assert itemGold.btn_exchange.exists(), "Exchange button not found!"
            assert itemGold.price.exists(), "Price not found!"
            assert itemGold.price_icon.exists(), "Price icon not found!"
        print("gem_shop_check_presence passed!")

    def check_ItemGemShop(self):
        itemGem_amounts = [itemGem.gem_amount for itemGem in self.shop_navigator.gem_shop.item_gem]
        self.check_amount(gem_amount, itemGem_amounts)
        self.check_vip_point()
        self.check_actual_price()
        self.check_old_price()
        self.check_buy_all_gem_items()

    def check_ItemEneryShop(self):
        x, y = self.shop_navigator.gem_shop.root.child("Scroll View").get_position()
        self.poco.swipe([x,y],direction=[0, -1], duration=1)
        itemEnergy_energy_amounts = [itemEnergy.energy_amount for itemEnergy in self.shop_navigator.gem_shop.item_energy]
        itemEnergy_gem_prices = [itemEnergy.price for itemEnergy in self.shop_navigator.gem_shop.item_energy]
        self.check_amount(enery_amount, itemEnergy_energy_amounts)
        self.check_amount(gem_price, itemEnergy_gem_prices)
        self.check_buy_all_energy_items()

    def check_ItemGoldShop(self):
        itemGold_gold_amounts = [itemGold.gold_amount for itemGold in self.shop_navigator.gem_shop.item_gold]
        itemGold_gem_prices = [itemGold.price for itemGold in self.shop_navigator.gem_shop.item_gold]
        self.check_amount(gold_amount, itemGold_gold_amounts)
        self.check_amount(gem_price, itemGold_gem_prices)
        self.check_buy_all_gold_items()

    def check_amount(self, expected_amount_list, item_list):
        # Check if amount in item_list meet the expected values in expected_amount_list
        for i, item in enumerate(item_list):
            assert clean_number(item.get_text()) == expected_amount_list[i], f"Amount for {item} does not match expected value {expected_amount_list[i]}!"
            print(f"{item} amount: {item.get_text()} matches expected value: {expected_amount_list[i]}")
            logger.info(f"Amount for {item} matches expected value: {expected_amount_list[i]}")
    def get_index_item_on_sale(self):
        for i, item in enumerate(self.shop_navigator.gem_shop.item_gem):
            if item.old_price is not None:
                item_on_sale.append(i)
                print(f"Item {i} is on sale with old price: {item.old_price.get_text()}")

    def check_vip_point(self):
        #Check if the VIP points in the Gem Shop match the expected values
        for i, item in enumerate(self.shop_navigator.gem_shop.item_gem):
            if item.old_price is not None:
                assert item.vip_point.get_text() == str(vip_point_sale[i]), f"VIP point for item {i} does not match expected value!"
                print(f"Item {i} is on sale with VIP point: {item.vip_point.get_text()} matches expected value: {vip_point_sale[i]}")
            else:
                assert item.vip_point.get_text()==str(vip_point[i]), f"VIP point for item {i} does not match expected value!"
                print(f"Item {i} VIP point: {item.vip_point.get_text()} matches expected value: {vip_point[i]}")
        print("check_vip_point passed!")

    def check_actual_price(self):
        #check price in right format
        for i, item in enumerate(self.shop_navigator.gem_shop.item_gem):
            price_text = item.actual_price.get_text()
            if price_text is not None:
                item_prices.append(tuple(parse_store_price(price_text)))
            else:
                raise ValueError(f"Item {i} does not have a valid price text: {price_text}")
        print("Parsed item prices:", item_prices)

    def check_old_price(self):
        #check old price in right format and bigger than actual price
        for i, item in enumerate(self.shop_navigator.gem_shop.item_gem):
            if item.old_price is not None:
                print(f"Checking old price for item {i}: {item.old_price.child("lOldPrice").get_text()}")
                old_price_text = item.old_price.child("lOldPrice").get_text()
                currency, price = parse_store_price(old_price_text)
                if price and currency is not None:
                    assert currency == item_prices[i][0], f"Currency mismatch for item {i}: expected {item_prices[i][0]}, got {currency}"
                    assert price> item_prices[i][1], f"Old price for item {i} is not greater than actual price: {price} > {item_prices[i][1]}"
                    print(f"Item {i} old price: {old_price_text} is valid and greater than actual price: {item_prices[i][1]}")
                else:
                    raise ValueError(f"Item {i} does not have a valid old price text: {old_price_text}")

    def check_buy_all_gem_items(self):
        # Check if all items can be bought
        buyBtn=None
        self.get_index_item_on_sale()
        for i, item in enumerate(self.shop_navigator.gem_shop.item_gem):
            gemBefore=get_single_resource_amount(self.poco,"gem")
            print(f"checking item{i}, buy {gem_amount[i]}gem, gemBefore:{gemBefore} ...")
            # 1. Click the in‐game “Buy” button
            item.btn_buy.click(sleep_interval=1)
            # 2.Wait for and click the store’s “Buy”/“Confirm” button
            """
                    Poll the Google Play / Apple Store dialog for the “Buy” or “Confirm” button.
                    Attempts up to 13 times, waiting 1 seconds between tries.
                    Returns a Poco node for the “Buy” button once found, or raises RuntimeError.
            """
            for attempt in range(13):
                time.sleep(1)
                try:
                    buyBtn = self.pocoAndroid("android.widget.FrameLayout").child("android.widget.LinearLayout").child(
                        "android.widget.FrameLayout").offspring("android:id/content").child(
                        "com.android.vending:id/0_resource_name_obfuscated").child(
                        "com.android.vending:id/0_resource_name_obfuscated").child(
                        "com.android.vending:id/0_resource_name_obfuscated")[1].child(
                        "com.android.vending:id/0_resource_name_obfuscated")[3].child(
                        "com.android.vending:id/0_resource_name_obfuscated").offspring(
                        "com.android.vending:id/button_group").child("com.android.vending:id/0_resource_name_obfuscated")
                    if buyBtn.exists():
                        print(f"Buy button appeared for item {i} on attempt {attempt + 1}.")
                        break
                except Exception as e:
                    pass
                    # print(f"An error occurred: {e}")
            else:
                raise RuntimeError(f"Buy button did not appear for item {i} after 5 attempts.")
            buyBtn.click(sleep_interval=1)
            maybe_handle_vip_congrats(self.poco, timeout=7.0, poll_interval=0.5)
            # 3. Wait for the reward popup, then read and verify its icon+amount
            popupClaim=self.poco("PopupRewardItem(Clone)")
            wait_for_element(popupClaim, condition="appear", timeout=5)
            if popupClaim.exists():
                actual_reward={
                    "sprite": popupClaim.offspring("sIcon").attr("texture"),
                    "amount": clean_number(popupClaim.offspring("lQuantity").get_text())
                }
            else:
                raise RuntimeError(f"Reward popup did not appear for item {i} after 5 seconds.")
            expected_reward={
                "sprite": RESOURCE_SPRITE_MAPPING.get("gem"),
                "amount": clean_number(item.gem_amount.get_text())
            }
            assert actual_reward["sprite"] == expected_reward["sprite"], f"Item {i} reward sprite mismatch: expected {expected_reward['sprite']}, got {actual_reward['sprite']}"
            assert actual_reward["amount"] == expected_reward["amount"], f"Item {i} reward amount mismatch: expected {expected_reward['amount']}, got {actual_reward['amount']}"
            # 4. Click the “Claim” button on the popup
            btnClaim= popupClaim.offspring("bClaim")
            btnClaim.click(sleep_interval=1)
            # 5. Verify gem balance increased correctly
            gemAfter=get_single_resource_amount(self.poco,"gem")
            assert verify_resource_amount_change("gem", gemAfter, gemBefore + clean_number(item.gem_amount.get_text()))\
                , f"Gem after {gemAfter} purchase for item {i} does not match expected value {gemBefore} + {clean_number(item.gem_amount.get_text())}!"
            # 6. Verify vip point increased correctly after buying
            # verify vip point every purchase by comparing with CachePvp.myVipPoin
            # then sum up all vip points in a variable. when the loop ends, compare point shown in VIP popup with (that variable + the point before the loop start)
            # 7. Verify item on sale back to normal after buying
            if i in item_on_sale and item_on_sale:
                assert item.old_price is None, f"Item {i},old price not vanish after buying"
                assert item.vip_point.get_text() == str(vip_point[i]), f"Item {i}, vip point not back to normal value after buying!"

    def check_buy_all_energy_items(self):
        for i, item in enumerate(self.shop_navigator.gem_shop.item_energy):
            # 1. get energy and gem balance before buying
            energyBefore = get_single_resource_amount(self.poco, "energy")
            gemBefore = get_single_resource_amount(self.poco, "gem")
            print(f"checking item {i}, buy {enery_amount[i]} energy, energyBefore: {energyBefore}, gemBefore: {gemBefore} ...")
            # 2. check gem balance is enough to buy the item, if not, call the poco command to add gems
            if gemBefore < gem_price[i]:
                self.poco.invoke("add_gem", amount=3000)
                time.sleep(3)
                gemBefore = get_single_resource_amount(self.poco, "gem")
                print(f"Not enough gems to buy item {i}, adding 3000 gems. Current amount: {gemBefore}")
                assert gemBefore>= gem_price,"not enough gem to test"
            # 3. Click the in‐game “Exchange” button
            item.btn_exchange.click(sleep_interval=1)
            # 4. Wait for popupClaim, verify reward then click Claim button
            popupClaim = self.poco("PopupRewardItem(Clone)")
            wait_for_element(popupClaim, condition="appear", timeout=5)
            if popupClaim.exists():
                actual_reward = {
                    "sprite": popupClaim.offspring("sIcon").attr("texture"),
                    "amount": clean_number(popupClaim.offspring("lQuantity").get_text())
                }
            else:
                raise RuntimeError(f"Reward popup did not appear for item {i} after 5 seconds.")
            expected_reward = {
                "sprite": RESOURCE_SPRITE_MAPPING.get("energy"),
                "amount": clean_number(item.energy_amount.get_text())
            }
            assert actual_reward["sprite"] == expected_reward["sprite"], f"Item {i} reward sprite mismatch: expected {expected_reward['sprite']}, got {actual_reward['sprite']}"
            assert actual_reward["amount"] == expected_reward["amount"], f"Item {i} reward amount mismatch: expected {expected_reward['amount']}, got {actual_reward['amount']}"
            #5. Click the “Claim” button on the popup
            btnClaim = popupClaim.offspring("bClaim")
            btnClaim.click(sleep_interval=1)
            #6. verify energy, gem balance fluctuate correctly
            energyAfter = get_single_resource_amount(self.poco, "energy")
            gemAfter = get_single_resource_amount(self.poco, "gem")
            assert verify_resource_amount_change("energy", energyAfter, energyBefore + clean_number(item.energy_amount.get_text())),\
                     f"Energy after {energyAfter} purchase for item {i} does not match expected value {energyBefore} + {enery_amount[i]}!"
            assert verify_resource_amount_change("gem", gemAfter, gemBefore - gem_price[i]),\
                        f"Gem after {gemAfter} purchase for item {i} does not match expected value {gemBefore} - {gem_price[i]}!"

    def check_buy_all_gold_items(self):
        for i, item in enumerate(self.shop_navigator.gem_shop.item_gold):
            # 1. get gold and gem balance before buying
            goldBefore = get_single_resource_amount(self.poco, "gold")
            gemBefore = get_single_resource_amount(self.poco, "gem")
            print(f"checking item {i}, buy {gold_amount[i]} gold, goldBefore: {goldBefore}, gemBefore: {gemBefore} ...")
            # 2. check gem balance is enough to buy the item, if not, call the poco command to add gems
            if gemBefore < gem_price[i]:
                self.poco.invoke("add_gem", amount=3000)
                time.sleep(3)
                gemBefore = get_single_resource_amount(self.poco, "gem")
                print(f"Not enough gems to buy item {i}, adding 3000 gems. Current amount: {gemBefore}")
            # 3. Click the in‐game “Exchange” button
            item.btn_exchange.click(sleep_interval=1)
            # 4. Wait for popupClaim, verify reward then click Claim button
            popupClaim = self.poco("PopupRewardItem(Clone)")
            wait_for_element(popupClaim, condition="appear", timeout=5)
            if popupClaim.exists():
                actual_reward = {
                    "sprite": popupClaim.offspring("sIcon").attr("texture"),
                    "amount": clean_number(popupClaim.offspring("lQuantity").get_text())
                }
            else:
                raise RuntimeError(f"Reward popup did not appear for item {i} after 5 seconds.")
            expected_reward = {
                "sprite": RESOURCE_SPRITE_MAPPING.get("gold"),
                "amount": clean_number(item.gold_amount.get_text())
            }
            assert actual_reward["sprite"] == expected_reward["sprite"], f"Item {i} reward sprite mismatch: expected {expected_reward['sprite']}, got {actual_reward['sprite']}"
            assert actual_reward["amount"] == expected_reward["amount"], f"Item {i} reward amount mismatch: expected {expected_reward['amount']}, got {actual_reward['amount']}"
            #5. Click the “Claim” button on the popup
            btnClaim = popupClaim.offspring("bClaim")
            btnClaim.click(sleep_interval=1)
            #6. verify gold, gem balance fluctuate correctly
            goldAfter = get_single_resource_amount(self.poco, "gold")
            gemAfter = get_single_resource_amount(self.poco, "gem")
            assert verify_resource_amount_change("gold", goldAfter, goldBefore + clean_number(item.gold_amount.get_text())),\
                        f"Gold after {goldAfter} purchase for item {i} does not match expected value {goldBefore} + {gold_amount[i]}!"
            assert verify_resource_amount_change("gem", gemAfter, gemBefore - gem_price[i]),\
                        f"Gem after {gemAfter} purchase for item {i} does not match expected value {gemBefore} - {gem_price[i]}!"



def parse_store_price(price_str):
    """
    Parses a localized price string (e.g. "$4.99", "€1 234,56", "₫39 000", "¥120", "£0.99")
    into (currency_part, amount_as_float).

    - currency_part: everything up to (but not including) the first digit or grouping separator.
    - amount_as_float: the numeric value as a float after removing grouping and normalizing decimal.

    Raises ValueError if format is not recognized.
    """
    # 1) Trim whitespace
    s = price_str.strip()

    # 2) Regex to capture:
    #    ^\s*([^\d]+)?([\d.,\u00A0\u2009\u202F]+)\s*$
    #     └─── Group 1: all leading non-digit characters (currency symbols, letters) ───┐
    #         e.g. "$", "€", "USD ", "JPY"
    #                                   └── Group 2: digits plus possible separators ─┘
    #                                        (commas, periods, NBSP, thin-space, narrow-no-break)
    pattern = re.compile(r'^\s*([^\d]+)?([\d.,\u00A0\u2009\u202F]+)\s*$')
    m = pattern.match(s)
    if not m:
        raise ValueError(f"Price '{price_str}' does not match expected pattern.")

    currency_part = m.group(1) or ""    # e.g. "₫", "$", "EUR ", or "" if none
    number_part   = m.group(2)         # e.g. "39,000", "1 234,56", "4.99"

    # 3) Normalize all known space-like grouping separators to a single ASCII comma
    #    Replace NBSP, thin space, narrow no-break space, ordinary space → comma
    normalized = (
        number_part
        .replace("\u00A0", ",")   # NBSP → ,
        .replace("\u2009", ",")   # thin-space → ,
        .replace("\u202F", ",")   # narrow no-break → ,
        .replace(" ", ",")        # ordinary space → ,
    )

    # 4) Decide which character - comma or period - is the decimal separator:
    #    - If both ',' and '.' appear, the rightmost one is decimal.
    #    - If only one appears:
    #        • If it appears exactly once at least 1 digit from the end, treat as decimal.
    #        • If it appears multiple times, treat as grouping, unless the last group is 2 digits (common).
    dec_sep = None

    if ',' in normalized and '.' in normalized:
        # whichever is rightmost
        if normalized.rfind('.') > normalized.rfind(','):
            dec_sep = '.'
        else:
            dec_sep = ','
    elif '.' in normalized:
        # only period present
        # if there's exactly one period and exactly two digits after it → decimal
        idx = normalized.rfind('.')
        if len(normalized) - idx - 1 in (1, 2, 3):
            dec_sep = '.'
        else:
            # treat '.' as grouping?
            # But most store prices like "Kč 1.234,56" use '.' as grouping not decimal.
            dec_sep = None
    elif ',' in normalized:
        idx = normalized.rfind(',')
        if len(normalized) - idx - 1 in (1, 2, 3):
            dec_sep = ','
        else:
            dec_sep = None
    else:
        dec_sep = None  # no period or comma

    # 5) Remove grouping separators and normalize decimal to a dot
    if dec_sep == ',':
        # replace that comma with a period, then remove all other commas
        temp = normalized.replace(',', 'X')      # temporarily mark all commas
        temp = temp.replace('X', '.')            # if they were decimal
        # but we only want the RIGHTMOST comma to be decimal → careful:
        # Actually, above logic might convert ALL commas incorrectly. Let's do it more carefully:

        # Better approach here:
        #   – split on last comma → left & right parts
        idx = normalized.rfind(',')
        left = normalized[:idx].replace(',', '')  # remove all grouping commas on the left
        right = normalized[idx+1:]                # the decimal fraction
        temp = left + '.' + right
    elif dec_sep == '.':
        idx = normalized.rfind('.')
        left = normalized[:idx].replace(',', '')  # remove all commas on the left
        right = normalized[idx+1:]
        temp = left + '.' + right
    else:
        # No decimal detected; simply remove all commas (treat them as grouping)
        temp = normalized.replace(',', '')

    # 6) Convert to float
    try:
        amount_float = float(temp)
    except ValueError:
        raise ValueError(f"After cleaning, '{temp}' is not a valid number.")

    return currency_part.strip(), amount_float

