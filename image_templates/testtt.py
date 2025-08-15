# -*- encoding=utf8 -*-
__author__ = "9999"

from airtest.core.api import *
from airtest.cli.parser import cli_setup
from poco.drivers.unity3d import UnityPoco
if not cli_setup():
    auto_setup(__file__, logdir=True, devices=["android://127.0.0.1:5037/emulator-5562?",])

poco=UnityPoco()
# script content
print("start...")

poco("PanelWorldInfo")
btn=poco("GridElement").child("ElementWorld(Clone)")[0].child("ButtonGo")
title=poco("GridElement").child("ElementWorld(Clone)")[0].child("lTitleWorld")
print(title.get_text())
btn.click()
# poco("GridElement").child("ElementWorld(Clone)")[4].child("ButtonGo").click()
poco("PopupSelectLevelHome(Clone)poco("B_Worlds")")print("endddd")