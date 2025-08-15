import time
from poco.exceptions import PocoNoSuchNodeException
from utils.get_resource_amount import *
from airtest.core.api import swipe, sleep
from logger_config import get_logger

def swipe_to_target_world_in_list(panel_worlds, target_item_index, max_attempts=10, logger_name="ScrollviewHelper"):
    """
    Swipe to find and display a target item in a scrollview.
    This is a generic helper function that can be used with any scrollview containing indexed items.

    Args:
        panel_worlds: Object containing the scrollview with title and list_world properties
        target_item_index: The index (1-based) of the item to find
        max_attempts: Maximum number of swipe attempts
        logger_name: Name for the logger instance

    Returns:
        an object of class WorldItem if found, None otherwise
    """
    logger = get_logger(logger_name)

    if not panel_worlds:
        logger.error("Panel not found")
        return None

    # Get reference positions
    title_pos = panel_worlds.title.get_position()

    # Cache item objects and indices on first attempt only
    cached_items = None
    avg_vertical_distance = None
    items_per_swipe = None
    prev_first_visible = None

    for attempt in range(max_attempts):
        logger.info(f"Attempt {attempt + 1}: Looking for world {target_item_index}")

        # Only build cache on first attempt or if cache is empty
        if cached_items is None:
            logger.info("Building item cache...")
            list_items = panel_worlds.list_world  # Generic property name
            logger.info(f"done  Building item cache: {list_items}")
            if not list_items:
                logger.warning("No world found in current view")
                continue

            # Build cache of valid items with their indices
            cached_items = []
            for item in list_items:
                try:
                    item_index = int(item.index) if item.index and item.index.isdigit() else None
                    if item_index:
                        cached_items.append((item, item_index))
                except (ValueError, AttributeError):
                    continue
            logger.info(f"Found {len(cached_items)} items in cache")

            if len(cached_items) < 2:
                logger.warning("Not enough valid worlds found")
                continue

            logger.info(f"Cached {len(cached_items)} valid worlds")

        # Get current positions for cached items (much faster than re-parsing)
        valid_items_with_pos = []

        for item, item_index in cached_items:
            try:
                pos = item.root.get_position()
                valid_items_with_pos.append((item, item_index, pos))
            except:
                # Skip if item is no longer accessible
                continue

        if len(valid_items_with_pos) < 2:
            logger.warning("Not enough worlds with valid positions")
            continue

        # Calculate average vertical distance only once
        if avg_vertical_distance is None:
            # Sort by Y position to calculate distance
            valid_items_with_pos.sort(key=lambda x: x[2][1])

            vertical_distances = []
            for i in range(1, min(10, len(valid_items_with_pos))):
                vertical_distance = abs(valid_items_with_pos[i][2][1] - valid_items_with_pos[i-1][2][1])
                vertical_distances.append(vertical_distance)

            avg_vertical_distance = sum(vertical_distances) / len(vertical_distances) if vertical_distances else 0
            logger.info(f"Calculated average vertical distance: {avg_vertical_distance}")

        # Find visible threshold
        visible_threshold = title_pos[1] + avg_vertical_distance

        # Filter visible items (y > visible_threshold)
        visible_items = []
        for item, item_index, item_pos in valid_items_with_pos:
            if item_pos[1] > visible_threshold:
                visible_items.append((item, item_index, item_pos))

        # Sort visible items by Y position and take first 10
        visible_items.sort(key=lambda x: x[2][1])
        visible_items = visible_items[:10]

        if not visible_items:
            logger.warning("No visible items found")
            continue

        # Sort by item index for easier processing
        visible_items_by_index = sorted(visible_items, key=lambda x: x[1])
        visible_indices = [w[1] for w in visible_items_by_index]
        logger.info(f"Visible items: {visible_indices}")

        # Check if target item is among the visible elements
        for item, item_index, item_pos in visible_items:
            if item_index == target_item_index:
                logger.info(f"Found target world {target_item_index} at position {item_pos}")
                return item

        # Calculate items per swipe for intelligent swiping
        if items_per_swipe is None and attempt > 0:
            # Calculate based on previous swipe result
            if prev_first_visible is not None:
                current_first_visible = visible_items_by_index[0][1]
                items_per_swipe = abs(current_first_visible - prev_first_visible)
                logger.info(f"Calculated items per swipe: {items_per_swipe}")

        # Store current first visible for next calculation
        prev_first_visible = visible_items_by_index[0][1]

        # Determine swipe direction and calculate intelligent swipe distance
        if not visible_items_by_index:
            continue

        first_visible_index = visible_items_by_index[0][1]
        last_visible_index = visible_items_by_index[-1][1]

        # Calculate swipe parameters
        screen_center_x = panel_worlds.root.get_position()[0]
        first_visible_y = visible_items[0][2][1]
        last_visible_y = visible_items[-1][2][1]
        single_swipe_distance = abs(last_visible_y - first_visible_y)

        # Calculate how many items we need to move
        if target_item_index < first_visible_index:
            items_to_move = first_visible_index - target_item_index
            # Add buffer to ensure target is in visible range
            items_to_move += 3
            direction = "down"  # Swipe down to show earlier items (smaller indices)
        elif target_item_index > last_visible_index:
            items_to_move = target_item_index - last_visible_index
            # Add buffer to ensure target is in visible range
            items_to_move += 3
            direction = "up"  # Swipe up to show later items (larger indices)
        else:
            # Target should be visible but wasn't found - try a small adjustment
            logger.warning(f"Target {target_item_index} should be visible but not found, trying small swipe")
            items_to_move = 2
            direction = "up"

        # Calculate swipe multiplier based on items to move
        if items_per_swipe and items_per_swipe > 0:
            swipe_multiplier = max(1.0, items_to_move / items_per_swipe)
        else:
            # Use estimated multiplier based on typical scrollview behavior
            estimated_items_per_swipe = 6  # Based on common scrollview behavior
            swipe_multiplier = max(1.0, items_to_move / estimated_items_per_swipe)

        # Cap the multiplier to prevent overshooting
        swipe_multiplier = min(swipe_multiplier, 5.0)

        logger.info(f"Target {target_item_index}, visible range [{first_visible_index}-{last_visible_index}]")
        logger.info(f"Need to move {items_to_move} items {direction}, swipe multiplier: {swipe_multiplier:.2f}")

        if direction == "down":
            # Swipe down to show earlier items (smaller indices) - increase Y coordinate
            swipe_start = (screen_center_x, first_visible_y)
            swipe_end = (screen_center_x, first_visible_y + single_swipe_distance * swipe_multiplier)
        else:  # direction == "up"
            # Swipe up to show later items (larger indices) - decrease Y coordinate
            swipe_start = (screen_center_x, last_visible_y)
            swipe_end = (screen_center_x, last_visible_y - single_swipe_distance * swipe_multiplier)

        # Perform swipe
        norm_start = (max(min(swipe_start[0], 1), -1), max(min(swipe_start[1], 1), -1))
        norm_end = (max(min(swipe_end[0], 1), -1), max(min(swipe_end[1], 1), -1))
        logger.info(f"ORIGINAL: Swiping from {norm_start} to {norm_end}")
        swipe(norm_start, norm_end, duration=0.5)
        sleep(1)  # Wait for animation to complete

    logger.error(f"Could not find item {target_item_index} after {max_attempts} attempts")
    return None

def navigate_and_click_level(popup_campaign, target_level, panel_worlds, logger_name="LevelHelper"):
    """
    Find and click a target level by automatically navigating to the correct world.

    Args:
        popup_campaign: PopupCampaignSelectLv instance
        target_level: The level number to find and click (1-based)
        panel_worlds: PanelWorlds instance (must be provided explicitly)
        logger_name: Name for the logger instance

    Returns:
        True if level was found and clicked, False otherwise

    Raises:
        RuntimeError: If target level is not found in the expected world
    """
    logger = get_logger(logger_name)

    # Calculate which world the target level belongs to (7 levels per world)
    expected_world = (target_level - 1) // 7 + 1
    logger.info(f"Target level {target_level} should be in World {expected_world}")

    # Get current world
    current_world = popup_campaign.current_world
    if current_world:
        current_world_num = int(current_world)
        logger.info(f"Current world: {current_world_num}")
    else:
        logger.error("Could not determine current world")
        return False

    # Check if we need to navigate to a different world
    if current_world_num != expected_world:
        logger.info(f"Need to navigate from World {current_world_num} to World {expected_world}")

        # Open world selection panel
        popup_campaign.btn_select_world.click()
        sleep(1)

        # Use swipe_to_target_world to find the target world
        target_world_item = swipe_to_target_world_in_list(
            panel_worlds,
            expected_world,
            logger_name=logger_name
        )

        if not target_world_item:
            logger.error(f"Could not find World {expected_world}")
            return False

        # Click on the target world
        target_world_item.btn_go.click()
        logger.info(f"Clicked on World {expected_world}")
        sleep(3)  # Wait for world to load

        # Verify we're now in the correct world
        current_world = popup_campaign.current_world
        if not current_world or int(current_world) != expected_world:
            logger.error(f"Failed to navigate to World {expected_world}")
            return False

        logger.info(f"Successfully navigated to World {expected_world}")

    # Now find the target level in list_level_normal
    logger.info(f"Looking for level {target_level} in normal levels")

    # Wait for levels to load and refresh the list multiple times to ensure we get fresh data
    max_refresh_attempts = 5
    list_normal = None
    target_level_item = None

    for refresh_attempt in range(max_refresh_attempts):
        sleep(1)  # Wait for levels to load

        # Get fresh list of normal levels
        list_normal = popup_campaign.list_level_normal

        if list_normal:
            logger.info(f"Refresh attempt {refresh_attempt + 1}: Found {len(list_normal)} levels")

            # Search for the target level directly
            for level_item in list_normal:
                if level_item.index and level_item.index.isdigit():
                    level_index = int(level_item.index)
                    print(f"Checking level: {level_index} vs target: {target_level}")
                    if level_index == target_level:
                        target_level_item = level_item
                        break

            if target_level_item:
                logger.info(f"✓ Found target level {target_level} on attempt {refresh_attempt + 1}")
                break  # Found target level, exit refresh loop
        else:
            logger.warning(f"Refresh attempt {refresh_attempt + 1}: No levels found, retrying...")

    # Debug: Print all levels found
    if list_normal:
        for level in list_normal:
            print(f"::::::level: {level.root.attr('name')}, index: {level.index}")

    if not list_normal:
        logger.error("No normal levels found")
        return False

    logger.info(f"Found {len(list_normal)} normal levels")

    if not target_level_item:
        # Log available levels for debugging
        available_levels = [level.index for level in list_normal if level.index and level.index.isdigit()]
        logger.error(f"Level {target_level} not found in World {expected_world}")
        logger.error(f"Available levels: {available_levels}")
        raise RuntimeError(f"Target level {target_level} not found in expected World {expected_world}")

    # Click on the target level
    logger.info(f"Found level {target_level}, clicking on it")
    target_level_item.root.click()
    logger.info(f"Successfully clicked on level {target_level}")

    return True
