﻿import time
class UIButtonUtils:
    @staticmethod
    def _check_sprite_state(btn, expected_active):
        active_sprite_node = btn.offspring("SpriteActive")
        active_sprite = active_sprite_node if active_sprite_node.exists() else None
        inactive_sprite_node = btn.offspring("Sprite")
        inactive_sprite = inactive_sprite_node if inactive_sprite_node.exists() else None
        if expected_active:
            return active_sprite and not inactive_sprite
        else:
            return inactive_sprite and not active_sprite
    @staticmethod
    def check_sprite_btn_active(btn):
        return UIButtonUtils._check_sprite_state(btn, expected_active=True)
    @staticmethod
    def check_sprite_btn_inactive(btn):
        return UIButtonUtils._check_sprite_state(btn, expected_active=False)

class PopupLeaderboard:
    def __init__(self,poco):
        self.poco=poco
        self.root = poco("PopupLeaderboardAll(Clone)")
    @property
    def btn_close(self):
        return self.root.offspring("B_Back")
    @property
    def btn_player(self):
        return self.root.offspring("btnPlayer")
    @property
    def btn_clan(self):
        return self.root.offspring("btnClan")
    @property
    def tab_player(self):
        tab_player_node = self.root.offspring("TabPlayer")
        return tab_player_node if tab_player_node.exists() else None
    @property
    def tab_clan(self):
        tab_clan_node = self.root.offspring("TabClan")
        return tab_clan_node if tab_clan_node.exists() else None

class TabPlayer:
    def __init__(self,poco):
        self.poco=poco
    @property
    def root(self):
        return self.poco("PopupLeaderboardAll(Clone)").offspring("TabPlayer")
    @property
    def btn_world(self):
        return self.root.offspring("btnWorld")
    @property
    def btn_local(self):
        return self.root.offspring("btnLocal")
    @property
    def btn_friends(self):
        return self.root.offspring("btnFriend")
    @property
    def btn_campaign(self):
        return self.root.offspring("btnCampaign")
    @property
    def btn_league(self):
        return self.root.offspring("btnLeague")
    @property
    def btn_pvpT1(self):
        return self.root.offspring("btnPvpTier1")
    @property
    def btn_pvpT2(self):
        return self.root.offspring("btnPvpTier2")
    @property
    def btn_2v2(self):
        return self.root.offspring("btn2v2")
    @property
    def title(self):
        title_node = self.root.offspring("lTitle")
        return title_node.get_text() if title_node.exists() else None
    @property
    def top3_name(self):  # not exists in hierarchy if don't get SC
        names = []
        for i in range(1, 4):
            name_node = self.root.offspring(f"lNameTop{i}")
            names.append(name_node.get_text() if name_node.exists() else None)
        return names
    @property
    def top3_ava(self):  # not exists in hierarchy if don't get SC
        avatars = []
        for i in range(1, 4):
            ava_node = self.root.offspring(f"UIProfile ({i})")
            avatars.append(ava_node if ava_node.exists() else None)
        return avatars
    @property
    def loading_icon(self):
        icon_node = self.root.offspring("Fx_Loading_Cuonglh")
        return icon_node if icon_node.exists() else None
    # @property
    # def players(self):
    #     """Returns a lazy list that creates ItemPlayer objects only when accessed"""
    #     # start_time = time.time()
    #     result = LazyPlayerList(self.root.offspring("Scroll View").child("content"))
    #     # execution_time = time.time() - start_time
    #     # print(f"players() property access time: {execution_time:.4f} seconds")
    #     return result
    @property
    def players(self):
        _players = []
        for player in self.root.offspring("Scroll View").child("content").children():
            _players.append(ItemPlayer(player))  # 20x __init__ calls
        return _players
    def get_player_count(self):
        """Quick method to get player count without creating objects"""
        return len(self.root.offspring("Scroll View").child("content").children())

class TabClan:
    def __init__(self,poco):
        self.poco=poco
    @property
    def root(self):
        return self.poco("PopupLeaderboardAll(Clone)").offspring("TabClan")
    @property
    def btn_world(self):
        return self.root.offspring("btnWorld")
    @property
    def btn_local(self):
        return self.root.offspring("btnLocal")
    @property
    def btn_upgrade(self):
        return self.root.offspring("btnUpgrade")
    @property
    def btn_glory(self):
        return self.root.offspring("btnGlory")
    @property
    def btn_clan_war(self):
        return self.root.offspring("btnClanWar")
    @property
    def btn_zodiac(self):
        return self.root.offspring("btnZodiac")
    @property
    def title(self):
        node = self.root.offspring("lTitle")
        return node.get_text() if node.exists() else None
    @property
    def top3_name(self):
        names = []
        for i in range(1, 4):
            node = self.root.offspring(f"lNameTop{i}")
            names.append(node.get_text() if node.exists() else None)
        return names
    @property
    def top3_ava(self):
        avatars = []
        for i in range(1, 4):
            node = self.root.offspring(f"sAvatarTop{i}")
            avatars.append(node if node.exists() else None)
        return avatars
    @property
    def loading_icon(self):
        node = self.root.offspring("Fx_Loading_Cuonglh")
        return node if node.exists() else None
    @property
    def clans(self):
        start_time = time.time()
        _clans=[]
        for clan in self.root.offspring("Scroll View").child("content").children():
            _clans.append(ItemClan(clan))
        execution_time = time.time() - start_time
        print(f"clans() execution time: {execution_time:.4f} seconds")
        return _clans
class ItemClan:
    def __init__(self,node):
        self.root=node
    @property
    def sprite_index_top3(self):
        node = self.root.offspring("sTop")
        return node.attr("texture") if node.exists() else None
    @property
    def index_beyond_top3(self):
        node = self.root.offspring("lTop")
        return node.get_text() if node.exists() else None
    @property
    def profile_pic(self):
        node = self.root.offspring("sAvatar")
        return node.attr("texture") if node.exists() else None
    @property
    def name(self):
        node = self.root.offspring("lName")
        return node.get_text() if node.exists() else None

class ItemPlayer:
    def __init__(self,node):
        self.root=node
    @property
    def index(self):
        """
        Returns the index of the player:
        - If sprite_index_top3 is not None, returns 1, 2, or 3 depending on the texture value.
        - If index_beyond_top3 is not None, returns its value.
        """
        sprite_map = {
            "UI5_TopPlayer_Num_1": 1,
            "UI5_TopPlayer_Num_2": 2,
            "UI5_TopPlayer_Num_3": 3,
        }
        sprite = self.sprite_index_top3
        if sprite is not None:
            return sprite_map.get(sprite, None)
        idx = self.index_beyond_top3
        if idx is not None:
            return int(idx)
        return None

    @property
    def sprite_index_top3(self):
        node = self.root.offspring("sTop")
        return node.attr("texture") if node.exists() else None
    @property
    def index_beyond_top3(self):
        node = self.root.offspring("lTop")
        return node.get_text() if node.exists() else None
    @property
    def profile_pic(self):
        return self.root.offspring("UIProfile")  # group contains avatar + frame
    @property
    def flag(self):
        return self.root.offspring("sFlag")
    @property
    def name(self):
        node = self.root.offspring("lName")
        return node.get_text() if node.exists() else None
    @property
    def id(self):
        node = self.root.offspring("lId")
        return node.get_text() if node.exists() else None
    @property
    def clan(self):
        node = self.root.offspring("lClan")
        return node.get_text() if node.exists() else None
    @property
    def campaign_stat(self):
        campaign_node = self.root.offspring("campaign")
        return CampaignStat(campaign_node) if campaign_node.exists() else None
    @property
    def league_stat(self):
        league_node = self.root.offspring("champion")
        return LeagueStat(league_node) if league_node.exists() else None
    @property
    def pvp_stat(self): #pvp tier 1, pvp tier 2
        pvp_node = self.root.offspring("pvp")
        return PvPStat(pvp_node) if pvp_node.exists() else None
    @property
    def vs2_stat(self):
        vs2_node = self.root.offspring("2v2")
        return Vs2Stat(vs2_node) if vs2_node.exists() else None

class CampaignStat:
    def __init__(self,node):
        self.root=node
        node = self.root.offspring("lTitleLevel")
        self.level_title = node.get_text() if node.exists() else None
        node = self.root.offspring("lLevel")
        self.level_value = node.get_text() if node.exists() else None
        self.star_icons = []
        for i in range(3):
            tag = "sStar" if i == 0 else f"sStar ({i})"
            icon_node = self.root.offspring(tag)
            self.star_icons.append(icon_node if icon_node.exists() else None)
        node = self.root.offspring("lStar")
        self.star_value = node.get_text() if node.exists() else None
class LeagueStat:
    def __init__(self,node):
        self.root=node
        node_score = self.root.offspring("lChampionScore")
        self.score = node_score.get_text() if node_score.exists() else None
        node_score_icon = self.root.offspring("sScore")
        self.score_icon = node_score_icon.attr("texture") if node_score_icon.exists() else None
class PvPStat:
    def __init__(self,node):
        self.root=node
        node_rank = self.root.offspring("lRank")
        self.rank_value = node_rank.get_text() if node_rank.exists() else None #Master III
        node_rank_icon = self.root.offspring("sRank")
        self.rank_icon = node_rank_icon.attr("texture") if node_rank_icon.exists() else None
        node_elo = self.root.offspring("lElo")
        self.elo = node_elo.get_text() if node_elo.exists() else None #ELO: 2488
class Vs2Stat:
    def __init__(self,node):
        self.root=node
        node_score = self.root.offspring("lScore")
        self.score = node_score.get_text() if node_score.exists() else None #Season score: 1,751
        node_rank_icon = self.root.offspring("sRank")
        self.rank_icon = node_rank_icon.attr("texture") if node_rank_icon.exists() else None #it could be ""
        node_rank_value = self.root.offspring("lRankPVP")
        self.rank_value = node_rank_value.get_text() if node_rank_value.exists() else None #Silver, it could be ""
class LazyPlayerList:
    """Lazy list that creates ItemPlayer objects only when accessed"""
    def __init__(self, content_node):
        self.content_node = content_node
        self._children = None  # Cache children nodes

    def _get_children(self):
        if self._children is None:
            raw_children = self.content_node.children()
            # raw_children is a UIObjectProxy that may contain mixed types
            # We need to flatten it to get all individual player nodes
            self._children = []

            for item in raw_children:
                if isinstance(item, list):
                    # If it's a nested list, extend with all items from the list
                    self._children.extend(item)
                elif hasattr(item, 'exists'):
                    # If it's a UI node, add it directly
                    self._children.append(item)

            # print(f"DEBUG: Flattened {len(raw_children)} raw items into {len(self._children)} individual UI children")
        return self._children

    def __len__(self):
        children = self._get_children()
        # print(f"DEBUG: LazyPlayerList.__len__() returning {len(children)}")
        return len(children)

    def __getitem__(self, index):
        start_time = time.time()
        children = self._get_children()

        if isinstance(index, slice):
            # Let's see what's happening with the slice
            # start = index.start or 0
            # stop = index.stop or len(children)
            # step = index.step or 1
            # print(f"DEBUG: Slice parameters - start:{start}, stop:{stop}, step:{step}")

            sliced_children = children[index]
            # print(f"DEBUG: Slice {index} resulted in {len(sliced_children)} children")

            # Debug: Check each sliced child
            for i, child in enumerate(sliced_children):
                exists = child.exists() if hasattr(child, 'exists') else 'No exists method'
                # print(f"DEBUG: Sliced child {i}: exists={exists}, type={type(child)}")

            result = [ItemPlayer(child) for child in sliced_children]
            # print(f"DEBUG: Created {len(result)} ItemPlayer objects")
            execution_time = time.time() - start_time
            print(f"__getitem__() execution time: {execution_time:.4f} seconds")
            return result
        execution_time = time.time() - start_time
        print(f"__getitem__() execution time: {execution_time:.4f} seconds")
        return ItemPlayer(children[index])

    def __iter__(self):
        for child in self._get_children():
            yield ItemPlayer(child)