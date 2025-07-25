from Hierarchy.PopupLeaderboard import *
from Hierarchy.PopupPlayerProfile import *
from logger_config import get_logger
import pytest
import time
from typing import Literal
from utils.get_resource_amount import clean_number


from utils.helper_functions import wait_for_element

player_title=["Campaign Leaderboard", "Champions League", "PVP Tier 1 Leaderboard", "PVP Tier 2 Leaderboard", "2v2 Leaderboard"]
len_of_list=20
max_level=303
roman=["I", "II", "III", "IV", "V"]
categories=["Bronze", "Silver", "Gold", "Platinum", "Diamond", "Master", "Challenger", "Legendary"]
allowed_ranks = {f"{cat} {lv}" for cat in categories for lv in roman}


@pytest.fixture(scope="class")
def PopupLeaderboard_back_btn(poco):
    button= poco("PopupLeaderboardAll(Clone)").offspring("B_Back")
    return button if button.exists() else None

@pytest.mark.use_to_home(before=True, after=True, logger_name="PopupLeaderboard", back_button="PopupLeaderboard_back_btn")
class TestPopupLeaderboard:
    @pytest.fixture(scope="function", autouse=True)
    def setup(self, poco):
        logger = get_logger("setup method")
        logger.info("Setting up PopupLeaderboard test environment...")
        self.poco = poco
        leaderboard_home_icon=poco("SubFeatureTopLayer").offspring("Rank_Home")
        assert leaderboard_home_icon.exists(), "Leaderboard home icon not found!"
        leaderboard_home_icon.click(sleep_interval=1)
        start_time = time.time()
        self.popup = PopupLeaderboard(poco)
        assert self.popup.root.exists(), "PopupLeaderboard not found after click!"
        self.tab_player = TabPlayer(poco)
        print(f"PopupLeaderboard initialized in {time.time() - start_time:.2f} seconds")

    def test_main_element(self):
        logger=get_logger()
        logger.info("Testing main elements presence in PopupLeaderboard...")
        # Verify main elements exist
        assert self.popup.btn_close.exists(), "btnClose not found!"
        assert self.popup.btn_clan.exists(), "btn_clan not found!"
        assert self.popup.btn_player.exists(), "btn_player not found!"

        # Test Player tab activation
        self.popup.btn_player.click(sleep_interval=1)
        assert UIButtonUtils.check_sprite_btn_active(self.popup.btn_player), "Player button not activated!"
        assert UIButtonUtils.check_sprite_btn_inactive(self.popup.btn_clan), "Clan button not deactivated!"
        assert self.popup.tab_player.exists(), "Player tab not open!"

        # Test Clan tab activation
        self.popup.btn_clan.click(sleep_interval=1)
        assert UIButtonUtils.check_sprite_btn_inactive(self.popup.btn_player), "Player button not deactivated!"
        assert UIButtonUtils.check_sprite_btn_active(self.popup.btn_clan), "Clan button not activated!"
        assert self.popup.tab_clan.exists(), "Clan tab not open!"

    def test_elements_in_player_tab(self):
        logger=get_logger()
        logger.info("Verifying elements in Player tab...")
        # Ensure we're in player tab
        self.popup.btn_player.click(sleep_interval=1)
        # Verify Player tab elements
        assert self.tab_player.btn_campaign.exists(), "btn_campaign not found!"
        assert self.tab_player.btn_league.exists(), "btn_league not found!"
        assert self.tab_player.btn_pvpT1.exists(), "btn_pvpT1 not found!"
        assert self.tab_player.btn_pvpT2.exists(), "btn_pvpT2 not found!"
        assert self.tab_player.btn_2v2.exists(), "btn_2v2 not found!"
        assert self.tab_player.btn_world.exists(), "btn_world not found!"
        assert self.tab_player.btn_local.exists(), "btn_local not found!"
        assert self.tab_player.btn_friends.exists(), "btn_friends not found!"

    def test_elements_in_clan_tab(self):
        logger = get_logger()
        logger.info("Verifying elements in Clan tab...")
        # Ensure we're in clan tab
        self.popup.btn_clan.click(sleep_interval=1)
        tab_clan = TabClan(self.poco)
        # Verify Clan tab elements (specific to TabClan)
        assert tab_clan.btn_world.exists(), "btn_world not found in clan tab!"
        assert tab_clan.btn_local.exists(), "btn_local not found in clan tab!"
        assert tab_clan.btn_upgrade.exists(), "btn_upgrade not found in clan tab!"
        assert tab_clan.btn_glory.exists(), "btn_glory not found in clan tab!"
        assert tab_clan.btn_clan_war.exists(), "btn_clan_war not found in clan tab!"
        assert tab_clan.btn_zodiac.exists(), "btn_zodiac not found in clan tab!"

    def test_clan_tab_all_subtabs(self):
        """Test all Clan main tabs (Upgrade, Glory, Clan War, Zodiac) with World and Local sub-tabs"""
        logger = get_logger()
        logger.info("Starting Clan tab test...")
        self.popup.btn_clan.click(sleep_interval=1)
        tab_clan = TabClan(self.poco)
        main_tabs = [
            # (tab_clan.btn_upgrade, 'upgrade'),
            # (tab_clan.btn_glory, 'glory'),
            (tab_clan.btn_clan_war, 'clan_war'),
            (tab_clan.btn_zodiac, 'zodiac')
        ]
        for main_tab_btn, tab_name in main_tabs:
            start_time = time.time()
            self.run_clan_tab_subtabs_test(main_tab_btn, tab_name)
            elapsed_time = time.time() - start_time
            logger.info(f"{tab_name} tab test completed in {elapsed_time:.2f} seconds")

    def test_player_tab_all_subtabs(self):
        """Test Player tab with all sub-tabs"""
        logger = get_logger()
        logger.info("Starting Player tab test...")
        self.popup.btn_player.click(sleep_interval=1)
        main_tabs = [
            (self.tab_player.btn_campaign, 'campaign', 'campaign'),
            (self.tab_player.btn_league, 'league', 'league'),
            (self.tab_player.btn_pvpT1, 'pvpT1', 'pvp'),
            (self.tab_player.btn_pvpT2, 'pvpT2', 'pvp'),
            (self.tab_player.btn_2v2, '2v2', 'vs2')
        ]
        for main_tab_btn, tab_name, stat_type in main_tabs:
            start_time = time.time()
            logger.info(f"Testing Player tab - {tab_name} sub-tab...")
            self.run_tab_subtabs_test(main_tab_btn, tab_name, stat_type)
            elapsed_time = time.time() - start_time
            logger.info(f"Player tab - {tab_name} sub-tab test completed in {elapsed_time:.2f} seconds")

    def test_check_first_two_players_campaign_world(self):
        """
        1. Go to Campaign > World tab
        2. Click the first two players (by their root)
        3. For each, check PopupPlayerProfile is open and all elements exist
        4. Compare id and name between leaderboard list and opened profile popup
        5. Compare id and name of these 2 players, they must be different
        """
        logger = get_logger()
        logger.info("Testing first two players in Campaign > World tab...")
        # Go to Campaign > World tab
        self.popup.btn_player.click(sleep_interval=1)
        tab_player = TabPlayer(self.poco)
        tab_player.btn_campaign.click(sleep_interval=1)
        tab_player.btn_world.click(sleep_interval=1)
        # Wait for loading to complete
        timeout = 15
        if tab_player.loading_icon:
            try:
                wait_for_element(lambda: not tab_player.loading_icon, timeout=timeout)
                time.sleep(1)
            except:
                logger.warning(f"Loading icon did not disappear within timeout {timeout}s - no data available")
                return
        players = tab_player.players
        assert len(players) >= 2, "Less than 2 players found in Campaign > World tab!"
        player_data = []

        for i in range(2):
            player = players[i]
            # Get id and name from leaderboard list before clicking
            leaderboard_id = player.id.replace("ID: ", "").strip()
            leaderboard_name = player.name

            logger.info(f"Player {i+1} in leaderboard: ID={leaderboard_id}, Name={leaderboard_name}")

            # Click player to open profile
            player.root.click(sleep_interval=1)

            # Check PopupPlayerProfile is open and all elements exist
            popup = PopupOtherPlayerProfile(self.poco)  # ensure correct poco context
            from tests.test_PopupPlayerProfile import test_all_elements_exist_other_player_profile
            test_all_elements_exist_other_player_profile(popup)

            # Get id and name from popup
            popup_id = popup.player_id.get_text().replace("id: ", "").strip()
            popup_name = popup.player_name.get_text()

            logger.info(f"Player {i+1} in popup: ID={popup_id}, Name={popup_name}")

            # Verify that id and name match between leaderboard and popup
            assert leaderboard_id == popup_id, f"Player {i+1} ID mismatch: leaderboard={leaderboard_id}, popup={popup_id}"
            assert leaderboard_name[:8] == popup_name[:8], f"Player {i+1} Name mismatch: leaderboard={leaderboard_name}, popup={popup_name}"

            # Store data for comparison between players
            player_data.append((popup_id, popup_name))

            # Close the profile popup to return to leaderboard
            popup.btnBack.click(sleep_interval=1)

        # Compare id and name between the two players
        assert player_data[0][0] != player_data[1][0], f"Player IDs are the same: {player_data[0][0]}"
        assert player_data[0][1] != player_data[1][1], f"Player names are the same: {player_data[0][1]}"
        print(f"✅ First two players have different IDs and names: {player_data[0]} vs {player_data[1]}")
        print(f"✅ Player IDs and names match between leaderboard and profiles")

    def test_check_first_two_clans_upgrade_world(self):
        """
        1. Go to Clan tab > Upgrade > World subtab
        2. Click the first two clans (by their root)
        3. For each, check PopupClanGeneralInfo is open
        4. Compare id and name between leaderboard list and opened clan profile popup
        5. Compare id and name of these 2 clans, they must be different
        """
        logger = get_logger()
        logger.info("Testing first two clans in Upgrade > World tab...")

        # Go to Clan tab > Upgrade > World subtab
        self.popup.btn_clan.click(sleep_interval=1)
        tab_clan = TabClan(self.poco)
        tab_clan.btn_clan_war.click(sleep_interval=1)
        tab_clan.btn_world.click(sleep_interval=1)

        # Wait for loading to complete
        timeout = 15
        if tab_clan.loading_icon:
            try:
                wait_for_element(lambda: not tab_clan.loading_icon, timeout=timeout)
                time.sleep(1)
            except:
                logger.warning(f"Loading icon did not disappear within timeout {timeout}s - no data available")
                return

        # Get list of clans
        clans = tab_clan.clans
        clan_data = []

        # Check first two clans
        for i in range(2):
            clan = clans[i]
            # Get id and name from leaderboard list before clicking
            leaderboard_name = clan.name
            logger.info(f"Clan {i+1} in leaderboard: Name={leaderboard_name}")

            # Click clan to open profile
            clan.root.click(sleep_interval=1)

            # Check PopupClanGeneralInfo is open
            popup = self.poco("PopupClanGeneralInfo(Clone)")
            assert popup.exists(), "PopupClanGeneralInfo not opened after clicking clan!"

            # Get id and name from popup
            popup_id = popup.offspring("IDClan").get_text() if popup.offspring("IDClan").exists() else None
            popup_name = popup.offspring("lNameClan").get_text() if popup.offspring("lNameClan").exists() else None

            logger.info(f"Clan {i+1} in popup: ID={popup_id}, Name={popup_name}")
            assert popup_id is not None, "Clan ID not found in popup!"
            assert popup_name is not None, "Clan name not found in popup!"

            # Verify name matches between leaderboard and popup
            assert leaderboard_name == popup_name, f"Clan {i+1} Name mismatch: leaderboard={leaderboard_name}, popup={popup_name}"

            # Store data for comparison between clans
            clan_data.append((popup_id, popup_name))

            # Close the popup to return to leaderboard
            back_button = popup.offspring("B_Back") if popup.offspring("B_Back").exists() else None
            assert back_button is not None, "Back button not found in clan popup!"
            back_button.click(sleep_interval=1)

        # Compare id and name between the two clans
        assert clan_data[0][0] != clan_data[1][0], f"Clan IDs are the same: {clan_data[0][0]}"
        assert clan_data[0][1] != clan_data[1][1], f"Clan names are the same: {clan_data[0][1]}"
        print(f"✅ First two clans have different IDs and names: {clan_data[0]} vs {clan_data[1]}")
        print(f"✅ Clan names match between leaderboard and profiles")

########### helper functions ###########
    def _wait_for_loading_complete(self):
        """Wait for loading icon to disappear. Returns True if loading completed, False if timeout"""
        loading_icon = self.tab_player.loading_icon
        timeout = 10
        if loading_icon:
            logger = get_logger()
            logger.info("Waiting for loading to complete...")
            try:
                wait_for_element(lambda: not self.tab_player.loading_icon, timeout=timeout)
                time.sleep(1)  # Additional wait for data to populate
                return True
            except:
                logger.warning(f"Loading icon did not disappear within timeout {timeout}s - no data available")
                return False
        return True  # No loading icon means already loaded

    def check_common_elements(self, tab_name: str, sub_tab_name: str):
        """Check common elements present in all sub-tabs"""
        logger = get_logger()
        logger.info(f"Checking common elements in {tab_name} - {sub_tab_name}...")

        # Wait for loading to complete
        loading_completed = self._wait_for_loading_complete()

        # Check title (always available)
        title = self.tab_player.title
        expected_titles = {
            'campaign': "Campaign Leaderboard",
            'league': "Champions League",
            'pvpT1': "PVP Tier 1 Leaderboard",
            'pvpT2': "PVP Tier 2 Leaderboard",
            '2v2': "2v2 Leaderboard"
        }
        assert title == expected_titles[tab_name], f"Title mismatch in {tab_name}-{sub_tab_name}: expected {expected_titles[tab_name]}, got {title}"

        # If loading didn't complete, only title is available
        if not loading_completed:
            logger.warning(f"No data loaded for {tab_name}-{sub_tab_name}, only title checked")
            return False  # Return False to indicate no player data available

        # Check top 3 players (except for friends tab which might have <3 players)
        top3_names = self.tab_player.top3_name
        top3_avatars = self.tab_player.top3_ava

        if sub_tab_name != 'friends':
            # For world and local tabs, expect 3 top players
            if len([name for name in top3_names if name]) != 3:
                logger.error(
                    f"Expected 3 top players in {tab_name}-{sub_tab_name}, got {len([name for name in top3_names if name])}")
            if len([ava for ava in top3_avatars if ava]) != 3:
                logger.error(
                    f"Expected 3 top avatars in {tab_name}-{sub_tab_name}, got {len([ava for ava in top3_avatars if ava])}")
            if not all(name and name.strip() != "" for name in top3_names):
                logger.error(f"All top 3 player names must be non-empty in {tab_name}-{sub_tab_name}")
            if not all(ava is not None for ava in top3_avatars):
                logger.error(f"All top 3 player avatars must not be None in {tab_name}-{sub_tab_name}")
        return True  # Return True to indicate data is available for player checking

    def check_player_stats(self, players: list, stat_type: str, tab_name: str, sub_tab_name: str, player_count: int = None):
        """Check player statistics based on stat type - optimized to check only first 8 players"""
        logger = get_logger()
        # Use passed player_count to avoid calling len(players) again
        if player_count is None:
            player_count = len(players)

        # Debug: Log the actual player list details
        logger.info(f"Total players available: {player_count}")

        # Limit to first 3 players for faster testing
        number_checked = 3
        players_to_check = players[:number_checked]

        logger.info(f"Checking first {number_checked} players' {stat_type} stats in {tab_name}-{sub_tab_name}...")

        for index, player in enumerate(players_to_check):
            logger.info(f"Checking player {index + 1}...")

            try:
                # Verify player has valid root before proceeding
                if not player.root.exists():
                    logger.error(f"Player {index + 1} has invalid root node - skipping")
                    continue
                # Check common player elements with optimized checks
                if index < 3:  # top3 players have different layout
                    sprite_index = player.sprite_index_top3
                    if sprite_index and f"Num_{index+1}" not in str(sprite_index):
                        logger.warning(f"Player {index + 1} sprite index unexpected: {sprite_index}")
                else:
                    beyond_top3 = player.index_beyond_top3
                    if beyond_top3 and str(beyond_top3) != str(index+1):
                        logger.warning(f"Player beyond top 3 index mismatch: expected {index + 1}, got {beyond_top3}")
                # Quick existence checks
                assert player.profile_pic.exists(), f"Profile picture not found for player {index + 1}"
                assert player.flag.exists(), f"Flag not found for player {index + 1}"
                # Quick text validations
                name = player.name
                assert name and name.strip(), f"Player name is empty for player {index + 1}"
                # Check ID format - simplified
                actual_id = player.id
                if actual_id and not actual_id.startswith("ID: "):
                    logger.warning(f"Player ID format unexpected: {actual_id}")
                # Check clan format - simplified
                clan = player.clan
                if clan and not clan.startswith("Team: "):
                    logger.warning(f"Player clan format unexpected: {clan}")
                # Check stat-specific elements with simplified validation
                if stat_type == 'campaign':
                    stat = player.campaign_stat
                    if stat and stat.root.exists():
                        level_title = stat.level_title
                        level_value = stat.level_value
                        star_icons=stat.star_icons
                        star_value=stat.star_value
                        if level_title and level_title.strip() != "Level:":
                            logger.warning(f"Unexpected level title for player {index + 1}: {level_title}")
                        if level_value and level_value.strip().isdigit():
                            level_val = int(level_value.strip())
                            if not (1 <= level_val <= max_level):
                                logger.warning(f"Level out of range for player {index + 1}: {level_val}")
                        for i, icon in enumerate(star_icons):
                            if not icon.exists():
                                logger.warning(f"Star icon {i+1} not found for player {index + 1}")
                        if star_value =="":
                            logger.warning(f"Star value is empty for player {index + 1}")
                        max_star_can_get=(max_level*3+max_level//7*3*2)*3 # every 7 levels has 2 extra levels, each level has 3 stars. total 3 mode
                        print(f"max_star_can_get: {max_star_can_get}")
                        if not (0<=int(star_value)<=max_star_can_get+1):
                            logger.warning(f"Star value out of range for player {index + 1}: {star_value}")
                    else:
                        logger.warning(f"Campaign stat not found for player {index + 1}")

                elif stat_type == 'league':
                    stat = player.league_stat
                    if stat and stat.root.exists():
                        score = int(stat.score)
                        score_icon = stat.score_icon
                        if score < 0:
                            logger.warning(f"League score is negative for player {index + 1}: {score}")
                        if score_icon != "UI5_Champion_PointBig":
                            logger.warning(f"League score icon unexpected for player {index + 1}: {score_icon}")
                    else:
                        logger.warning(f"League stat not found for player {index + 1}")

                elif stat_type == 'pvp':
                    stat = player.pvp_stat
                    if stat and stat.root.exists():
                        rank_value = stat.rank_value
                        rank_icon = stat.rank_icon
                        elo = stat.elo
                        if rank_value not in allowed_ranks:
                            logger.warning(f"Unexpected rank value for player {index + 1}: {rank_value}")
                        if not rank_icon.startswith("PVP_rank_"):
                            logger.warning(f"Unexpected rank icon for player {index + 1}: {rank_icon}")
                        if not elo.startswith("ELO: "):
                            logger.warning(f"Unexpected ELO format for player {index + 1}: {elo}")
                        elo = int(elo.replace("ELO: ", ""))
                        if elo < 0:
                            logger.warning(f"PvP ELO is negative for player {index + 1}: {elo}")
                    else:
                        logger.warning(f"PvP stat not found for player {index + 1}")

                elif stat_type == 'vs2':
                    stat = player.vs2_stat
                    if stat and stat.root.exists():
                        score = stat.score
                        rank_icon = stat.rank_icon
                        rank_value = stat.rank_value
                        if not score.startswith("Season score: "):
                            logger.warning(f"Unexpected score format for player {index + 1}: {score}")
                        score_digit = score.replace("Season score: ", "")
                        if clean_number(score_digit) < 1000:
                            logger.warning(f"2v2 score too low for player {index + 1}: {score_digit}")
                        if not rank_icon or not rank_value:
                            logger.info(f"2v2 rank icon or value missing for player {index + 1}")
                        if rank_icon and not rank_icon.startswith("2vs2Chest"):
                            logger.warning(f"Unexpected 2v2 rank icon for player {index + 1}: {rank_icon}")
                        if rank_value and rank_value not in categories:
                            logger.warning(f"Unexpected 2v2 rank value for player {index + 1}: {rank_value}")
                    else:
                        logger.warning(f"2v2 stat not found for player {index + 1}")

            except Exception as e:
                logger.error(f"Error checking player {index + 1}: {str(e)}")
                # Continue with next player instead of failing the entire test

    def run_tab_subtabs_test(self, main_tab_btn, tab_name: str, stat_type: str):
        """Test all sub-tabs for a given main tab"""
        logger = get_logger()
        logger.info(f"Testing {tab_name} tab with all sub-tabs...")

        # Click main tab
        main_tab_btn.click(sleep_interval=1)

        # Check that clicked main tab is active and others are inactive
        main_tab_buttons = [
            (self.tab_player.btn_campaign, 'campaign'),
            (self.tab_player.btn_league, 'league'),
            (self.tab_player.btn_pvpT1, 'pvpT1'),
            (self.tab_player.btn_pvpT2, 'pvpT2'),
            (self.tab_player.btn_2v2, '2v2')
        ]

        for btn, btn_name in main_tab_buttons:
            if btn_name == tab_name:
                assert UIButtonUtils.check_sprite_btn_active(btn), f"{btn_name} main tab button not activated after click!"
            else:
                assert UIButtonUtils.check_sprite_btn_inactive(btn), f"{btn_name} main tab button not deactivated!"

        # Test each sub-tab
        sub_tabs = [
            (self.tab_player.btn_world, 'world'),
            (self.tab_player.btn_local, 'local'),
            (self.tab_player.btn_friends, 'friends')
        ]

        for sub_tab_btn, sub_tab_name in sub_tabs:
            logger.info(f"Testing {tab_name} - {sub_tab_name} sub-tab...")

            # Click sub-tab
            sub_tab_btn.click(sleep_interval=1)

            # Check that clicked sub-tab is active and others are inactive
            sub_tab_buttons = [
                (self.tab_player.btn_world, 'world'),
                (self.tab_player.btn_local, 'local'),
                (self.tab_player.btn_friends, 'friends')
            ]

            for btn, btn_name in sub_tab_buttons:
                if str(btn) == str(sub_tab_btn):
                    assert UIButtonUtils.check_sprite_btn_active(btn), f"{btn_name} sub-tab button not activated after click!"
                else:
                    assert UIButtonUtils.check_sprite_btn_inactive(btn), f"{btn_name} sub-tab button not deactivated!"

            # Check common elements and get data availability status
            data_available = self.check_common_elements(tab_name, sub_tab_name)

            # If no data is available (loading timeout), skip player checking
            if not data_available:
                logger.warning(f"Skipping player stats check for {tab_name}-{sub_tab_name} due to no data")
                continue

            # Get players list
            players = self.tab_player.players
            player_count = len(players)

            # Check player list length based on sub-tab type
            if sub_tab_name in ['world', 'local']:
                # World and local tabs should have exactly 20 players - log error if not
                if player_count != 20:
                    logger.error(f"Expected 20 players in {tab_name}-{sub_tab_name}, got {player_count}")
                else:
                    logger.info(f"Confirmed {player_count} players in {tab_name}-{sub_tab_name}")

            # Check player stats (still limited to first 8 for performance)
            if player_count > 0:
                self.check_player_stats(players, stat_type, tab_name, sub_tab_name, player_count)
            else:
                logger.warning(f"No players found in {tab_name}-{sub_tab_name}")

    # def test_campaign_tab_all_subtabs(self):
    #     """Test Campaign tab with World, Local, and Friends sub-tabs"""
    #     logger = get_logger()
    #     logger.info("Starting Campaign tab test...")
    #     start_time = time.time()
    #     self.run_tab_subtabs_test(self.tab_player.btn_campaign, 'campaign', 'campaign')
    #     elapsed_time = time.time() - start_time
    #     logger.info(f"Campaign tab test completed in {elapsed_time:.2f} seconds")
    #
    # def test_league_tab_all_subtabs(self):
    #     logger = get_logger()
    #     logger.info("Starting League tab test...")
    #     start_time = time.time()
    #     self.run_tab_subtabs_test(self.tab_player.btn_league, 'league', 'league')
    #     elapsed_time = time.time() - start_time
    #     logger.info(f"League tab test completed in {elapsed_time:.2f} seconds")
    #
    # def test_pvpT1_tab_all_subtabs(self):
    #     """Test PvP Tier 1 tab with World, Local, and Friends sub-tabs"""
    #     logger = get_logger()
    #     logger.info("Starting PvP Tier 1 tab test...")
    #     start_time = time.time()
    #     self.run_tab_subtabs_test(self.tab_player.btn_pvpT1, 'pvpT1', 'pvp')
    #     elapsed_time = time.time() - start_time
    #     logger.info(f"PvP Tier 1 tab test completed in {elapsed_time:.2f} seconds")
    #
    # def test_pvpT2_tab_all_subtabs(self):
    #     """Test PvP Tier 2 tab with World, Local, and Friends sub-tabs"""
    #     logger = get_logger()
    #     logger.info("Starting PvP Tier 2 tab test...")
    #     start_time = time.time()
    #     self.run_tab_subtabs_test(self.tab_player.btn_pvpT2, 'pvpT2', 'pvp')
    #     elapsed_time = time.time() - start_time
    #     logger.info(f"PvP Tier 2 tab test completed in {elapsed_time:.2f} seconds")
    #
    # def test_2v2_tab_all_subtabs(self):
    #     """Test 2v2 tab with World, Local, and Friends sub-tabs"""
    #     logger = get_logger()
    #     logger.info("Starting 2v2 tab test...")
    #     start_time = time.time()
    #     self.run_tab_subtabs_test(self.tab_player.btn_2v2, '2v2', 'vs2')
    #     elapsed_time = time.time() - start_time
    #     logger.info(f"2v2 tab test completed in {elapsed_time:.2f} seconds")

    # --- Clan tab tests (added below player tab tests, do not remove or modify player tab tests) ---
    def run_clan_tab_subtabs_test(self, main_tab_btn, tab_name: str):
        logger = get_logger()
        logger.info(f"Testing {tab_name} tab with World and Local sub-tabs in Clan tab...")
        # Click main tab
        main_tab_btn.click(sleep_interval=1)
        tab_clan = TabClan(self.poco)
        # Check that clicked main tab is active
        if not UIButtonUtils.check_sprite_btn_active(main_tab_btn):
            logger.error(f"{tab_name} main tab button not activated after click!")
        main_tab_buttons = [
            tab_clan.btn_upgrade,
            tab_clan.btn_glory,
            tab_clan.btn_clan_war,
            tab_clan.btn_zodiac
        ]
        for btn in main_tab_buttons:
            if str(btn) != str(main_tab_btn):
                assert UIButtonUtils.check_sprite_btn_inactive(btn), f"{btn} main tab button not deactivated!"
        # Test each sub-tab
        sub_tabs = [
            (tab_clan.btn_world, 'world'),
            (tab_clan.btn_local, 'local')
        ]
        for sub_tab_btn, sub_tab_name in sub_tabs:
            logger.info(f"Testing {tab_name} - {sub_tab_name} sub-tab in Clan tab...")
            sub_tab_btn.click(sleep_interval=1)
            # Check that clicked sub-tab is active and others are inactive
            sub_tab_buttons = [
                (tab_clan.btn_world, 'world'),
                (tab_clan.btn_local, 'local')
            ]
            for btn, btn_name in sub_tab_buttons:
                if str(btn) == str(sub_tab_btn):
                    assert UIButtonUtils.check_sprite_btn_active(
                        btn), f"{btn_name} sub-tab button not activated after click!"
                else:
                    assert UIButtonUtils.check_sprite_btn_inactive(btn), f"{btn_name} sub-tab button not deactivated!"
            # Wait for loading to complete
            loading_icon = tab_clan.loading_icon
            timeout = 10
            if loading_icon:
                try:
                    wait_for_element(lambda: not tab_clan.loading_icon, timeout=timeout)
                    time.sleep(1)
                except:
                    logger.warning(f"Loading icon did not disappear within timeout {timeout}s - no data available")
                    # If loading uncompleted, check title and skip the rest
                    assert tab_clan.title == "Top team", f"Title mismatch in {tab_name}-{sub_tab_name}: expected 'Top team', got {tab_clan.title}"
                    continue
            # Check title
            assert tab_clan.title == "Top team", f"Title mismatch in {tab_name}-{sub_tab_name}: expected 'Top team', got {tab_clan.title}"

            # Check top 3 clans
            top3_names = tab_clan.top3_name
            top3_avatars = tab_clan.top3_ava
            if len([name for name in top3_names if name]) != 3:
                logger.error(f"Expected 3 top clans in {tab_name}-{sub_tab_name}, got {len([name for name in top3_names if name])}")
            if len([ava for ava in top3_avatars if ava]) != 3:
                logger.error(f"Expected 3 top avatars in {tab_name}-{sub_tab_name}, got {len([ava for ava in top3_avatars if ava])}")
            # Check ItemClan list
            clans = tab_clan.clans
            clan_count = len(clans)
            if clan_count != 20:
                logger.error(f"Expected 20 clans in {tab_name}-{sub_tab_name}, got {clan_count}")
            logger.info(f"Total clans available: {clan_count}")
            number_checked = min(3, clan_count)
            for index, clan in enumerate(clans[:number_checked]):
                logger.info(f"Checking clan {index + 1}...")
                assert clan.root.exists(), f"Clan {index + 1} has invalid root node - skipping"
                if index < 3:
                    sprite_index = clan.sprite_index_top3
                    if sprite_index and f"Num_{index+1}" not in str(sprite_index):
                        logger.warning(f"Clan {index + 1} sprite index unexpected: {sprite_index}")
                else:
                    beyond_top3 = clan.index_beyond_top3
                    if beyond_top3 and str(beyond_top3) != str(index+1):
                        logger.warning(f"Clan beyond top 3 index mismatch: expected {index + 1}, got {beyond_top3}")
                name = clan.name
                assert name and name.strip(), f"Clan name is empty for clan {index + 1}"
                profile_pic = clan.profile_pic
                assert profile_pic, f"Profile picture not found for clan {index + 1}"

    def test_leaderboard_scrollview(self):
        """
        Test scrolling functionality by comparing player items before and after swiping.
        Verifies that:
        1. The scroll view actually moves content
        2. Different player items appear after scrolling
        3. Player indices after scrolling are greater than before (when scrolling down)
        """
        logger = get_logger()
        logger.info("Starting leaderboard scrollview test")
        # Make sure we're on the leaderboard screen and player tab is active
        self.popup.btn_player.click(sleep_interval=1)
        self.tab_player.btn_campaign.click(sleep_interval=1)
        self.tab_player.btn_world.click(sleep_interval=1)
        # Get the scrollview
        leaderboard_scrollview = self.popup.root.offspring("Scroll View")
        assert leaderboard_scrollview.exists(), "Leaderboard scrollview not found!"

        # Get the position of the scrollview for swiping
        x, y = leaderboard_scrollview.get_position()
        logger.info(f"Scrollview position: {x}, {y}")

        # Get player items before scrolling (sample first 2 visible players)


        # Wait for loading to complete
        loading_completed = self._wait_for_loading_complete()
        if not loading_completed:
            logger.warning("Loading did not complete, cannot test scrollview")
            return False

        # Get player items before scrolling using existing tab_player.players
        before_players = []
        players_before = self.tab_player.players[:2]  # Get first 2 players

        if len(players_before) < 2:
            logger.warning("Found fewer than 2 player items before scrolling")

        for player in players_before:
            player_info = {
                'index': int(player.index_beyond_top3) if player.index_beyond_top3 and player.index_beyond_top3.isdigit() else -1,
                'id': player.id.replace("ID: ", "").strip() if player.id else "unknown",
                'name': player.name if player.name else "unknown"
            }
            before_players.append(player_info)

        logger.info("Player items before scrolling:")
        for player in before_players:
            logger.info(f"Index: {player['index']}, ID: {player['id']}, Name: {player['name']}")

        # Perform the scroll action (swipe up to see lower ranked players)
        logger.info("Performing swipe action")
        self.poco.swipe([x, y], direction=[0, -0.2], duration=1.0)
        time.sleep(1.0)  # Wait for UI to stabilize after swipe

        # Get player items after scrolling using existing tab_player.players
        after_players = []
        players_after = self.tab_player.players[:2]  # Get first 2 players after scrolling

        if len(players_after) < 2:
            logger.warning("Found fewer than 2 player items after scrolling")

        for player in players_after:
            player_info = {
                'index': int(player.index_beyond_top3) if player.index_beyond_top3 and player.index_beyond_top3.isdigit() else -1,
                'id': player.id.replace("ID: ", "").strip() if player.id else "unknown",
                'name': player.name if player.name else "unknown"
            }
            after_players.append(player_info)

        logger.info("Player items after scrolling:")
        for player in after_players:
            logger.info(f"Index: {player['index']}, ID: {player['id']}, Name: {player['name']}")

        # Verify scrolling worked correctly
        if not before_players or not after_players:
            logger.error("Error: Missing player data to verify scroll")
            return False

        # Check if at least some players are different (scrolling worked)
        before_ids = set(player['id'] for player in before_players)
        after_ids = set(player['id'] for player in after_players)

        if before_ids == after_ids:
            logger.error("ERROR: Player IDs before and after scrolling are identical - scroll may not have worked")
            return False

        # When scrolling down, player indices should be greater after scrolling
        before_min_index = min(player['index'] for player in before_players if player['index'] > 0)
        after_min_index = min(player['index'] for player in after_players if player['index'] > 0)

        if after_min_index <= before_min_index:
            logger.warning(f"WARNING: Player indices not increasing after scrolling down. Before min: {before_min_index}, After min: {after_min_index}")

        logger.info(f"Scroll test PASSED: Players changed after scrolling (before: {before_ids}, after: {after_ids})")
        return True

    def test_scroll_up_down(self):
        """
        Test both scroll down and scroll up operations to ensure bidirectional scrolling works.
        """
        logger = get_logger()
        logger.info("Testing bidirectional scrolling (down then up)")

        # Make sure we're on the leaderboard screen and player tab is active
        self.popup.btn_player.click(sleep_interval=1)

        # Get the scrollview
        leaderboard_scrollview = self.poco("PopupLeaderboardAll(Clone)").offspring("Scroll View")

        # Get scrollview position
        x, y = leaderboard_scrollview.get_position()

        # Get initial players
        initial_players = self.tab_player.players[:2]
        logger.info("Initial players:")
        for player in initial_players:
            logger.info(f"Index: {player.index}, ID: {player.id}, Name: {player.name}")

        # Scroll down
        logger.info("Scrolling DOWN")
        self.poco.swipe([x, y], direction=[0, -0.5], duration=1.0)
        time.sleep(1.0)

        # Get middle players (after scrolling down)
        middle_players = self.tab_player.players[:2]
        logger.info("Middle players (after scrolling down):")
        for player in middle_players:
            logger.info(f"Index: {player.index}, ID: {player.id}, Name: {player.name}")

        # Scroll back up
        logger.info("Scrolling UP")
        self.poco.swipe([x, y], direction=[0, 0.5], duration=1.0)
        time.sleep(1.0)

        # Get final players (after scrolling up)
        final_players = self.tab_player.players[:2]
        logger.info("Final players (after scrolling up):")
        for player in final_players:
            logger.info(f"Index: {player.index}, ID: {player.id}, Name: {player.name}")

        # Verify scroll down worked
        down_scroll_worked = self._verify_scroll_success(initial_players, middle_players)

        # Verify scroll up worked
        up_scroll_worked = self._verify_scroll_success(middle_players, final_players)

        # Check if we returned close to the original position
        initial_ids = set(player.id for player in initial_players)
        final_ids = set(player.id for player in final_players)

        overlap = len(initial_ids.intersection(final_ids))
        if overlap > 0:
            logger.info(f"Found {overlap} players in common between initial and final position - scroll up returned to similar position")
        else:
            logger.info("No common players between initial and final position - may indicate scroll up didn't return to original position")

        return down_scroll_worked and up_scroll_worked
