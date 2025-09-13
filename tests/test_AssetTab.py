from airtest.core.api import *
from Hierarchy.PopupPlayerProfile import *
from utils.get_resource_amount import clean_number
from utils.sprite_mapping import CARD_SPRITE_MAPPING


energy_sprite="Icon_enegy1"
gold_sprite="UI5_Head_Icon_Golds"
gem_sprite="UI5_Head_Icon_Gems"
planes=[]
drones=[]
wings=[]
lens_planes=24
lens_drones=24
lens_wings=24

def get_plane():
    for key in CARD_SPRITE_MAPPING.keys():
        if "PLANE_" in key:
            plane= key.split("_")[-1]
            planes.append(plane)
        if "WINGMAN_" in key:
            drone= key.split("_")[-1]
            drones.append(drone)
        if "WING_" in key:
            wing= key.split("_")[-1]
            wings.append(wing)
    print("Planes:", planes)
    print("Drones:", drones)
    print("Wings:", wings)

class TestAssetTab(BaseTest):
    def __init__(self,popup_player_profile):
        super().__init__()
        self.popup = popup_player_profile

    def run_all_tests(self):
        print("running all AssetTab tests...")
        # self.check_3btn_squad_and_group_squad()
        # self.check_panel_info()
        # get_plane()
        self.check_bottom_group()

    def check_3btn_squad_and_group_squad(self):
        print("checking 3btn_squad...")
        assert self.popup.asset_tab.btn_squad1.exists(), "btn_squad1 not found!"
        self.popup.asset_tab.btn_squad1.click(sleep_interval=1)
        assert self.get_btn_squad_texture(self.popup.asset_tab.btn_squad1)== "UI5_Squad_Tab2", "btn_squad1 active texture not found!"
        assert self.get_btn_squad_texture(self.popup.asset_tab.btn_squad2)== "UI5_Squad_Tab1", "btn_squad2 deactive texture not found!"
        assert self.get_btn_squad_texture(self.popup.asset_tab.btn_squad3)== "UI5_Squad_Tab1", "btn_squad3 deactive texture not found!"
        self.check_group_squad_fully_present()

        assert self.popup.asset_tab.btn_squad2.exists(), "btn_squad2 not found!"
        self.popup.asset_tab.btn_squad2.click(sleep_interval=1)
        assert self.get_btn_squad_texture(self.popup.asset_tab.btn_squad2)== "UI5_Squad_Tab2", "btn_squad2 active texture not found!"
        assert self.get_btn_squad_texture(self.popup.asset_tab.btn_squad1)== "UI5_Squad_Tab1", "btn_squad1 deactive texture not found!"
        assert self.get_btn_squad_texture(self.popup.asset_tab.btn_squad3)== "UI5_Squad_Tab1", "btn_squad3 deactive texture not found!"
        self.check_group_squad_fully_present()


        assert self.popup.asset_tab.btn_squad3.exists(), "btn_squad3 not found!"
        self.popup.asset_tab.btn_squad3.click(sleep_interval=1)
        assert self.get_btn_squad_texture(self.popup.asset_tab.btn_squad3)== "UI5_Squad_Tab2", "btn_squad3 active texture not found!"
        assert self.get_btn_squad_texture(self.popup.asset_tab.btn_squad1)== "UI5_Squad_Tab1", "btn_squad1 deactive texture not found!"
        assert self.get_btn_squad_texture(self.popup.asset_tab.btn_squad2)== "UI5_Squad_Tab1", "btn_squad2 deactive texture not found!"
        self.check_group_squad_fully_present()

    def get_btn_squad_texture(self, btn_squad):
        btn_squad.refresh()
        return btn_squad.child("sBG").attr("texture")

    def check_group_squad_fully_present(self):
        print("checking group_squad_fully_present...")
        assert self.popup.asset_tab.plane.exists(), "plane not found!"
        assert self.popup.asset_tab.left_drone.exists(), "left_drone not found!"
        assert self.popup.asset_tab.right_drone.exists(), "right_drone not found!"
        assert self.popup.asset_tab.wing.exists(), "wing not found!"
        for engine in self.popup.asset_tab.engines:
            assert engine.root.exists(), f"engine {engine} not found!"
            print("checking engine:", engine)
        assert self.popup.asset_tab.pilot.root.exists(), "pilot not found!"
        assert self.popup.asset_tab.military.exists(), "military not found!"

    def check_panel_info(self):
        print("checking panel_info...")
        assert self.popup.asset_tab.energyBG.exists(), "energyBG not found!"
        assert self.popup.asset_tab.energyIcon.exists(), "energyIcon not found!"
        assert self.popup.asset_tab.energyIcon.attr("texture") == energy_sprite, f"energyIcon texture not match! Expected: {energy_sprite}, Found: {self.popup.asset_tab.energyIcon.attr("texture")}"
        assert self.popup.asset_tab.energyAmount.exists(), "energyAmount not found!"
        assert self.popup.asset_tab.goldBG.exists(), "goldBG not found!"
        assert self.popup.asset_tab.goldIcon.exists(), "goldIcon not found!"
        assert self.popup.asset_tab.goldIcon.attr("texture") == gold_sprite, f"goldIcon texture not match! Expected: {gold_sprite}, Found: {self.popup.asset_tab.goldIcon.attr("texture")}"
        assert self.popup.asset_tab.goldAmount.exists(), "goldAmount not found!"
        assert self.popup.asset_tab.gemBG.exists(), "gemBG not found!"
        assert self.popup.asset_tab.gemIcon.exists(), "gemIcon not found!"
        assert self.popup.asset_tab.gemIcon.attr("texture") == gem_sprite, f"gemIcon texture not match! Expected: {gem_sprite}, Found: {self.popup.asset_tab.gemIcon.attr("texture")}"
        assert self.popup.asset_tab.gemAmount.exists(), "gemAmount not found!"
        int_energy_amount=clean_number(self.popup.asset_tab.energyAmount.get_text())
        int_gold_amount=clean_number(self.popup.asset_tab.goldAmount.get_text())
        int_gem_amount=clean_number(self.popup.asset_tab.gemAmount.get_text())
        assert int_energy_amount >= 0, f"Energy amount is negative: {int_energy_amount}"
        assert int_gold_amount >= 0, f"Gold amount is negative: {int_gold_amount}"
        assert int_gem_amount >= 0, f"Gem amount is negative: {int_gem_amount}"

    def check_bottom_group(self):
        print("checking bottom_group...")
        assert self.popup.asset_tab.btn_aircraft.exists(), "btn_aircraft not found!"
        self.popup.asset_tab.btn_aircraft.click(sleep_interval=1)
        assert self.popup.asset_tab.Agroup.exists(), "Agroup not found!"
        self.check_hangar_items("plane")

        assert self.popup.asset_tab.btn_drone.exists(), "btn_drone not found!"
        self.popup.asset_tab.btn_drone.click(sleep_interval=1)
        assert self.popup.asset_tab.Dgroup.exists(), "Dgroup not found!"
        self.check_hangar_items("drone")

        assert self.popup.asset_tab.btn_wing.exists(), "btn_wing not found!"
        self.popup.asset_tab.btn_wing.click(sleep_interval=1)
        assert self.popup.asset_tab.Wgroup.exists(), "Wgroup not found!"
        self.check_hangar_items("wing")

    def check_hangar_items(self, type):
        print(f"checking hangar items of type: {type}...")
        textures=[] # List to store the textures of hangar items
        # Iterate through all items in the hangar and collect their textures.
        for item in self.popup.asset_tab.items:
            texture=item.root.child("sIcon").attr("texture")
            textures.append(texture)
        # Validate hangar items
        if type == "plane":
            if len(self.popup.asset_tab.items)!= lens_planes:
                raise AssertionError(f"Expected {lens_planes} plane items, found {len(self.popup.asset_tab.items)} items in hangar.")
            for tex in textures:
                print(f"checking {tex}...")
                if "aircraft" not in tex:
                    raise AssertionError(f"invalid Plane texture {tex} ")
        if type == "drone":
            if len(self.popup.asset_tab.items)!= lens_drones:
                raise AssertionError(f"Expected {lens_drones} drone items, found {len(self.popup.asset_tab.items)} items in hangar.")
            for tex in textures:
                print(f"checking {tex}...")
                if "wingman" not in tex:
                    raise AssertionError(f"invalid Drone texture {tex}")
        if type =="wing":
            if len(self.popup.asset_tab.items)!= lens_wings:
                raise AssertionError(f"Expected {lens_wings} wing items, found {len(self.popup.asset_tab.items)} items in hangar.")
            for tex in textures:
                print(f"checking {tex}...")
                if "wing" not in tex:
                    raise AssertionError(f"invalid Wing texture {tex} ")
