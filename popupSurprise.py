# -*- encoding=utf8 -*-
__author__ = "9999"
import time
# import pytest
from airtest.core.api import *
from airtest.cli.parser import cli_setup
from pocounit.case import PocoTestCase
from airtest.cli.parser import cli_setup
from pocounit.addons.poco.action_tracking import ActionTracker
if not cli_setup():
    auto_setup(__file__, logdir=True, devices=["android://127.0.0.1:5037/emulator-5554?cap_method=MINICAP&&ori_method=MINICAPORI&&touch_method=MINITOUCH",])

class CommonCase(PocoTestCase):
    @classmethod
    def setUpClass(cls):
        super(CommonCase, cls).setUpClass()
        cls.poco = Poco(...)

        action_tracker = ActionTracker(cls.poco)
        cls.register_addon(action_tracker)
    def say(self):
        return "heloo000000000000000000"
     

# script content
print("start...")



# generate html report
# from airtest.report.report import simple_report
# simple_report(__file__, logpath=True)
