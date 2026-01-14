from airtest.core.api import swipe, sleep

from Hierarchy.PopupCampaignSelectLv import PopupCampaignSelectLv
from logger_config import get_logger
from utils.helper_functions import wait_for_element
from airtest.core.api import exists, touch, Template
import os
from utils.get_resource_amount import clean_number

# Module-level reward mapping (from unity-side snippet): level -> list of reward keys
LEVEL_REWARD_KEYS = {
    4:  ['GEM', 'ITEM_POWER_ATK_UP'],
    7:  ['CARD_WINGMAN_DOUBLE_GALTING', 'GOLD', 'ITEM_POWER_SPEED_UP'],
    11: ['KEY_GOLDEN', 'GOLD'],
    14: ['CARD_WING_WING_OF_JUSTICE', 'ENERGY', 'ITEM_POWER_GOLD_UP'],
    18: ['GEM'],
    21: ['KEY_ENGINE', 'ENERGY'],
    25: ['CARD_AIRCRAFT_GENERAL', 'ENERGY'],
    28: ['KEY_ENGINE', 'GOLD', 'ITEM_POWER_CDR_UP'],
    32: ['GEM'],
    35: ['KEY_MYSTIC', 'ENERGY'],
    39: ['CARD_AIRCRAFT_GENERAL', 'GOLD'],
    42: ['KEY_ENGINE', 'GOLD', 'ITEM_POWER_HP_UP'],
}

# Expected amounts mapping per level (Unity snippet)
LEVEL_REWARD_AMOUNTS = {
    4:  [('GEM', 10), ('ITEM_POWER_ATK_UP', 1)],
    7:  [('CARD_WINGMAN_DOUBLE_GALTING', 20), ('GOLD', 5000), ('ITEM_POWER_SPEED_UP', 1)],
    11: [('KEY_GOLDEN', 2), ('GOLD', 5000)],
    14: [('CARD_WING_WING_OF_JUSTICE', 20), ('ENERGY', 2000), ('ITEM_POWER_GOLD_UP', 1)],
    18: [('GEM', 50)],
    21: [('KEY_ENGINE', 2), ('ENERGY', 3000)],
    25: [('CARD_AIRCRAFT_GENERAL', 10), ('ENERGY', 3000)],
    28: [('KEY_ENGINE', 2), ('GOLD', 5000), ('ITEM_POWER_CDR_UP', 1)],
    32: [('GEM', 50)],
    35: [('KEY_MYSTIC', 3), ('ENERGY', 3000)],
    39: [('CARD_AIRCRAFT_GENERAL', 10), ('GOLD', 5000)],
    42: [('KEY_ENGINE', 3), ('GOLD', 5000), ('ITEM_POWER_HP_UP', 1)],
}

# Registry: reward key -> filename in image/ (adjust when new icons are added)
REWARD_ICON_MAP = {
    'GEM': 'gemPanelTitle.png',
    'GOLD': 'goldPanelTitle.png',
    'ENERGY': 'energyPanelTitle.png',
    # Add these when images are available in image/ or a subfolder
    'KEY_ENGINE': 'keyEngine.png',
    'KEY_GOLDEN': 'keyGolden.png',
    'KEY_MYSTIC': 'keyMystic.png',
    'ITEM_POWER_ATK_UP': 'itemPowerAtkUp.png',
    'ITEM_POWER_SPEED_UP': 'itemPowerSpeedUp.png',
    'ITEM_POWER_GOLD_UP': 'itemPowerGoldUp.png',
    'ITEM_POWER_CDR_UP': 'itemPowerCDRUp.png',
    'ITEM_POWER_HP_UP': 'itemPowerHPUp.png',
    'CARD_WINGMAN_DOUBLE_GALTING': 'card_wingman_double_galting.png',
    'CARD_WING_WING_OF_JUSTICE': 'card_wing_of_justice.png',
    'CARD_AIRCRAFT_GENERAL': 'card_aircraft_general.png',
}

def swipe_to_target_world_in_list(poco,popup_Selectlv, target_item_index:int, max_attempts=10,
                                        logger_name="ScrollviewHelper"):
    logger = get_logger(logger_name)
    # Get reference positions
    title_pos = popup_Selectlv.world_panel.title.get_position()

    # Cache item objects and indices on first attempt only
    list_item = None  # all world items
    avg_vertical_distance = None
    items_per_swipe = None
    prev_first_visible = None

    for attempt in range(max_attempts):
        logger.info(f"Attempt {attempt + 1}: Looking for world {target_item_index}")
        if attempt > 0: # 1st attempt already have cache, need fresh positions after swipe
            popup_Selectlv= PopupCampaignSelectLv(poco.freeze())
        list_item = [] # reset each attempt, need fresh positions after each swipe
        # item include (object, index, position)
        for item in popup_Selectlv.world_panel.list_world:
            try:
                item_index = int(item.index) if item.index else None
                item_pos = item.root.get_position()
                if item_index:
                    list_item.append((item, item_index, item_pos))
            except (ValueError, AttributeError):
                continue
        logger.info(f"Found {len(list_item)} items ")
        # Calculate average vertical distance only once
        if avg_vertical_distance is None:
            # Sort by Y position to calculate distance
            list_item.sort(key=lambda x: x[2][1])
            vertical_distances = []
            for i in range(1, min(5, len(list_item))):
                vertical_distance = abs(list_item[i][2][1] - list_item[i - 1][2][1])
                vertical_distances.append(vertical_distance)
            avg_vertical_distance = sum(vertical_distances) / len(vertical_distances) if vertical_distances else 0
            logger.info(f"Calculated average vertical distance: {avg_vertical_distance}")
        # Find visible threshold
        visible_threshold = title_pos[1] + avg_vertical_distance
        # Filter visible items (y > visible_threshold)
        visible_items = []
        for item, item_index, item_pos in list_item:
            if item_pos[1] > visible_threshold:
                visible_items.append((item, item_index, item_pos))

        #
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

        first_visible_index = visible_items_by_index[0][1]
        last_visible_index = visible_items_by_index[-1][1]

        # Calculate swipe parameters
        screen_center_x = popup_Selectlv.world_panel.scrollview.get_position()[0]
        first_visible_y = visible_items[0][2][1]
        last_visible_y = visible_items[-1][2][1]
        single_swipe_distance = abs(last_visible_y - first_visible_y)

        # Calculate how many items we need to move
        if target_item_index < first_visible_index:
            # items_to_move = first_visible_index - target_item_index
            # # Add buffer to ensure target is in visible range
            # items_to_move += 3
            direction = "down"  # Swipe down to show earlier items (smaller indices)
            logger.info(f"need to move DOWN to find {target_item_index} from first item:{first_visible_index}")
        elif target_item_index > last_visible_index:
            # items_to_move = target_item_index - last_visible_index
            # # Add buffer to ensure target is in visible range
            # items_to_move += 3
            direction = "up"  # Swipe up to show later items (larger indices)
            logger.info(f"need to move UP to find {target_item_index} from last item:{last_visible_index}")
        else:
            logger.warning(f"Target {target_item_index} should be visible but not found")
            continue

        if direction == "down":
            # Swipe down to show earlier items (smaller indices) - increase Y coordinate
            swipe_start = (screen_center_x, first_visible_y)
            swipe_end = (screen_center_x, last_visible_y-avg_vertical_distance) # adjust y for the last item to avoid clicking the rim-the border
        else:  # direction == "up"
            # Swipe up to show later items (larger indices) - decrease Y coordinate
            swipe_start = (screen_center_x, last_visible_y-avg_vertical_distance)# adjust y for the last item to avoid clicking the rim-the border
            swipe_end = (screen_center_x, first_visible_y)

        logger.info(f"Swiping from {swipe_start} to {swipe_end} to find world {target_item_index}")
        swipe(swipe_start, swipe_end)
        sleep(2) # Wait for UI to stabilize after swipe prepare for next attempt

    logger.error(f"Could not find item {target_item_index} after {max_attempts} attempts")
    return None

def navigate_and_click_level(poco,popup_campaign, target_level, logger):
    """
    Find and click a target level by automatically navigating to the correct world.
    Returns:
        True if level was found and clicked, False otherwise
    Raises:
        RuntimeError: If target level is not found in the expected world
        :param poco:
    """

    # Calculate which world the target level belongs to (7 levels per world)
    expected_world = int((target_level - 1) // 7 + 1)
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
        popup_campaign.btn_select_world.click(sleep_interval=1)
        print("Clicked on world selection buttonnnnnnnnnn")
        popup_campaign= PopupCampaignSelectLv(poco.freeze()) # refresh after click

        # Use swipe_to_target_world to find the target world
        target_world_item = swipe_to_target_world_in_list(poco, popup_campaign, expected_world, logger_name=logger_name
        )

        if not target_world_item:
            logger.error(f"Could not find World {expected_world}")
            return False

        # Click on the target world
        target_world_item.btn_go.click()
        logger.info(f"Clicked on World {expected_world}")
        sleep(2)  # Wait for world to load

        # Verify we're now in the correct world
        popup_campaign= PopupCampaignSelectLv(poco.freeze()) # refresh after world change
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
        popup_campaign= PopupCampaignSelectLv(poco.freeze())
        list_normal = popup_campaign.list_level_normal

        if list_normal:
            logger.info(f"Refresh attempt {refresh_attempt + 1}: Found {len(list_normal)} levels")

            # Search for the target level directly
            for level_item in list_normal:
                if level_item.index:
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
    target_level_item.root.click(sleep_interval=1)
    logger.info(f"Successfully clicked on level {target_level}")

    return True

def is_max_unlocked_level(level_index, all_levels):
    """
    Determine whether the provided level index is the current maximum unlocked level among all_levels.

    A level is considered max if:
    - Its list_star is not None (i.e., it's unlocked/visible), and
    - The next level (index == level_index + 1) exists in all_levels and has list_star == None.

    Args:
        level_index (int): The numeric level index to check (e.g., 2).
        all_levels (Iterable): Iterable of LevelItem-like objects having 'index' and 'list_star' properties.

    Returns:
        bool: True if the level at level_index is max by the above definition, otherwise False.
    """
    # Validate inputs
    if level_index is None:
        return False
    try:
        cur_idx = int(level_index)
    except (TypeError, ValueError):
        return False
    if not all_levels:
        return False

    # Helper to normalize an item's index to int (supports int or digit-string)
    def _idx(item):
        val = getattr(item, 'index', None)
        if isinstance(val, int):
            return val
        if isinstance(val, str) and val.isdigit():
            return int(val)
        return None

    # Find current and next levels
    current_level = None
    next_level = None
    next_idx = cur_idx + 1
    for lv in all_levels:
        idx = _idx(lv)
        if idx is None:
            continue
        if idx == cur_idx:
            current_level = lv
        elif idx == next_idx:
            next_level = lv
        # Early exit if both found
        if current_level is not None and next_level is not None:
            break

    # Current must exist and be unlocked (list_star not None)
    if current_level is None or getattr(current_level, 'list_star', None) is None:
        return False

    # Next must exist and be locked (list_star is None)
    if next_level is None:
        return False

    return getattr(next_level, 'list_star', None) is None

def is_level_unlocked(level_index, all_levels, logger):
    for level in all_levels:
        idx =getattr(level, 'index', None)
        if idx is None:
            continue
        if idx == level_index:
            return  getattr(level, 'list_star', None) is not None
    logger.error(f"Level {level_index} not found in World {all_levels}")
    return False


def get_expected_reward_keys_for_level(level_index):
    """
    Return the list of logical reward keys for a given level index using LEVEL_REWARD_KEYS.
    Example keys: GEM, GOLD, ENERGY, KEY_ENGINE, ITEM_POWER_ATK_UP, etc.
    """
    try:
        lvl = int(level_index)
    except Exception:
        return []
    return LEVEL_REWARD_KEYS.get(lvl, []).copy()

def get_expected_reward_templates_for_level(level_index):
    """
    Return a list of existing template image absolute paths for the expected rewards of a level.
    Uses REWARD_ICON_MAP and filters out non-existent files to avoid false negatives.
    """
    return _get_default_reward_template_paths_for_level(level_index)

def _get_default_reward_template_paths_for_level(level_index):
    """
    Resolve expected reward icon template paths by level index, based on the unity-side mapping.
    Only returns paths that exist on disk to avoid false negatives.

    Known keys mapped to available images:
    - GEM -> image/gemPanelTitle.png
    - GOLD -> image/goldPanelTitle.png
    - ENERGY -> image/energyPanelTitle.png
    Other rewards (keys, item powers, cards) require adding icon images to the repo;
    if present, add their filenames to REWARD_ICON_MAP.
    """
    # Base image directory
    base_img_dir = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'image'))

    # Normalize level_index to int if possible
    try:
        lvl = int(level_index)
    except Exception:
        return []

    keys = LEVEL_REWARD_KEYS.get(lvl, [])

    # Resolve keys to absolute paths and filter to existing files
    paths = []
    for key in keys:
        fname = REWARD_ICON_MAP.get(key)
        if not fname:
            continue
        # Try direct under image/
        path_direct = os.path.join(base_img_dir, fname)
        if os.path.exists(path_direct):
            paths.append(path_direct)
            continue
        # Also try under image/rewards/
        alt = os.path.join(base_img_dir, 'rewards', fname)
        if os.path.exists(alt):
            paths.append(alt)
            continue
    return paths

def claim_mini_chest_and_validate_rewards(level_item, chest_position, poco, logger, level_to_templates=None, retries=5, retry_sleep=0.5, popup_timeout=5.0):
    """
    Claim a mini chest at a given position for a LevelItem, then validate rewards by checking templates.

    Args:
        level_item: LevelItem instance.
        chest_position: tuple(float, float) normalized (0..1) screen position of the chest.
        poco: UnityPoco instance.
        logger: Logger instance.
        level_to_templates: Optional dict[int, list[str]] mapping level index to a list of
            absolute image paths to validate via exists(Template(path)). If None, a default
            per-level mapping will be used from _get_default_reward_template_paths_for_level.
        retries: Number of retries when searching for reward templates.
        retry_sleep: Delay between retries (seconds).
        popup_timeout: Seconds to wait for PopupRewardItem to appear/disappear.

    Returns:
        bool: True if chest was claimed and at least one expected template (when available) was found; else False.
    """
    try:
        if not chest_position or not isinstance(chest_position, (tuple, list)) or len(chest_position) != 2:
            logger.info("Invalid chest_position provided")
            return False

        # 1) Convert normalized coords to pixels for Airtest touch
        screen_w, screen_h = poco.get_screen_size()
        chest_pos_px = (int(chest_position[0] * screen_w), int(chest_position[1] * screen_h))
        logger.info(f"Touching chest at px: {chest_pos_px} (norm: {chest_position})")
        touch(chest_pos_px)

        # 2) Wait for reward popup
        popup = poco("PopupRewardItem(Clone)")
        if not wait_for_element(popup, timeout=popup_timeout, condition="appear"):
            logger.info("PopupRewardItem did not appear after touching chest.")
            return False

        # 3) Determine expected template paths
        idx = getattr(level_item, 'index', None)
        if isinstance(idx, str) and idx.isdigit():
            idx = int(idx)
        if level_to_templates is not None:
            expected_paths = level_to_templates.get(idx, [])
        else:
            expected_paths = _get_default_reward_template_paths_for_level(idx)

        # 4) Validate rewards via templates (skip missing template files without failing)
        found_any = False
        for path in expected_paths:
            try:
                tmpl = Template(path)
            except Exception as e:
                logger.info(f"Invalid template path '{path}': {e}")
                continue

            # Attempt to find each template a few times
            found = None
            for _ in range(max(1, retries)):
                found = exists(tmpl)
                if found:
                    logger.info(f"Found expected reward icon: {path} at {found}")
                    found_any = True
                    break
                sleep(max(0.0, retry_sleep))
            if not found:
                logger.info(f"Expected reward icon not found (may be missing image or different art): {path}")

        # 5) Claim and close the popup to clean up UI
        try:
            btn_claim = popup.offspring("bClaim")
            if btn_claim.exists():
                btn_claim.click()
                wait_for_element(popup, timeout=popup_timeout, condition="disappear")
        except Exception:
            pass

        return found_any if expected_paths else True

    except Exception as e:
        logger.info(f"Error in claim_mini_chest_and_validate_rewards: {e}")
        return False

def _resolve_template_for_key(key):
    """
    Return an absolute template path for a given reward key if the file exists, else None.
    """
    base_img_dir = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'image'))
    fname = REWARD_ICON_MAP.get(key)
    if not fname:
        return None
    path_direct = os.path.join(base_img_dir, fname)
    if os.path.exists(path_direct):
        return path_direct
    alt = os.path.join(base_img_dir, 'rewards', fname)
    if os.path.exists(alt):
        return alt
    return None

def claim_rewards_at_position(level_item, chest_position, poco, logger, popup_timeout=6.0, retries=5, retry_sleep=0.5):
    """
    Touch a given position (normalized), then verify rewards in PopupRewardItem for specific levels.

    - Touches chest_position (normalized 0..1), waits for PopupRewardItem.
    - If level index is one of the known cases, validates that the expected reward icons
      are present (exists(Template)) and their amounts match.
    - Supports both single-item popup (with child 'single') cycling through multiple rewards
      and a multi-item layout by best-effort checks.

    Args:
        level_item: LevelItem instance (must have 'index').
        chest_position: (x_norm, y_norm) normalized coordinates.
        poco: UnityPoco instance.
        logger: logger instance.
        popup_timeout: seconds to wait for reward popup appearance/disappearance.
        retries: retries for template existence polling.
        retry_sleep: sleep between retries.

    Returns:
        bool: True if all expected rewards (for known levels) were verified, else False.
              For unknown levels, returns True after a successful claim.
    """
    try:
        if not chest_position or not isinstance(chest_position, (tuple, list)) or len(chest_position) != 2:
            logger.info("Invalid chest_position provided")
            return False

        # 1) Touch the provided normalized position
        sw, sh = poco.get_screen_size()
        px = (int(chest_position[0] * sw), int(chest_position[1] * sh))
        logger.info(f"Touch at chest pos px={px} (norm={chest_position})")
        touch(px)

        # 2) Wait for PopupRewardItem
        popup = poco("PopupRewardItem(Clone)")
        if not wait_for_element(popup, timeout=popup_timeout, condition="appear"):
            logger.info("PopupRewardItem did not appear after touching chest.")
            return False

        # 3) Determine expected rewards for this level
        idx = getattr(level_item, 'index', None)
        if isinstance(idx, str) and idx.isdigit():
            idx = int(idx)

        expected = LEVEL_REWARD_AMOUNTS.get(idx)
        # Unknown level mapping: claim and exit success
        if not expected:
            logger.info(f"No predefined rewards for level {idx}, claiming popup.")
            btn = popup.offspring("bClaim")
            if btn.exists():
                btn.click()
                wait_for_element(popup, timeout=popup_timeout, condition="disappear")
            return True

        # Build a working list with templates
        # Each item: {key, amount, template_path or None}
        work = []
        for key, amt in expected:
            work.append({
                'key': key,
                'amount': int(amt),
                'template': _resolve_template_for_key(key)
            })

        # Helper to poll for template existence
        def _wait_exists(tpl_path):
            if not tpl_path:
                return False
            tpl = Template(tpl_path)
            for _ in range(max(1, retries)):
                if exists(tpl):
                    return True
                sleep(max(0.0, retry_sleep))
            return False

        # 4) Single-item popup mode: detect and iterate expected rewards
        # Heuristic: presence of child 'single' or exactly one UIItemIcon
        single_node = popup.offspring("single")
        is_single = single_node.exists()
        if is_single:
            remaining = work.copy()
            max_loops = len(remaining) + 2  # safety bound
            verified_all = True
            while remaining and max_loops > 0:
                max_loops -= 1
                # Try to match any remaining expected by template
                matched_index = None
                for i, item in enumerate(remaining):
                    if _wait_exists(item['template']):
                        # Read amount
                        qty_node = popup.offspring("lQuantity")
                        actual_amt = clean_number(qty_node.get_text()) if qty_node.exists() else 1
                        if int(actual_amt) == int(item['amount']):
                            logger.info(f"Verified reward: {item['key']} x{actual_amt}")
                            matched_index = i
                            break
                        else:
                            logger.info(f"Amount mismatch for {item['key']}: expected {item['amount']} got {actual_amt}")
                if matched_index is None:
                    verified_all = False
                    logger.info("Could not match any remaining expected reward in single popup.")
                    break
                # Claim and wait for next
                try:
                    btn = popup.offspring("bClaim")
                    if btn.exists():
                        btn.click()
                        wait_for_element(popup, timeout=popup_timeout, condition="disappear")
                except Exception:
                    pass
                # Remove matched and if more expected, wait for popup to reappear
                remaining.pop(matched_index)
                if remaining:
                    if not wait_for_element(popup, timeout=popup_timeout, condition="appear"):
                        logger.info("Next reward popup did not appear.")
                        verified_all = False
                        break
            return verified_all and not remaining

        # 5) Multi-item layout: delegate verification to shared helper
        verified = verify_popup_reward_contents(level_item, poco, logger, retries=retries, retry_sleep=retry_sleep)
        # Claim and close
        try:
            btn = popup.offspring("bClaim")
            if btn.exists():
                btn.click()
                wait_for_element(popup, timeout=popup_timeout, condition="disappear")
        except Exception:
            pass

        return verified

    except Exception as e:
        logger.info(f"Error in claim_rewards_at_position: {e}")
        return False

def verify_popup_reward_contents(level_item, poco, logger, retries=5, retry_sleep=0.5):
    """
    Verify rewards currently displayed in PopupRewardItem without mutating UI state.

    Handles two layouts:
    - Single reward: verifies the currently visible reward only (matches any one expected pair).
    - Multi rewards: verifies that all expected amounts are present among multi/content children
      and that expected icons exist via templates when available.

    Args:
        level_item: LevelItem instance (provides level index)
        poco: UnityPoco instance
        logger: logger instance
        retries: template polling retries
        retry_sleep: sleep between polls in seconds

    Returns:
        bool: True if verification passes for the visible contents; False otherwise.
              If level has no predefined mapping, returns True.
    """
    popup = poco("PopupRewardItem(Clone)")
    if not popup.exists():
        logger.info("PopupRewardItem not present for verification")
        return False

    # Resolve expected reward pairs for this level
    idx = getattr(level_item, 'index', None)
    if isinstance(idx, str) and idx.isdigit():
        idx = int(idx)
    expected = LEVEL_REWARD_AMOUNTS.get(idx)
    if not expected:
        # Nothing to verify for this level
        logger.info(f"No predefined rewards for level {idx}, skipping verification.")
        return True

    # Build working expected set with templates
    work = []
    for key, amt in expected:
        work.append({
            'key': key,
            'amount': int(amt),
            'template': _resolve_template_for_key(key)
        })

    def _wait_exists(tpl_path):
        if not tpl_path:
            return False
        tpl = Template(tpl_path)
        for _ in range(max(1, retries)):
            if exists(tpl):
                return True
            sleep(max(0.0, retry_sleep))
        return False

    # Detect layout
    is_single = popup.offspring("single").exists()

    if is_single:
        # Single: verify currently visible reward matches any expected pair
        qty_node = popup.offspring("lQuantity")
        actual_amt = clean_number(qty_node.get_text()) if qty_node.exists() else 1
        for item in work:
            icon_ok = True
            if item['template']:
                icon_ok = _wait_exists(item['template'])
            if icon_ok and int(actual_amt) == int(item['amount']):
                logger.info(f"Single reward verified: {item['key']} x{actual_amt}")
                return True
        logger.info("Single reward did not match any expected item")
        return False

    # Multi: enumerate children amounts and validate expected multiset + icons
    amounts_in_popup = []
    multi_content = popup.offspring("multi").offspring("content")
    if multi_content.exists():
        try:
            for child in multi_content.children():
                try:
                    q = child.offspring("lQuantity")
                    amt = clean_number(q.get_text()) if q.exists() else 1
                    amounts_in_popup.append(int(amt))
                except Exception:
                    continue
        except Exception:
            pass
    else:
        # Fallback: scan all lQuantity under popup
        qty_nodes = popup.offspring("lQuantity")
        try:
            for n in qty_nodes:
                if n.exists():
                    amounts_in_popup.append(int(clean_number(n.get_text())))
        except TypeError:
            if qty_nodes.exists():
                amounts_in_popup.append(int(clean_number(qty_nodes.get_text())))

    icons_ok = True
    amounts_ok = True

    # Icon presence (global search) and amounts multiset check
    for item in work:
        if item['template'] and not _wait_exists(item['template']):
            logger.info(f"Expected icon not found for {item['key']}")
            icons_ok = False
        required = int(item['amount'])
        if required in amounts_in_popup:
            amounts_in_popup.remove(required)
        else:
            logger.info(f"Expected amount not present for {item['key']}: {required}")
            amounts_ok = False

    return icons_ok and amounts_ok

def has_valid_mini_chest(level_item, poco, logger, vertical_tolerance=50, retries=5, retry_sleep=0.5):
    """
    Detect a valid mini chest for a given LevelItem and return its normalized position.

    A mini chest is considered valid if:
    - The level has a mini chest node present, and
    - The mini chest template can be found on screen to the right of the level's
      normalized position and within a vertical tolerance (pixels converted to normalized).

    Args:
        level_item: LevelItem instance from PopupCampaignSelectLv
        poco: UnityPoco instance
        logger: Logger instance to use for logging
        vertical_tolerance: Allowed vertical distance between level and chest, in pixels
        retries: Number of retries to search for the chest template
        retry_sleep: Delay between retries in seconds

    Returns:
        tuple(float, float): chest normalized position (x, y) if found; otherwise None.
    """
    try:
        if not level_item or not getattr(level_item, 'root', None) or not level_item.root.exists():
            logger.info("Level item/root not available")
            return None

        if not getattr(level_item, 'mini_chest', None):
            logger.info(f"Level {getattr(level_item, 'index', None)} has no mini chest node")
            return None

        screen_width, screen_height = poco.get_screen_size()
        if not screen_width or not screen_height:
            logger.info("Invalid screen size")
            return None

        level_pos_normalized = level_item.root.get_position()
        if not level_pos_normalized:
            logger.info("Could not get normalized level position")
            return None
        logger.info(f"Level {getattr(level_item, 'index', None)} normalized position: {level_pos_normalized}")

        from airtest.core.api import find_all
        chest_results = None
        for _ in range(max(1, retries)):
            chest_results = find_all(level_item.mini_chest_image_template)
            if chest_results:
                break
            sleep(max(0.0, retry_sleep))

        if not chest_results:
            logger.info("No chest templates found")
            return None

        vertical_tolerance_norm = float(vertical_tolerance) / float(screen_height)

        for i, chest_result in enumerate(chest_results):
            try:
                chest_pos_px = chest_result['result']
                confidence = chest_result.get('confidence', None)
                chest_pos_norm = (
                    float(chest_pos_px[0]) / float(screen_width),
                    float(chest_pos_px[1]) / float(screen_height)
                )
                dx_norm = chest_pos_norm[0] - level_pos_normalized[0]
                dy_norm = abs(chest_pos_norm[1] - level_pos_normalized[1])
                logger.info(
                    f"Chest {i}: px={chest_pos_px}, norm={chest_pos_norm}, conf={confidence}, dx_norm={dx_norm:.4f}, |dy_norm|={dy_norm:.4f}, tol_norm={vertical_tolerance_norm:.4f}"
                )
                if (chest_pos_norm[0] - level_pos_normalized[0]) in range(1,60)  and dy_norm < vertical_tolerance_norm:
                    return chest_pos_norm
            except Exception as e:
                logger.info(f"Error processing chest result {i}: {e}")
                continue

        logger.info("No valid mini chest found near the level")
        return None

    except Exception as e:
        logger.info(f"Error in has_valid_mini_chest: {e}")
        return None

def verify_popup_reward_contents_expected(poco, expected_rewards, logger, retries=5, retry_sleep=0.5):
    """
    Verify the rewards shown in PopupRewardItem against explicitly provided expectations.

    Supports both single and multi reward layouts.

    Args:
        poco: UnityPoco instance
        expected_rewards: list of dictionaries, each with keys:
            - 'template': str or None (absolute image path for exists(Template))
            - 'amount': int or None (expected numeric quantity)
            For multi, provide multiple dicts. For single, provide exactly one dict.
        logger: logger instance
        retries: template polling retries for exists(Template)
        retry_sleep: delay between retries in seconds

    Returns:
        bool: True if the popup contents match the expected rewards; False otherwise.
    """
    popup = poco("PopupRewardItem(Clone)")
    if not popup.exists():
        logger.info("PopupRewardItem not present for verification")
        return False

    # Validate and normalize expected input strictly to list[dict]
    if not isinstance(expected_rewards, list):
        logger.info(f"expected_rewards must be a list of dicts, got: {type(expected_rewards)}")
        return False
    if not expected_rewards:
        logger.info("expected_rewards is an empty list")
        return False

    expectation = []
    for idx, item in enumerate(expected_rewards):
        if not isinstance(item, dict):
            logger.info(f"expected_rewards[{idx}] is not a dict: {type(item)}")
            return False
        tpl = item.get('template', None)
        amt = item.get('amount', None)
        if tpl is not None and not isinstance(tpl, str):
            logger.info(f"expected_rewards[{idx}].template must be str or None, got: {type(tpl)}")
            return False
        if amt is not None:
            try:
                amt = int(amt)
            except Exception:
                logger.info(f"expected_rewards[{idx}].amount must be int-like, got: {item.get('amount')}")
                return False
        # Check that at least one spec is provided
        if tpl is None and amt is None:
            logger.info(f"expected_rewards[{idx}] must include 'template' and/or 'amount'")
            return False
        expectation.append({'template': tpl, 'amount': amt})

    def _wait_exists(tpl_path):
        if not tpl_path:
            return False
        try:
            tpl = Template(tpl_path)
        except Exception as e:
            logger.info(f"Invalid template path '{tpl_path}': {e}")
            return False
        for _ in range(max(1, retries)):
            if exists(tpl):
                return True
            sleep(max(0.0, retry_sleep))
        return False

    is_single = popup.offspring("single").exists()

    if is_single:
        # Single layout requires exactly one expected spec
        if len(expectation) != 1:
            logger.info("Single reward popup but multiple/none expected items provided")
            return False
        expected = expectation[0]
        # Icon check
        icon_ok = True
        if expected['template']:
            icon_ok = _wait_exists(expected['template'])
        # Amount check
        amount_ok = True
        qty_node = popup.offspring("lQuantity")
        actual_amt = clean_number(qty_node.get_text()) if qty_node.exists() else 1
        if expected['amount'] is not None and int(actual_amt) != int(expected['amount']):
            amount_ok = False
            logger.info(f"Amount mismatch: expected {expected['amount']} got {actual_amt}")
        # Require at least one of icon/amount to be specified
        if expected['template'] is None and expected['amount'] is None:
            logger.info("Expected spec must include template and/or amount for single reward")
            return False
        return icon_ok and amount_ok

    # Multi layout: collect all child quantities
    amounts_in_popup = []
    multi_content = popup.offspring("multi").offspring("content")
    if multi_content.exists():
        try:
            for child in multi_content.children():
                try:
                    q = child.offspring("lQuantity")
                    amt = clean_number(q.get_text()) if q.exists() else 1
                    amounts_in_popup.append(int(amt))
                except Exception:
                    continue
        except Exception:
            pass
    else:
        # Fallback: scan all lQuantity under popup
        qty_nodes = popup.offspring("lQuantity")
        try:
            for n in qty_nodes:
                if n.exists():
                    amounts_in_popup.append(int(clean_number(n.get_text())))
        except TypeError:
            if qty_nodes.exists():
                amounts_in_popup.append(int(clean_number(qty_nodes.get_text())))

    icons_ok = True
    amounts_ok = True

    # Icons: ensure each expected with a template exists on screen
    for exp in expectation:
        if exp['template'] and not _wait_exists(exp['template']):
            logger.info(f"Expected icon not found: {exp['template']}")
            icons_ok = False

    # Amounts: multiset containment
    amounts_pool = list(amounts_in_popup)
    for exp in expectation:
        if exp['amount'] is None:
            continue
        required = int(exp['amount'])
        if required in amounts_pool:
            amounts_pool.remove(required)
        else:
            logger.info(f"Expected amount not present: {required}")
            amounts_ok = False

    return icons_ok and amounts_ok
