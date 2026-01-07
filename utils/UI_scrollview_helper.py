"""
UI Scrollview Helper Utilities

This module provides helper functions for handling scrollview interactions
in UI automation tests, particularly for grid-based layouts.
"""


def calculate_row_distance(items, items_per_row=4):
    """
    Calculate the average vertical distance between rows in a grid layout.

    This is useful for determining if an item in a scrollview is fully visible
    or if scrolling is needed to bring it into view.

    Args:
        items: List of items (HangarItem, PilotItem, or any object with root.get_position())
        items_per_row: Number of items in each row (default: 4)

    Returns:
        float: Average vertical distance between rows, or 0 if cannot calculate

    Example:
        >>> items = popup.items
        >>> row_distance = calculate_row_distance(items, items_per_row=4)
        >>> adjusted_y = item_y + row_distance
    """
    if len(items) < items_per_row + 1:
        print("[calculate_row_distance] Not enough items to calculate row distance")
        return 0

    # Get y positions of items in first row
    first_row_y = []
    for i in range(min(items_per_row, len(items))):
        if items[i].root.exists():
            first_row_y.append(items[i].root.get_position()[1])

    # Get y positions of items in second row
    second_row_start = items_per_row
    second_row_y = []
    for i in range(second_row_start, min(second_row_start + items_per_row, len(items))):
        if items[i].root.exists():
            second_row_y.append(items[i].root.get_position()[1])

    if not first_row_y or not second_row_y:
        print("[calculate_row_distance] Could not get positions for row distance calculation")
        return 0

    # Calculate average y for each row
    avg_first_row_y = sum(first_row_y) / len(first_row_y)
    avg_second_row_y = sum(second_row_y) / len(second_row_y)

    # Distance between rows (includes item height + spacing)
    row_distance = abs(avg_second_row_y - avg_first_row_y)
    print(f"[calculate_row_distance] Row distance: {row_distance} (items_per_row={items_per_row})")

    return row_distance


def is_item_below_threshold(item, threshold_y, items_per_row=4, all_items=None):
    """
    Check if an item is below a threshold y-position, accounting for item height.

    Args:
        item: The item to check (must have root.get_position() method)
        threshold_y: The y-position threshold (e.g., weapon_points y-position)
        items_per_row: Number of items per row in the grid (default: 4)
        all_items: List of all items for calculating row distance (optional)

    Returns:
        bool: True if item is below threshold (needs scrolling), False otherwise

    Example:
        >>> needs_scroll = is_item_below_threshold(item, weapon_point_y, items_per_row=4, all_items=popup.items)
    """
    if not item.root.exists():
        print(f"[is_item_below_threshold] Item {item.root} does not exist")
        return False

    item_y = item.root.get_position()[1]

    # If all_items provided, calculate row distance for accurate detection
    if all_items:
        row_distance = calculate_row_distance(all_items, items_per_row)
        adjusted_item_y = item_y + row_distance
        print(f"[is_item_below_threshold] Item y: {item_y}, Adjusted y: {adjusted_item_y}, Threshold: {threshold_y}")
        return adjusted_item_y >= threshold_y
    else:
        # Fallback: just compare item y with threshold
        print(f"[is_item_below_threshold] Item y: {item_y}, Threshold: {threshold_y} (no adjustment)")
        return item_y >= threshold_y


def scroll_to_item(item, scrollview, threshold_y=None, items_per_row=4, all_items=None):
    """
    Scroll to make an item visible in a scrollview if it's below the threshold.

    Args:
        item: The item to scroll to (must have root.get_position() and root.focus() methods)
        scrollview: The scrollview element to perform swipe on (fallback)
        threshold_y: The y-position threshold for visibility (optional)
        items_per_row: Number of items per row in the grid (default: 4)
        all_items: List of all items for calculating row distance (optional)

    Returns:
        bool: True if scrolling was performed, False if item already visible

    Example:
        >>> from utils.UI_scrollview_helper import scroll_to_item
        >>> scroll_to_item(item, popup.scrollview, threshold_y=weapon_point_y, items_per_row=4, all_items=popup.items)
    """
    import time

    if not item.root.exists():
        print(f"[scroll_to_item] Item {item.root} does not exist, skipping")
        return False

    item_y = item.root.get_position()[1]
    print(f"[scroll_to_item] Item {item.root} y-axis: {item_y}")

    # If threshold provided, check if scrolling is needed
    if threshold_y is not None:
        if all_items:
            row_distance = calculate_row_distance(all_items, items_per_row)
            adjusted_item_y = item_y + row_distance
            print(f"[scroll_to_item] Adjusted item y (item_y + row_distance): {adjusted_item_y}")

            if adjusted_item_y < threshold_y:
                print(f"[scroll_to_item] Item is visible, no scroll needed")
                return False
        else:
            if item_y < threshold_y:
                print(f"[scroll_to_item] Item is visible, no scroll needed")
                return False

    # Item is below threshold or no threshold provided - scroll to it
    print(f"[scroll_to_item] Item is below threshold, scrolling...")

    try:
        # Option 1: Focus on the item (brings it to center if possible)
        item.root.focus('vertical')
        time.sleep(0.5)
        print(f"[scroll_to_item] Focused on item {item.root}")
        return True
    except Exception as e:
        print(f"[scroll_to_item] Focus failed: {e}, trying swipe")
        # Option 2: Swipe up to scroll down
        try:
            scrollview.swipe([0, -0.3])  # Negative y to scroll down
            time.sleep(0.5)
            print(f"[scroll_to_item] Swiped scrollview")
            return True
        except Exception as e2:
            print(f"[scroll_to_item] Swipe also failed: {e2}")
            return False

