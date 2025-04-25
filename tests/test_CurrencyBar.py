from Hierarchy.CurrencyBar import *
from airtest.core.api import *
from image_templates.Image_currencyBar import *
from utils.device_setup import PocoManager
from poco.drivers.unity3d import UnityPoco
import sys
import os


poco = PocoManager.get_poco()
bar = CurrencyBar(poco)


def back_to_home():
    home_button = poco("TabNavigator").offspring("BtnHome")
    assert home_button.exists(), "Home button not found!"
    home_button.click()
    sleep(1)  # Wait for the click action to take effect
    assert poco("HomeSquad_1").offspring("BtnAircraft").exists(), "Failed to return to home!"

def run_all_currency_bar_tests():
    print("Running Currency Bar tests...")
    test_gold_ui_elements()
    test_energy_ui_elements()
    test_gem_ui_elements()
    test_video_ui_elements()
    print("✅ All Currency Bar tests passed!")

def test_gold_ui_elements():
    assert bar.gold_home.gold_icon().exists(), "Gold icon not found!"
    assert bar.gold_home.gold_plus_btn().exists(), "Gold plus button missing!"
    assert bar.gold_home.gold_amount().exists(), "Gold amount label not found!"
    test_click_plus_btn(bar.gold_home.gold_plus_btn())
    # goldNavigatePanel = Template(get_resource_path("../image/goldPanelTitle.png"), record_pos=(-0.002, -0.38), resolution=(900, 1800))
    panel_check(goldNavigatePanel, bar.gold_home.gold_amount())

def test_energy_ui_elements():
    assert bar.energy_home.energy_icon().exists(), "Energy icon not found!"
    assert bar.energy_home.energy_plus_btn().exists(), "Energy plus button missing!"
    assert bar.energy_home.energy_amount().exists(), "Energy amount label not found!"
    test_click_plus_btn(bar.energy_home.energy_plus_btn())
    # energyNavigatePanel = Template(get_resource_path("../image/energyPanelTitle.png"), record_pos=(-0.001, -0.381), resolution=(900, 1800))
    panel_check(energyNavigatePanel,bar.energy_home.energy_amount())

def test_gem_ui_elements():
    assert bar.gem_home.gem_plus_btn().exists(), "Gem plus button not found!"
    assert bar.gem_home.gem_icon().exists(), "Gem icon not found!"
    assert bar.gem_home.gem_amount().exists(), "Gem amount label not found!"
    test_click_plus_btn(bar.gem_home.gem_plus_btn())
    # energyNavigatePanel = Template(get_resource_path("../image/gemPanelTitle.png"), record_pos=(-0.001, -0.378), resolution=(900, 1800))
    panel_check(gemNavigatePanel,bar.gem_home.gem_amount())

def test_video_ui_elements():
    assert bar.video_home.video_icon().exists(), "Video icon not found!"
    bar.video_home.video_icon().click()
    assert poco("PopupSpecialVideoReward(Clone)").exists(), "Video popup not found!"
    poco(texture="btn_back").click() #back to home

def test_click_plus_btn(button):
    button.click()
    sleep(1)  # Wait for the click action to take effect
    gemShop= poco("TabShopNavigator(Clone)").offspring("TabGemShop ")
    assert gemShop.exists(), "Gem Shop not found!"
    back_to_home()

def panel_check(panelImage,btn):
    btn.click()
    assert exists(panelImage), f"{panelImage} not found!"
    btn.click()
    assert poco("HomeSquad_1").offspring("BtnAircraft").exists(), "Failed to return to home!"


