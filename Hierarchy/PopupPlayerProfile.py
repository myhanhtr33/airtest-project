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
        self.champion_group = ChampionLeagueGroup(self.root)

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
        self.icon = self.root.offspring("sPVP")
        # — Tier 1 (1v1) —
        panel1= self.root.offspring("panel1v1_Tier1")
        self.tier1_label = panel1.child("l1v1")
        self.tier1_split = panel1.offspring("sSplit")
        self.tier1_rank = panel1.child("lRank")
        self.tier1_elo = panel1.child("lElo")
        self.tier1_rank_icon = panel1.offspring("sRank")
        self.tier1_total_win = panel1.child("lTotalWin")
        self.tier1_win_rate = panel1.child("lWinRate")
        # — Tier 2 (1v1) —
        panel2 = self.root.offspring("panel1v1_Tier2")
        self.tier2_label = panel2.child("l1v1")
        self.tier2_split = panel2.offspring("sSplit")
        self.tier2_rank = panel2.child("lRank")
        self.tier2_elo = panel2.child("lElo")
        self.tier2_rank_icon = panel2.offspring("sRank")
        self.tier2_total_win = panel2.child("lTotalWin")
        self.tier2_win_rate = panel2.child("lWinRate")
        # — 2v2 panel —
        panel2v2 = self.root.offspring("panel2v2")
        self.vs2_label = panel2v2.child("l2v2")
        self.vs2_split = panel2v2.offspring("sSplit")
        self.vs2_rank = panel2v2.child("lRank")
        self.vs2_score = panel2v2.child("lElo")
        self.vs2_rank_icon = panel2v2.offspring("sRank")
        self.vs2_total_win = panel2v2.child("lTotalWin")
        self.vs2_win_rate = panel2v2.child("lWinRate")

    def get_t1_stats(self):
        return{
            "label": self.tier1_label.get_text(), #PvP Tier 1
            "rank": self.tier1_rank.get_text(), #Silver V
            "elo": self.tier1_elo.get_text(), #[999999]ELO:[-] 1176[-]
            "rank_icon": self.tier1_rank_icon.attr("texture"), # texture :  b'PVP_rank_2'
            "total_win": self.tier1_total_win.get_text(), #[999999]Total win:[-] 16[-]
            "win_rate": self.tier1_win_rate.get_text()
        }
    def get_t2_stats(self):
        return {
            "label": self.tier2_label.get_text(),
            "rank": self.tier2_rank.get_text(),
            "elo": self.tier2_elo.get_text(),
            "rank_icon": self.tier2_rank_icon.attr("texture"),
            "total_win": self.tier2_total_win.get_text(),
            "win_rate": self.tier2_win_rate.get_text()
        }
    def get_vs2_stats(self):
        return {
            "label": self.vs2_label.get_text(),
            "rank": self.vs2_rank.get_text(),
            "elo": self.vs2_score.get_text(),
            "rank_icon": self.vs2_rank_icon.attr("texture"),
            "total_win": self.vs2_total_win.get_text(),
            "win_rate": self.vs2_win_rate.get_text()
        }

class EndlessGroup:
    def __init__(self, stat_tab):
        self.root = stat_tab.offspring("GroupEndless")
        self.icon = self.root.child("sEndless")
        self.title = self.root.offspring("lEndless")
        self.text = self.root.offspring("lNormal")
        self.best_score = self.root.offspring("lValue")

class ChampionLeagueGroup:
    def __init__(self, stat_tab):
        self.root = stat_tab.offspring("GroupChampionLeague")
        self.icon = self.root.child("sIcon")
        self.title = self.root.offspring("lChamp")
        self.total_point= self.root.offspring("lTotalPoint")
        self.best_point = self.root.offspring("lMaxPoint")
        self.top1_num= self.root.offspring("lNumTop1")
    def get_stats(self):
        return{
            "total": self.total_point.get_text(),
            "best": self.best_point.get_text(),
            "top1": self.top1_num.get_text()
        }
class PopupOtherPlayerProfile:
    def __init__(self,poco):
        self.poco=poco
        self.root=poco("PopupPlayerProfile(Clone)")
        self.btnBack=self.root.child("B_Back")
        self.title=self.root.offspring("panelLabelTitle")
        self.player_ava= self.root.offspring("sAvatar2D")
        self.player_flag= self.root.offspring("sFlag")
        self.player_name= self.root.offspring("lName")
        self.player_id= self.root.offspring("lId")
        self.btn_name_clan= self.root.offspring("lNameClan")
        self.vip_icon= self.root.offspring("sVipIcon")
        self.btn_asset= self.root.offspring("DetailProfile").offspring("bAsset")
        self.btn_stat= self.root.offspring("DetailProfile").offspring("bStatic")



