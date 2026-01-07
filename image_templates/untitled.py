# -*- encoding=utf8 -*-
__author__ = "9999"

from airtest.core.api import *
from airtest.cli.parser import cli_setup

if not cli_setup():
    auto_setup(__file__, logdir=True, devices=["android://127.0.0.1:5037/emulator-5554?",])


from poco.drivers.unity3d import UnityPoco
poco = UnityPoco()


# script content
print("start...")


# generate html report
# from airtest.report.report import simple_report
# simple_report(__file__, logpath=True
Template(r"tpl1766631100924.png", record_pos=(0.254, 0.511), resolution=(900, 1800))
poco("item0")poco("PopupMilitaryGetPoint(Clone)").offspring("Scrollviewpoco("PopupMilitaryGetPoint(Clone)").offspring("Grid")")