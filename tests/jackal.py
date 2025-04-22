# -*- encoding=utf8 -*-
__author__ = "9999"

from airtest.core.api import *
from airtest.cli.parser import cli_setup

if not cli_setup():
    auto_setup(__file__, logdir=True, devices=["android://127.0.0.1:5037/emulator-5554?",])


# script content
print("start...")


# generate html report
# from airtest.report.report import simple_report
# simple_report(__file__, logpath=True)
swipe(Template(r"tpl1744717078219.png", record_pos=(-0.032, -0.376), resolution=(900, 1800)), vector=[-500, -200])
item=[Template(r"tpl1744717709233.png", record_pos=(-0.307, -0.313), resolution=(900, 1800)),Template(r"tpl1744717728942.png", record_pos=(0.001, -0.312), resolution=(900, 1800)),Template(r"tpl1744717785796.png", record_pos=(0.3, -0.313), resolution=(900, 1800)),Template(r"tpl1744717811763.png", record_pos=(-0.306, 0.081), resolution=(900, 1800)),Template(r"tpl1744717831944.png", record_pos=(-0.001, 0.077), resolution=(900, 1800)),Template(r"tpl1744717852045.png", record_pos=(0.302, 0.083), resolution=(900, 1800))]
btn=[(150,713),(450,713),(750,713),(150,1065),(450,1065),(750,1065)]
# for i in item: 
#     if exists(i):
#         touch(btn[item.index(i)])
#         print(f"buy pack {item.index(i)}")
#     else:
#         print("aloloo")
       
count=0
print(len(item))
while count<len(item):
    if exists(item[count]):      
        touch(btn[count])
        print(f"buy pack {count}")
    else:
        print("aloloo")
    count+=1
        
        