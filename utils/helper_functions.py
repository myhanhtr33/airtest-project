import time
from poco.exceptions import PocoNoSuchNodeException
from utils.get_resource_amount import *
from airtest.core.api import swipe, sleep
from logger_config import get_logger

def wait_for_element(poco_obj, timeout=3, interval=0.5, condition="appear"):
    """
    Wait for a Poco object to appear or disappear.
    :param poco_obj: Poco element to check (must be a live query, not stale).
    :param timeout: How long to wait in seconds.
    :param interval: How frequently to check.
    :param condition: 'appear' or 'disappear'.
    :return: True if condition met within timeout, False otherwise.
    """
    elapsed = 0
    while elapsed < timeout:
        exists = False
        if poco_obj:
            exists = poco_obj.exists()
        if (condition == "appear" and exists) or (condition == "disappear" and not exists):
            return True
        time.sleep(interval)
        elapsed += interval
    return False

def maybe_handle_vip_congrats(poco, timeout=5.0, poll_interval=0.5):
    """
    If the VIP “Congratulations” popup ever appears, close it. Otherwise do nothing.

    :param timeout: total seconds to wait for the popup to appear
    :param poll_interval: how often (seconds) to poll
    """
    popup = poco("PopupVipCongratulation(Clone)")
    elapsed = 0.0

    # 1) Poll until either the popup appears or we exceed the timeout
    while elapsed < timeout:
        try:
            if popup.exists():
                print(f"[Info] VIP‐Congrats popup detected after {elapsed:.1f}s.")
                # 2) Once it’s detected, click its “Close” button:
                close_btn = popup.offspring("btnTaptoclose")
                if close_btn.exists():
                    close_btn.click()
                    # 3) Wait for it to actually disappear before returning
                    end_time = 0.0
                    while end_time < timeout:
                        if not popup.exists():
                            print("[Info] VIP‐Congrats popup closed successfully.")
                            return
                        time.sleep(poll_interval)
                        end_time += poll_interval
                    # If we get here, the popup never vanished, but we’ll bail anyway
                    print("[Warning] VIP‐Congrats popup did not disappear after clicking Close.")
                    return
                else:
                    print("[Warning] VIP‐Congrats popup close button not found.")
                    return
        except Exception as e:
            # Silently handle any exceptions during polling
            pass

        time.sleep(poll_interval)
        elapsed += poll_interval

    # If we reach here, no popup appeared within the timeout period.
    # This is normal behavior, so we don't print anything.

def check_noti(poco, expected_text):
    noti= poco("PanelNotification").offspring("lNotification")
    assert wait_for_element(noti, condition="appear"), "Notification not found!"
    print("✅ Notification appeared.")
    actual_text = noti.get_text().strip()
    assert actual_text == expected_text, f"Unexpected notification text: '{expected_text}'"
    # 3. Wait for disappearance
    assert wait_for_element(noti, condition="disappear"), "Notification did not disappear!"
    print("✅ Notification disappeared.")

def check_popup_claim_known_resourcce(poco,expected_amount,expected_sprite,logger):
    """
        Validates the appearance and content of a reward popup, ensuring the displayed
        reward matches the expected sprite and amount, and then claims the reward.
        """
    if "pilot" in expected_sprite.lower():
        popupPilot=poco("PopupReceivePilot(Clone)")
        wait_for_element(popupPilot, condition="appear", timeout=5)
        popupPilot.offspring("B_Skip").click()
        return
    popupClaim = poco("PopupRewardItem(Clone)")
    wait_for_element(popupClaim, condition="appear", timeout=5)
    #enigne dont have lQuantity
    actual_amount=clean_number(popupClaim.offspring("lQuantity").get_text()) if popupClaim.offspring("lQuantity").exists() else 1

    if popupClaim.exists():
        actual_reward = {
            "sprite": popupClaim.offspring("sIcon").attr("texture"),
            "amount": actual_amount
        }
    else:
        raise RuntimeError(f"Reward popup did not appear after 5 seconds.")
    assert actual_reward["sprite"] == expected_sprite, f"reward sprite mismatch: expected {expected_sprite}, got {actual_reward['sprite']}"
    logger.info(f"actual reward sprite {actual_reward["sprite"]} meet expected {expected_sprite}")
    assert actual_reward["amount"] == expected_amount, f"reward amount mismatch: expected {expected_amount}, got {actual_reward['amount']}"
    logger.info(f"actual reward amount {actual_reward['amount']} meet expected {expected_amount}")
    btnClaim = popupClaim.offspring("bClaim")
    btnClaim.click()

def swipe_to_scrollview_item(panel_worlds, target_item_index, max_attempts=10, logger_name="ScrollviewHelper"):
    """
    Swipe to find and display a target item in a scrollview.
    This is a generic helper function that can be used with any scrollview containing indexed items.

    Args:
        panel_worlds: Object containing the scrollview with title and list_world properties
        target_item_index: The index (1-based) of the item to find
        max_attempts: Maximum number of swipe attempts
        logger_name: Name for the logger instance

    Returns:
        Item object if found, None otherwise
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
        logger.info(f"Attempt {attempt + 1}: Looking for item {target_item_index}")

        # Only build cache on first attempt or if cache is empty
        if cached_items is None:
            logger.info("Building item cache...")
            list_items = panel_worlds.list_world  # Generic property name
            if not list_items:
                logger.warning("No items found in current view")
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

            if len(cached_items) < 2:
                logger.warning("Not enough valid items found")
                continue

            logger.info(f"Cached {len(cached_items)} valid items")

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
            logger.warning("Not enough items with valid positions")
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

        # Sort visible items by Y position and take first 8
        visible_items.sort(key=lambda x: x[2][1])
        visible_items = visible_items[:8]

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
                logger.info(f"Found target item {target_item_index} at position {item_pos}")
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
