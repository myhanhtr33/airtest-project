from airtest.core.api import *
# from popupSurprise import CommonCase
from airtest.core.api import *
from poco.drivers.unity3d import UnityPoco
from utils.device_setup import connect_to_unity
# dev1=connect_device("android://127.0.0.1:5037/emulator-5554")
poco=connect_to_unity()
gold= "UI Root/CurrencyBar/Anchor/root/Gold_Home/lGold"
# poco("CurrencyBar").offspring("lGold")
poco(gold).click()
poco("HomeSquad_2").offspring("BtnRightDrone").child("btnBG").click()
poco("CurrencyBar").offspring("GoldHome").child("IGold")
poco("IconShop").click()
poco("CurrencyBar").offspring("Icon").click()
poco("TabShopNavigator(Clone)").offspring("TabGemShop ")
poco("TabNavigator").offspring("BtnHome")
poco("HomeSquad_1").offspring("BtnAircraft")
poco("PopupSpecialVideoReward(Clone)")
poco(texture="btn_back").click()
