class PopupPlayerProfile:
    def __init__(self,poco):
        self.poco=poco
        self.root=poco("PopupPlayerProfile(Clone)")
        self.btnBack=self.root.child("B_Back")
        self.title=self.root.offspring("panelLabelTitle")
        self.player_ava= self.root.offspring("sAvatar")
        self.player_flag= self.root.offspring("sFlag")
        self.player_name= self.root.offspring("lName")
        self.player_id= self.root.offspring("lId")
        self.btn_name_clan= self.root.offspring("lNameClan")
        self.vip_icon= self.root.offspring("sVipIcon")
        self.btn_edit_profile= self.root.offspring("SocialInteractive").offspring("bEdit")
        self.btn_FB= self.root.offspring("SocialInteractive").offspring("bFb") if self.root.child("SocialInteractive").offspring("bFb").exists() else None
        self.btn_asset= self.root.offspring("DetailProfile").offspring("bAsset")
        self.btn_stat= self.root.offspring("DetailProfile").offspring("bStatic")
        self.asset_tab= AssetTab(self.root)
        self.stat_tab= StatTab(self.root)

class AssetTab:
    def __init__(self,popup_player_profile):
        self.root= popup_player_profile.offspring("DetailProfile").offspring("ContentAsset")
        self.btn_squad1=self.root.offspring("B_Squad (1)")
        self.btn_squad2=self.root.offspring("B_Squad (2)")
        self.btn_squad3=self.root.offspring("B_Squad (3)")
        # deactive= texture :  b'UI5_Squad_Tab1'
        # active texture :  b'UI5_Squad_Tab2
        # group squad
        self.plane= self.root.child("Squad").offspring("BtnAircraft")
        self.left_drone= self.root.child("Squad").offspring("BtnLeftDrone")
        self.right_drone= self.root.child("Squad").offspring("BtnRightDrone")
        self.wing= self.root.child("Squad").offspring("BtnWing")
        self.engines=[]
        for i in range(1,7):
            node= self.root.child("Squad").offspring(f"B_Engine_{i}")
            self.engines.append(EngineItem(node))
        self.pilot=PilotItem(self.root)
        self.military= self.root.child("Squad").offspring("BtnMilitary")
        #panel info
        self.energyBG=self.root.child("panelInfo").child("sBackgroundEnergy")
        self.energyIcon=self.root.child("panelInfo").child("sEnergy")
        self.energyAmount=self.root.child("panelInfo").child("lEnergy")
        self.goldBG=self.root.child("panelInfo").child("sBackgroundGold")
        self.goldIcon=self.root.child("panelInfo").child("sGold")
        self.goldAmount=self.root.child("panelInfo").child("lGold")
        self.gemBG=self.root.child("panelInfo").child("sBackgroundGem")
        self.gemIcon=self.root.child("panelInfo").child("sGem")
        self.gemAmount=self.root.child("panelInfo").child("lGem")
        #bottom group
        self.btn_aircraft= self.root.child("Bottom").offspring("bAircraft")
        self.btn_drone= self.root.child("Bottom").offspring("bDrone")
        self.btn_wing= self.root.child("Bottom").offspring("bWing")
        self.Agroup= self.root.child("Bottom").offspring("AGenerator")
        self.Dgroup= self.root.child("Bottom").offspring("DGenerator")
        self.Wgroup= self.root.child("Bottom").offspring("WGenerator")
        self._items=[]
    @property
    def items(self):
        if self._items is None and self.root.child("Bottom").offspring("Grid").child("HangarItem(Clone)").exists():
            for item in self.root.child("Bottom").offspring("Grid").child("HangarItem(Clone)"):
                self._items.append(HangarItem(item))
            return self._items

class StatTab:
    def __init__(self, popup_player_profile):
        self.root = popup_player_profile.offspring("DetailProfile").offspring("ContentStatistics")
        self.campaign_group = CampaignGroup(self.root)
        self.pvp_group = PvPGroup(self.root)
        self.endless_group = EndlessGroup(self.root)
        self.champion_league_group = ChampionLeagueGroup(self.root)

class EngineItem:
    def __init__(self, node):
        self.root = node
        self.empty_BG = self.root.child("sBG")
        self.rarity_frame= self.root.offspring("sAurora") if self.root.offspring("sAurora").exists() else None
        self.engine_img = self.root.offspring("sEngine") if self.root.offspring("sEngine").exists() else None
        self.engine_star_icon= self.root.offspring("sStar") if self.root.offspring("sStar").exists() else None
        self.engine_star_amount= self.root.offspring("lstar") if self.root.offspring("lstar").exists() else None

class PilotItem:
    def __init__(self, parent):
        self.root = parent.offspring("BtnPilot")
        self.rarity_frame = self.root.offspring("sBG") if self.root.offspring("sBG").exists() else None
        self.pilot_img = self.root.offspring("sPortrait") if self.root.offspring("sPortrait").exists() else None
        self.pilot_flag = self.root.offspring("sNationFlag") if self.root.offspring("sNationFlag").exists() else None
        self.pilot_lv = self.root.offspring("lLevel") if self.root.offspring("lLevel").exists() else None
        self.pilot_star_icon = self.root.offspring("sStar") if self.root.offspring("sStar").exists() else None
        self.pilot_star_amount = self.root.offspring("lStar") if self.root.offspring("lStar").exists() else None

class HangarItem:
    def __init__(self, node):
        self.root = node
        self.item_BG = self.root.child("BG")
        self.item_img = self.root.child("sIcon")
        self.item_lv= self.root.child("lLevel")
        self.item_star_icon = self.root.child("wStar")
        self.item_star_amount = self.root.child("lStar")

class CampaignGroup:
    def __init__(self, stat_tab):
        self.root = stat_tab.offspring("GroupCampaign")
        self.title= self.root.child("sCampaign")
        #normal campaign
        self.normal_title = self.root.child("sNormal").child("lNormal")
        self.normal_lv= self.root.child("sNormal").child("lValue")
        self.normal_star= self.root.child("sNormal").child("lValueStar")
        self.normal_star_icon = self.root.child("sNormal").child("sStar") #texture :  b'UI5_SelectLevel_Normal_Star_1'
        #hard campaign
        self.hard_title = self.root.child("sHard").child("lHard")
        self.hard_lv = self.root.child("sHard").child("lValue")
        self.hard_star = self.root.child("sHard").child("lValueStar")
        self.hard_star_icon = self.root.child("sHard").child("sStar") #texture :  b'UI5_SelectLevel_Hard_Star_1'
        #hell campaign
        self.hell_title = self.root.child("sHell").child("lHell")
        self.hell_lv = self.root.child("sHell").child("lValue")
        self.hell_star = self.root.child("sHell").child("lValueStar")
        self.hell_star_icon = self.root.child("sHell").child("sStar") #texture :  b'UI5_SelectLevel_Hell_Star_1'
        # total star
        self.total_star_title= self.root.child("lTotalStar")
        self.total_star_amount = self.root.child("lTotalStarValue")

class PvPGroup:
    def __init__(self, stat_tab):
        self.root = stat_tab.offspring("GroupPVP")

class EndlessGroup:
    def __init__(self, stat_tab):
        self.root = stat_tab.offspring("GroupEndless")

class ChampionLeagueGroup:
    def __init__(self, stat_tab):
        self.root = stat_tab.offspring("GroupChampionLeague")



