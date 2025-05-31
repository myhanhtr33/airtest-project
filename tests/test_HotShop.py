from airtest.core.api import *
from utils import base_test
from utils.base_test import BaseTest
from Hierarchy.ShopNavigator import *
import re
from poco.drivers.android.uiautomation import AndroidUiautomationPoco

class TestHotShop(BaseTest):
    def __init__(self,shop_navigator):
        super().__init__()