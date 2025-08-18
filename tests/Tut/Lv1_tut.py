from Hierarchy.PopupCampaignSelectLv import PopupCampaignSelectLv, PanelWorlds
from Hierarchy.PopupLevelPrepare import PopupLevelPrepare
from Hierarchy.UI_ingame import *
import pytest
from logger_config import get_logger
from utils.helper_functions import wait_for_element
from utils.test_level_helper import *
from airtest.core.api import swipe, sleep
current_dir=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
img_path= os.path.join(os.path.dirname(current_dir),"image","Plane1_bata.png")
bata_img = Template(img_path)

@pytest.mark.use_to_home(before=True, after=True, logger_name="Level1_tut")
@pytest.mark.use_to_campaign_select_lv(before=True)
class TestLevel1_tut:
    def setup(self):
        pass

    def swipe_to_world_item(self, popup_campaign, target_world_index, max_attempts=10):
        """
        ORIGINAL VERSION - Swipe to find and display the target WorldItem in the scrollview.
        The scrollview shows 6 visible elements at a time.
        Optimized with intelligent swipe distance calculation to minimize attempts.

        Args:
            popup_campaign: PopupCampaignSelectLv instance
            target_world_index: The index (1-based) of the world to find
            max_attempts: Maximum number of swipe attempts

        Returns:
            WorldItem if found, None otherwise
        """
        logger = get_logger("Level1_tut")
        panel_worlds = popup_campaign.panel_worlds

        if not panel_worlds:
            logger.error("Panel worlds not found")
            return None

        # Get reference positions
        title_pos = panel_worlds.title.get_position()

        # Cache world objects and indices on first attempt only
        cached_worlds = None
        avg_vertical_distance = None
        worlds_per_swipe = None

        for attempt in range(max_attempts):
            logger.info(f"ORIGINAL: Attempt {attempt + 1}: Looking for World {target_world_index}")

            # Only build cache on first attempt or if cache is empty
            if cached_worlds is None:
                logger.info("ORIGINAL: Building world cache...")
                list_world = panel_worlds.list_world
                if not list_world:
                    logger.warning("No worlds found in current view")
                    continue

                # Build cache of valid worlds with their indices
                cached_worlds = []
                for world in list_world:
                    try:
                        world_index = int(world.index) if world.index and world.index.isdigit() else None
                        if world_index:
                            cached_worlds.append((world, world_index))
                    except (ValueError, AttributeError):
                        continue

                if len(cached_worlds) < 2:
                    logger.warning("Not enough valid worlds found")
                    continue

                logger.info(f"ORIGINAL: Cached {len(cached_worlds)} valid worlds")

            # Get current positions for cached worlds (much faster than re-parsing)
            valid_worlds_with_pos = []

            for world, world_index in cached_worlds:
                try:
                    pos = world.root.get_position()
                    valid_worlds_with_pos.append((world, world_index, pos))
                except:
                    # Skip if world is no longer accessible
                    continue

            if len(valid_worlds_with_pos) < 2:
                logger.warning("Not enough worlds with valid positions")
                continue

            # Calculate average vertical distance only once
            if avg_vertical_distance is None:
                # Sort by Y position to calculate distance
                valid_worlds_with_pos.sort(key=lambda x: x[2][1])

                vertical_distances = []
                for i in range(1, min(10, len(valid_worlds_with_pos))):
                    vertical_distance = abs(valid_worlds_with_pos[i][2][1] - valid_worlds_with_pos[i-1][2][1])
                    vertical_distances.append(vertical_distance)

                avg_vertical_distance = sum(vertical_distances) / len(vertical_distances) if vertical_distances else 0
                logger.info(f"ORIGINAL: Calculated average vertical distance: {avg_vertical_distance}")

            # Find visible threshold
            visible_threshold = title_pos[1] + avg_vertical_distance

            # Filter visible worlds (y > visible_threshold)
            visible_worlds = []
            for world, world_index, world_pos in valid_worlds_with_pos:
                if world_pos[1] > visible_threshold:
                    visible_worlds.append((world, world_index, world_pos))

            # Sort visible worlds by Y position and take first 8
            visible_worlds.sort(key=lambda x: x[2][1])
            visible_worlds = visible_worlds[:8]

            if not visible_worlds:
                logger.warning("No visible worlds found")
                continue

            # Sort by world index for easier processing
            visible_worlds_by_index = sorted(visible_worlds, key=lambda x: x[1])
            visible_indices = [w[1] for w in visible_worlds_by_index]
            logger.info(f"ORIGINAL: Visible worlds: {visible_indices}")

            # Check if target world is among the visible elements
            for world, world_index, world_pos in visible_worlds:
                if world_index == target_world_index:
                    logger.info(f"ORIGINAL: Found target World {target_world_index} at position {world_pos}")
                    return world

            # Calculate worlds per swipe for intelligent swiping
            if worlds_per_swipe is None and attempt > 0:
                # Calculate based on previous swipe result
                prev_first_visible = getattr(self, '_prev_first_visible', None)
                if prev_first_visible is not None:
                    current_first_visible = visible_worlds_by_index[0][1]
                    worlds_per_swipe = abs(current_first_visible - prev_first_visible)
                    logger.info(f"ORIGINAL: Calculated worlds per swipe: {worlds_per_swipe}")

            # Store current first visible for next calculation
            self._prev_first_visible = visible_worlds_by_index[0][1]

            # Determine swipe direction and calculate intelligent swipe distance
            if not visible_worlds_by_index:
                continue

            first_visible_index = visible_worlds_by_index[0][1]
            last_visible_index = visible_worlds_by_index[-1][1]

            # Calculate swipe parameters
            screen_center_x = panel_worlds.root.get_position()[0]
            first_visible_y = visible_worlds[0][2][1]
            last_visible_y = visible_worlds[-1][2][1]
            single_swipe_distance = abs(last_visible_y - first_visible_y)

            # Calculate how many worlds we need to move
            if target_world_index < first_visible_index:
                worlds_to_move = first_visible_index - target_world_index
                # Add buffer to ensure target is in visible range
                worlds_to_move += 3
                direction = "down"
            elif target_world_index > last_visible_index:
                worlds_to_move = target_world_index - last_visible_index
                # Add buffer to ensure target is in visible range
                worlds_to_move += 3
                direction = "up"
            else:
                # Target should be visible but wasn't found - try a small adjustment
                logger.warning(f"Target {target_world_index} should be visible but not found, trying small swipe")
                worlds_to_move = 2
                direction = "up"

            # Calculate swipe multiplier based on worlds to move
            if worlds_per_swipe and worlds_per_swipe > 0:
                swipe_multiplier = max(1.0, worlds_to_move / worlds_per_swipe)
            else:
                # Use estimated multiplier based on typical scrollview behavior
                estimated_worlds_per_swipe = 6  # Based on log showing ~6-7 worlds per swipe
                swipe_multiplier = max(1.0, worlds_to_move / estimated_worlds_per_swipe)

            # Cap the multiplier to prevent overshooting
            swipe_multiplier = min(swipe_multiplier, 5.0)

            logger.info(f"ORIGINAL: Target {target_world_index}, visible range [{first_visible_index}-{last_visible_index}]")
            logger.info(f"ORIGINAL: Need to move {worlds_to_move} worlds {direction}, swipe multiplier: {swipe_multiplier:.2f}")

            if direction == "down":
                swipe_start = (screen_center_x, first_visible_y)
                swipe_end = (screen_center_x, first_visible_y + single_swipe_distance * swipe_multiplier)
            else:  # direction == "up"
                swipe_start = (screen_center_x, last_visible_y)
                swipe_end = (screen_center_x, last_visible_y - single_swipe_distance * swipe_multiplier)

            # Perform swipe

            # Normalize coordinates to range [-1, 1]
            norm_start = (max(min(swipe_start[0], 1), -1), max(min(swipe_start[1], 1), -1))
            norm_end = (max(min(swipe_end[0], 1), -1), max(min(swipe_end[1], 1), -1))
            logger.info(f"ORIGINAL: Swiping from {norm_start} to {norm_end}")
            swipe(norm_start, norm_end, duration=0.5)
            sleep(1)  # Wait for animation to complete

        logger.error(f"ORIGINAL: Could not find World {target_world_index} after {max_attempts} attempts")
        return None

    def test12333(self,poco):
        logger = get_logger("Level1_tut")

        popup_campaign = PopupCampaignSelectLv(poco)
        panel_worlds = PanelWorlds(poco)
        assert popup_campaign.root.exists(), "PopupCampaignSelectLv not found"
        # popup_campaign.mode_normal.click(sleep_interval=1)


        click_to_level=navigate_and_click_level(popup_campaign, 1,panel_worlds,  logger_name="Level1_tut")
        if not click_to_level:
            logger.error("Failed to navigate to Level 1")
            return
        popup_prepare=PopupLevelPrepare(poco)
        assert popup_prepare.root.exists(), "PopupLevelPrepare not found after clicking level 1"
        popup_prepare.btn_start.click(sleep_interval=3)
        ui_ingame = UI_Ingame(poco)
        if wait_for_element(ui_ingame.root, timeout=5):
            bata_pos = wait(bata_img, timeout=6)
            btn_skill_pos = ui_ingame.btn_plane_skill.get_position() if ui_ingame.btn_plane_skill.exists() else None

            if bata_pos and btn_skill_pos:
                start_pos = ((bata_pos[0] - btn_skill_pos[0]) / 2 + btn_skill_pos[0], bata_pos[1])
                end_pos = (bata_pos[0] + (bata_pos[0] - start_pos[0]), bata_pos[1])

                ingameUI = UI_Ingame(poco)
                btn = ingameUI.btn_plane_skill if ingameUI.btn_plane_skill.exists() else None
                first_move = False

                while btn:
                    if not first_move:
                        for i in range(30):
                            keyevent("P")
                        swipe(bata_pos, start_pos)  # move to start position
                        first_move = True
                    # keyevent("U")
                    swipe(start_pos, end_pos, duration=3)
                    swipe(end_pos, start_pos, duration=3)
                    sleep(2)
                    btn = ingameUI.btn_plane_skill if ingameUI.btn_plane_skill.exists() else None

        max_attempts = 5
        for attempt in range(max_attempts):
            popup_lose = PopupGameLose(poco)
            popup_win = PopupGameWin(poco)
            if popup_lose.root.exists():
                logger.info("Game lost, retrying...")
                # popup_lose.btn_retry.click(sleep_interval=3)
                # # Retry logic can be added here if needed
                break
            elif popup_win.root.exists():
                logger.info("Game won!")
                # popup_win.btn_continue.click(sleep_interval=3)
                break
            attempt += 1
            sleep(2)
            # Raise error if we run out of attempts and neither win nor lose popup appears
            if attempt >= max_attempts - 1:
                raise AssertionError("Game didn't reach a conclusion (win or lose) after maximum attempts")
