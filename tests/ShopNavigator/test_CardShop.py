import csv
from utils.helper_functions import *
from utils.get_resource_amount import *
import math
import copy
import pytest
# from conftest import logger
from logger_config import get_logger
gem_day_reset=100
gem_week_reset=500
balance_of_items = []  #name, amount, item type, sprite name
actual_price_and_amount_items = [] #currency type, price, amount
balance_of_currency = {}

@pytest.mark.usefixtures("shop_navigator")
class TestCardShop:
    @pytest.fixture(autouse=True)
    def setup(self,shop_navigator,poco):
        self.shop_navigator=shop_navigator
        self.poco=poco
        # self.logger=get_logger()
        # return self.logger

    # def __init__(self,shop):
    #     super().__init__()
    #     self.shop_navigator = shop_navigator
    #
    # def run_all_test(self, shop_navigator):
    #     self.test_PanelResetDay()
    #     self.test_btn_day_reset()
    #     self.test_PanelResetWeek()
    #     self.test_btn_week_reset()
    #     self.test_DayItems_check_presence()
    #     self.test_DayItems_verify_data()
    #     self.test_DayItems_check_buy()

    @pytest.mark.order(1)
    def test_PanelResetDay(self, shop_navigator):
        logger = get_logger()
        logger.info("Checking PanelResetDay in CardShop...")
        logger.critical("criticalllllll testttttttt...")
        logger.error("1111test thui hihihihihihihihihihihihihihihi")
        logger.warning("test tip' hihihihihihihihihihihihi")
        assert self.shop_navigator.card_shop.day_panel.exists(), "PanelResetDay not found!"
        assert self.shop_navigator.card_shop.day_countdown.exists(), "PanelResetDay countdown not found!"
        assert self.shop_navigator.card_shop.btn_day_reset.exists(), "PanelResetDay reset button not found!"
    @pytest.mark.order(2)
    def test_btn_day_reset(self):
        logger = get_logger()
        logger.info("Checking btn_day_reset in CardShop...")
        assert self.shop_navigator.card_shop.btn_day_reset.exists(), "BtnDayReset not found!"
        assert self.shop_navigator.card_shop.btn_day_reset_BG.exists(), "BtnDayReset background not found!"
        assert self.shop_navigator.card_shop.btn_day_reset_gemIcon.exists(), "BtnDayReset gemIcon not found!"
        assert self.shop_navigator.card_shop.btn_day_reset_gemPrice.exists(), "BtnDayReset gemPrice not found!"
        assert self.shop_navigator.card_shop.btn_day_reset_resetIcon.exists(), "BtnDayReset resetIcon not found!"
        assert self.shop_navigator.card_shop.btn_day_reset_resetCount.exists(), "BtnDayReset resetCount not found!"
        resetCount= int(self.shop_navigator.card_shop.btn_day_reset_resetCount.get_text().strip())
        btn_BG= self.shop_navigator.card_shop.btn_day_reset_BG
        btnDayReset = self.shop_navigator.card_shop.btn_day_reset
        if resetCount == 0:
            self.check_deactive_btn_reset(btnDayReset,btn_BG,self.shop_navigator.card_shop.day_items,logger=logger)
        elif resetCount >= 1:
            self.check_active_btn_reset(btnDayReset,btn_BG,self.shop_navigator.card_shop.day_items, type="day", logger=logger)
            btn_BG = self.shop_navigator.card_shop.btn_day_reset_BG
            self.check_deactive_btn_reset(btnDayReset,btn_BG,self.shop_navigator.card_shop.day_items,logger=logger)
        else:
            raise ValueError("Invalid reset count value: {}".format(resetCount))
    @pytest.mark.order(3)
    def test_PanelResetWeek(self,shop_navigator):
        logger = get_logger()
        logger.info("Checking PanelResetWeek in CardShop...")
        assert self.shop_navigator.card_shop.week_panel.exists(), "PanelResetWeek not found!"
        assert self.shop_navigator.card_shop.week_countdown.exists(), "PanelResetWeek countdown not found!"
        assert self.shop_navigator.card_shop.btn_week_reset.exists(), "PanelResetWeek reset button not found!"
    @pytest.mark.order(4)
    def test_btn_week_reset(self,shop_navigator):
        logger = get_logger()
        assert self.shop_navigator.card_shop.btn_week_reset.exists(), "BtnWeekReset not found!"
        assert self.shop_navigator.card_shop.btn_week_reset_BG.exists(), "BtnWeekReset background not found!"
        assert self.shop_navigator.card_shop.btn_week_reset_gemIcon.exists(), "BtnWeekReset gemIcon not found!"
        assert self.shop_navigator.card_shop.btn_week_reset_gemPrice.exists(), "BtnWeekReset gemPrice not found!"
        assert self.shop_navigator.card_shop.btn_week_reset_resetIcon.exists(), "BtnWeekReset resetIcon not found!"
        assert self.shop_navigator.card_shop.btn_week_reset_resetCount.exists(), "BtnWeekReset resetCount not found!"
        resetCount= int( self.shop_navigator.card_shop.btn_week_reset_resetCount.get_text().strip())
        btn_BG= self.shop_navigator.card_shop.btn_week_reset_BG
        btnWeekReset = self.shop_navigator.card_shop.btn_week_reset
        if resetCount == 0:
            self.check_deactive_btn_reset(btnWeekReset,btn_BG,self.shop_navigator.card_shop.week_items,logger)
        elif resetCount >= 1:
            self.check_active_btn_reset(btnWeekReset,btn_BG,self.shop_navigator.card_shop.week_items, type="week",logger=logger)
            btn_BG = self.shop_navigator.card_shop.btn_week_reset_BG
            self.check_deactive_btn_reset(btnWeekReset,btn_BG,self.shop_navigator.card_shop.week_items,logger=logger)
        else:
            raise ValueError("Invalid reset count value: {}".format(resetCount))
    @pytest.mark.order(5)
    def test_DayItems_check_presence(self, shop_navigator):
        logger=get_logger()
        logger.info("222Checking DayItems in CardShop...")
        assert len(shop_navigator.card_shop.day_items)>0, "no items found in DayItems!"
        for item in shop_navigator.card_shop.day_items +shop_navigator.card_shop.week_items:
            logger.info(f"Checking item: {item}")
            assert item.reward_img.exists(), "Reward image not found in DayItems!"
            assert item.reward_amount.exists(), "Reward amount not found in DayItems!"
            assert item.btn_buy.exists(), "Buy button not found in DayItems!"
            if item.active_btn_buy:
                assert item.price.exists(), "Price not found in active DayItems!"
                assert item.price_icon.exists(), "Price icon not found in active DayItems!"
            elif item.deactive_btn_buy:
                assert item.sold_out_label.exists(), "Sold out label not found in deactive DayItems!"
            else:
                raise ValueError("Item in DayItems is neither active nor deactive!")
    @pytest.mark.order(6)
    def test_DayItems_check_buy(self,shop_navigator):
        logger=get_logger()
        logger.info("Checking DayItems buy functionality in CardShop...")
        #1. get price all items, soldout items will get 0 price
        # 2. get balance of all items,gold,gem,energy. skip for now if item = pilot, diammond chest, stone
        self.get_info_of_items(logger)
        # state before buy
        tempt = copy.deepcopy(balance_of_items)
        tempt1 = copy.deepcopy(balance_of_currency)
        i=0
        # check balance then add if it less than item's price
        for item in self.shop_navigator.card_shop.day_items+self.shop_navigator.card_shop.week_items:
            if actual_price_and_amount_items[i][0]!="":
                balance = get_single_resource_amount(self.poco, actual_price_and_amount_items[i][0])
                if balance < actual_price_and_amount_items[i][1]:
                    if  actual_price_and_amount_items[i][0] == "gem":
                        self.poco.invoke("add_gem", amount=3000)
                    elif actual_price_and_amount_items[i][0] == "gold":
                        self.poco.invoke("add_gold", amount=3000)
                    else:
                        raise ValueError(f"unexpected price {self.poco, actual_price_and_amount_items[i][0]}")
            # 6.there are 2 cases:
            #   a. active button: bought item increament balance, price decrease, all other items remain unchanged. button -> deactive
            #   b. deactive button: popup notice "sold out", balance, price, items remain unchanged
            if item.deactive_btn_buy:
                item.btn_buy.click()
                check_noti(self.poco, "Sold out")
                assert item.deactive_btn_buy.exists(), f"item{i} Deactive Button not found in DayItems!"
                # self.get_info_of_items()
                # assert tempt==balance_of_items, (f"balance_of_items change after click deactive btn buy\n"
                #                                  f"before: {tempt}\n"
                #                                  f"afer: {balance_of_items}")
                # assert tempt1==balance_of_currency, (f"balance_of_currency change after click deactive btn buy\n"
                #                                      f"before: {tempt1}\n"
                #                                      f"after:{balance_of_currency}")
                logger.info(f"item{i} click btnBuy deactive" )
            if item.active_btn_buy:
                item.btn_buy.click()
                # verify popup reward claim: reward amount,reward img in popup compare with img and amount in item
                check_popup_claim_known_resourcce(self.poco,actual_price_and_amount_items[i][2],balance_of_items[i][3],logger)
                sleep(1)
                assert item.deactive_btn_buy.exists(), "Deactive Button not found after successfully buying item!"
                amount=actual_price_and_amount_items[i][2]
                for t in tempt:
                    if tempt[i][3]==t[3]:
                        tempt[tempt.index(t)] = [t[0], t[1] + amount, t[2], t[3]]   # create new list with updated amount
                logger.info(f"item{i} bought: {tempt[i][0]} increased from {tempt[i][1] - amount} to {tempt[i][1]}")
                currency_type=actual_price_and_amount_items[i][0]
                price=actual_price_and_amount_items[i][1]
                if currency_type!="":
                    tempt1[currency_type]-=price
                logger.info(f"item{i} click BUY, {currency_type} {(tempt1[currency_type]+price)} decrease by {price}")
            i+=1
        self.get_info_of_items(logger)
        j=0
        for item in balance_of_items:
            if item[0]!="":
                assert item[1]==tempt[j][1],f"{balance_of_items[j][0]} {balance_of_items[j][1]} don't match expected {tempt[j][1]}, after buy all"
            j+=1
        for key in tempt1:
            verify_resource_amount_change(key,balance_of_currency[key], tempt1[key])
    @pytest.mark.order(7)
    def test_DayItems_verify_data(self, shop_navigator):
        logger = get_logger()
        logger.info("Verifying DayItems data in CardShop...")
        #1. load data from CardShop.csv and actual data from UI
        csv_group1= load_card_shop_data(1)
        csv_group2 = load_card_shop_data(2)
        csv_group3 = load_card_shop_data(3)
        self.get_info_of_items(logger)
        logger.info("CSV Group 1 Data:", csv_group1)
        #2. compare quanity, price, currency of each item in UI with data in CardShop.csv
        i=0
        UInodes=shop_navigator.card_shop.day_items + shop_navigator.card_shop.week_items
        for item in actual_price_and_amount_items:
            logger.info(f"check data item{i}")
            if UInodes[i].deactive_btn_buy:
                i+=1
                continue
            if i in range(0,3): #3 first items
                item_name,expected= csv_group1[i]
                assert item[0] == expected[
                    'currency'], f"Currency mismatch for item{i}: expected {expected['currency']}, got {item[0]}"
                assert item[1] == expected[
                    'price'], f"Price mismatch for item{i}: expected {expected['price']}, got {item[1]}"
                assert item[2] == expected[
                    'quantity'], f"Quantity mismatch for item{i}: expected {expected['quantity']}, got {item[2]}"
                logger.info(f"1:item{i} currency {item[0]} price {item[1]} quantity {item[2]} meet expected {expected['currency']} {expected['price']} {expected['quantity']}")
            elif i in range(3,7):# 3 in middle
                j=0
                item_name, expected = csv_group2[j]
                prices = [item[1]['price'] for item in csv_group2]  # extract all price value from csv_group2
                discount_prices=[math.ceil(item*0.9) for item in prices]  # apply 10% discount to all prices
                amounts= [item[1]['quantity'] for item in csv_group2]  # extract all quantity value from csv_group2
                assert item[0] == expected[
                    'currency'], f"Currency mismatch for item{i}: expected {expected['currency']}, got {item[0]}"
                if i==3: # special case for item 3, which has a discount
                    assert item[1] in discount_prices, f"DiscountPrice mismatch for item{i}: expected {discount_prices}, got {item[1]}"
                else:
                    assert item[1] in prices, f"Price mismatch for item{i}: expected {prices}, got {item[1]}"
                assert item[2] in amounts, f"Quantity mismatch for item{i}: expected {amounts}, got {item[2]}"
                j+= 1
                logger.info(f"2:item{i} currency {item[0]} price {item[1]} quantity {item[2]} meet expected {expected['currency']} {prices} {amounts}")
            else: #3 last items
                j=0
                item_name, expected = csv_group3[j]
                prices = [item[1]['price'] for item in csv_group3]  # extract all price value from csv_group2
                amounts = [item[1]['quantity'] for item in csv_group3]  # extract all quantity value from csv_group2
                assert item[0] == expected[
                    'currency'], f"Currency mismatch for item{i}: expected {expected['currency']}, got {item[0]}"
                assert item[1] in prices, f"Price mismatch for item{i}: expected {prices}, got {item[1]}"
                assert item[2] in amounts, f"Quantity mismatch for item{i}: expected {amounts}, got {item[2]}"
                j += 1
                logger.info(f"3:item{i} currency {item[0]} price {item[1]} quantity {item[2]} meet expected {expected['currency']} {prices} {amounts}")
            i+= 1


    def get_info_of_items(self,logger):
        balance_of_items.clear()
        actual_price_and_amount_items.clear()
        all_items = self.shop_navigator.card_shop.day_items + self.shop_navigator.card_shop.week_items
        reward_imgs= [item.reward_img.attr("texture") for item in all_items]
        for img in reward_imgs:
            item_type = next((key for key, value in CARD_SPRITE_MAPPING.items() if value == img), "")
            if item_type != "":
                item_balance, name = get_single_card_amount(self.poco, item_type)
                balance_of_items.append((name,item_balance,item_type,img))
            else:
                balance_of_items.append(("", 0, "",img))
        logger.info("Balance Items:", balance_of_items)
        for item in all_items:
            amount = clean_number(item.reward_amount.get_text().strip())
            if item.active_btn_buy:
                price_type = item.price_icon.attr("texture")
                price_type = "gold" if price_type == "Gold_small" else "gem" if price_type == "Gem_Green_small" else None
                if price_type is None:
                    raise ValueError("Price icon type not recognized!")
                actual_price_and_amount_items.append((price_type, clean_number(item.price.get_text().strip()), amount))
            elif item.deactive_btn_buy:
                actual_price_and_amount_items.append(("", 0, amount))
                logger.info(f"Item {item.reward_img.attr('texture')}: Sold out, Price = 0")
            else:
                raise ValueError("Item is neither active nor deactive!")
        logger.info(f"actual_price_of_items: {actual_price_and_amount_items}")
        self.get_currency_amount(logger=logger)
    def check_deactive_btn_reset(self,button,btnBG,item_list,logger):
        logger.info("Checking deactive reset button...")
        listBefore=[item.reward_img.attr("texture") for item in item_list]
        gemBefore = get_single_resource_amount(self.poco, "gem")
        BG= btnBG.attr("texture")
        assert BG=="UI5_Bottom_btn_9sl_Grey", "BtnReset background texture is not grey!"
        button.click()
        check_noti(self.poco,"You have used all reset chances")
        sleep(3)
        listAfter = [item.reward_img.attr("texture") for item in item_list]
        assert listBefore== listAfter, "Reward images changed after click deactivating reset button!"
        gemAfter = get_single_resource_amount(self.poco, "gem")
        assert gemBefore== gemAfter, "Gem amount changed after click deactive reset button!"
    def check_active_btn_reset(self,button,btnBG,item_list, type="day",logger=None):
        logger.info("Checking active reset button...")
        listBefore = [item.reward_img.attr("texture") for item in item_list]
        BG = btnBG.attr("texture")
        gemBefore = get_single_resource_amount(self.poco, "gem")
        gem_reset= gem_day_reset if type == "day" else gem_week_reset
        assert BG=="UI5_Bottom_btn_9sl_Red", "BtnReset background texture is not red!"
        if gemBefore < gem_reset:
            self.poco.invoke("add_gem", amount=1000)
            time.sleep(3)
            gemBefore = get_single_resource_amount(self.poco, "gem")
            logger.info("not enough gem, add 1000 gem to test")
            assert gemBefore >= gem_reset, "Not enough gems to reset!"
        button.click()
        popup_notice=self.poco("PopupNotice(Clone)")
        popup_notice_confirm_btn=popup_notice.offspring("bOK")
        popup_notice_confirm_btn.click(sleep_interval=4)
        listAfter = [item.reward_img.attr("texture") for item in item_list]
        logger.info("listBef:", listBefore)
        logger.info("listAft:", listAfter)
        assert listBefore!= listAfter, "Reward images did not change after click activating reset button!"
        gemAfter = get_single_resource_amount(self.poco, "gem")
        assert gemAfter == gemBefore - gem_reset,f"gem amount did not decrease by {gem_reset} after click active reset button! Before: {gemBefore}, After: {gemAfter}"
    def check_day_countdown(self):
        assert self.shop_navigator.card_shop.day_countdown.exists(), "PanelResetDay countdown not found!"
        second1=parse_countdown_text(self.shop_navigator.card_shop.day_countdown.get_text())
        time.sleep(2)
        second2=parse_countdown_text(self.shop_navigator.card_shop.day_countdown.get_text())
        assert second2 < second1, "Countdown not decreasing!"
    def get_currency_amount(self,logger):
        balance_of_currency.update({
            "gold": get_single_resource_amount(self.poco, "gold"),
            "energy": get_single_resource_amount(self.poco, "energy"),
            "gem": get_single_resource_amount(self.poco, "gem")
        })
        logger.info("balance_of_currency:", balance_of_currency)


def parse_countdown_text(countdown_text):
    """
    Parses the countdown text to extract hours, minutes, and seconds.
    Example input: "00:01:23"
    Returns a tuple (hours, minutes, seconds).
    """
    match = re.match(r'Reset In:\s*(\d{2}):(\d{2}):(\d{2})', countdown_text)
    if not match:
        raise ValueError("Invalid countdown text")
    hours, minutes, seconds = map(int, match.groups())
    return hours * 3600 + minutes * 60 + seconds

def load_card_shop_data(group_number):
    """
        Reads CardShop.csv and
        returns a dict keyed by ItemName, where each value is
        {"quantity": int, "price": int, "currency": str}.
        """
    this_dir = os.path.dirname(__file__)
    print("::::::Current directory:", this_dir)
    csv_path = os.path.abspath(os.path.join(this_dir, "../../Data/CardShop.csv"))
    group_items = []

    with open(csv_path, encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

        # Define group ranges (excluding empty lines)
        groups = {
            1: (0, 3),  # First 3 items
            2: (4, 16),  # Next 13 items
            3: (17, 29)  # Remaining items
        }

        start, end = groups[group_number]
        for row in rows[start:end]:
            name = row["ItemName"].strip()
            item_data = {
                "quantity": int(row["Quantity"]),
                "price": int(row["Price"].replace(",", "").strip()),
                "currency": row["Currency"].strip().lower()
            }
            group_items.append((name, item_data))
    return group_items
