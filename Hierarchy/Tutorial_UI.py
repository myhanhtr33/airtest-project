import os
from airtest.core.api import Template

current_dir = os.path.dirname(os.path.abspath(__file__))
hand_tut_path= os.path.join(os.path.dirname(current_dir), "image","Tut", "Handtut.png")
npc_img_path = os.path.join(os.path.dirname(current_dir), "image","Tut","NPC.png")
drone1_img_path = os.path.join(os.path.dirname(current_dir), "image","Tut","Drone1.png")
drone2_img_path = os.path.join(os.path.dirname(current_dir), "image","Tut","Drone2.png")
event_icon_path= os.path.join(os.path.dirname(current_dir),"image","Tut","BigIconTut_Event_6.png")


class TutorialManager:
    def __init__(self,poco):
        self.root=poco("TutorialManager")
    @property
    def btn_claim(self): #tut lv5, claim drone from PopupReceiveDrone
        tmp = self.root.offspring("B_Claim")
        return tmp if tmp.exists() else None
    @property
    def btn_left_drone(self): #tut lv5, click left drone position
        tmp = self.root.offspring("BtnLeftDrone")
        return tmp if tmp.exists() else None
    @property
    def btn_equip_drone(self): #tut lv5, click equip drone button
        tmp = self.root.offspring("BtnEquip")
        return tmp if tmp.exists() else None
    @property
    def btn_right_drone(self): #tut lv8, click right drone position
        tmp = self.root.offspring("BtnRightDrone")
        return tmp if tmp.exists() else None
    @property
    def btn_back_from_hangar(self): #tut lv8, click back button from hangar
        tmp = self.root.offspring("BtnBack")
        return tmp if tmp.exists() else None
    @property
    def lv8_event_icon_template(self):
        return Template(event_icon_path)
    @property
    def lv8_panel_description(self): #New feature unlock
        tmp = self.root.offspring("OnClickSkip").offspring("lDesciption")
        return tmp.get_text().strip() if tmp.exists() else None
    @property
    def lv8_panel_title(self): #Continue
        tmp = self.root.offspring("OnClickSkip").offspring("lTitle") #Continue
        return tmp.get_text().strip() if tmp.exists() else None
    @property
    def lv8_hand_click_event_on_navigator_template(self):
        return Template(hand_tut_path,threshold=0.5, rgb=True)
    @property
    def lv8_btn_event_on_navigator(self):
        tmp = self.root.offspring("BtnEvent")
        return tmp if tmp.exists() else None


class PopupNPC:
    def __init__(self,poco):
        self.root = poco("PopupNPCIntroduce")
    @property
    def message(self): #Good job! I have some gift for you
        tmp= self.root.offspring("lMess")
        return tmp.get_text().strip() if tmp.exists() else None
    @property
    def btn_go(self):
        tmp = self.root.offspring("B_Confirm_NPC")
        return tmp if tmp.exists() else None
    @property
    def npc_image_template(self):
        return Template(npc_img_path)

class PopupReceiveDrone:
    def __init__(self,poco):
        self.root = poco("PopupReceiveDroneWingTutorial(Clone)")
    @property
    def drone_group(self):
        node= self.root.offspring("Drone")
        return node if node.exists() else None
    @property
    def drone_name(self):
        node = self.drone_group.offspring("lName") #lv5: GATLING GUN, lv8: DOUBLE GATLING
        return node.get_text().strip() if node.exists() else None
    @property
    def drone_image(self):
        node = self.drone_group.offspring("sIcon")
        return node.attr("texture") if node.exists() else None
    @property
    def drone1_image_template(self):
        return Template(drone1_img_path)
    @property
    def drone2_image_template(self):
        return Template(drone2_img_path)
    @property
    def message(self):
        #Thanks for helping us repel the invading alien. Here is our thank-you gift. Let's try equipping it!
        node = self.root.offspring("L_Message")
        return node.get_text().strip() if node.exists() else None