# -*- encoding=utf8 -*-
__author__ = "9999"
import time
import pytest
import sys
import os
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(project_root)
from airtest.core.api import *
from airtest.cli.parser import cli_setup
from pocounit.case import PocoTestCase
from airtest.cli.parser import cli_setup
from pocounit.addons.poco.action_tracking import ActionTracker
from poco.drivers.unity3d import UnityPoco
from utils.device_setup import connect_to_unity
# if not cli_setup():
#     auto_setup(__file__, logdir=True, devices=["android://127.0.0.1:5037/emulator-5554?cap_method=MINICAP&&ori_method=MINICAPORI&&touch_method=MINITOUCH",])

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
poco= None

def panelInteract(shopname=""):
    panel= poco("PanelNavigateResource")
    grid=panel.offspring("Grid")
    children = grid.children()
    num_children = len(children)
    childTitle=[]
    for child in children:
        childTitle.append(child.child("lTitle"))
    #     print(childTitle.get_text())
    for title in childTitle:
        print(title.get_text())
    result1=(Template(r"../image/botRightBackBtn.png", record_pos=(-0.42, 0.914), resolution=(900, 1800)))
    result2=poco("BtnHome")
    count=0
    for child in children:


        btnGo=child.child("ButtonGo")
        if btnGo.exists():
            btnGo.click()
            print(f"{childTitle[count].get_text()} click GO")    
            if exists(result1):
                touch(result1)
            elif result2.exists():
                result2.click()
            else:
                print("unexpected result")
            if count==len(children)-1:
                print(f"done buy all in {shopname}")
                break
            shop=poco(shopname)
            if shop.exists():
                shop.click()
                print(f"click on {shop}")
            else: 
                print(f"at{count} cannotfind shop {shop} ")
                break
            count+=1
        else:
            print("cannot find btnGo")
            break

def runTest():
    shopBtnTitle = ["lGold", "lEnergy", "lGem"]
    title = [poco("CurrencyBar").offspring("lGold"), poco("CurrencyBar").offspring("lEnergy"),
             poco("CurrencyBar").offspring("lGem")]
    popup = [Template(r"../image/goldPanelTitle.png", record_pos=(-0.002, -0.38), resolution=(900, 1800)),
             Template(r"../image/energyPanelTitle.png", record_pos=(-0.001, -0.381), resolution=(900, 1800)),
             Template(r"../image/gemPanelTitle.png", record_pos=(-0.001, -0.378), resolution=(900, 1800))]
    count1 = 0
    for i in title:
        tit = shopBtnTitle[count1]

        while not exists(popup[count1]):
            i.click()

        #     print(f"CLICK ON {i}")
        #     print(f"title {tit}")
        #     touch((415,1500))

        panelInteract(tit)
        count1 += 1
# runTest()
# for i in children:
#     print (f"children {i}")

# print(num_children)
# childrenName=[]
# for child in children:
#     childrenName.append(child)
# for name in childrenName: 
#     print(f"name {name}")
    
    
# poco("Grid").child("ElementDirector(Clone)")[0].child("ButtonGo")


# generate html report
# from airtest.report.report import simple_report
# simple_report(__file__, logpath=True)
