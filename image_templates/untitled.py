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
# class SurvivePanel:
#     def __init__(self,root):
#         self.root= root if root.exists() else None
#     @property
#     def title(self):
#         node=self.root.offspring("lLabelTitle")
#         return node.get_text().strip() if node.exists() else None
#     @property
#     def description(self):
#         node=self.root.offspring("lLabelDescription")
#         return node.get_text().strip() if node.exists() else None

# panels= []
# for i in range(1,4):
#     panel_node=poco("UI INGAME (1)").offspring("panelItemBonus").offspring(f"Item{i}")
#     panels.append(SurvivePanel(panel_node))

# for p in panels:
#     print(str(p.root))



    

