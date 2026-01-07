"""
Example usage of UI_scrollview_helper utilities

This file demonstrates how to use the scrollview helper functions
in your test files.
"""

from utils.UI_scrollview_helper import calculate_row_distance, is_item_below_threshold, scroll_to_item


# Example 1: Calculate row distance
def example_calculate_row_distance(popup):
    """
    Calculate the distance between rows in a grid layout.
    """
    items = popup.items
    row_distance = calculate_row_distance(items, items_per_row=4)
    print(f"Row distance: {row_distance}")
    return row_distance


# Example 2: Check if item needs scrolling
def example_check_item_visibility(item, weapon_point_y, popup):
    """
    Check if an item is below the threshold and needs scrolling.
    """
    needs_scroll = is_item_below_threshold(
        item,
        threshold_y=weapon_point_y,
        items_per_row=4,
        all_items=popup.items
    )

    if needs_scroll:
        print(f"Item {item.root} needs scrolling")
    else:
        print(f"Item {item.root} is visible")

    return needs_scroll


# Example 3: Scroll to item
def example_scroll_to_item(item, popup, weapon_point_y):
    """
    Scroll to make an item visible if needed.
    """
    scrolled = scroll_to_item(
        item,
        scrollview=popup.scrollview,
        threshold_y=weapon_point_y,
        items_per_row=4,
        all_items=popup.items
    )

    if scrolled:
        print(f"Scrolled to item {item.root}")
    else:
        print(f"Item {item.root} was already visible")

    return scrolled


# Example 4: Full workflow in a test
def example_test_workflow(poco):
    """
    Complete example of using scrollview helpers in a test.
    """
    from Hierarchy.PopupMilitary import PopupMilitaryGetPoint

    # Open popup
    popup_get_point = PopupMilitaryGetPoint(poco, "Air")

    # Get weapon points threshold
    weapon_point_y = popup_get_point.weapon_points[0].root.get_position()[1]

    # Iterate through all items
    for item in popup_get_point.items:
        # Option 1: Use the helper function directly
        scroll_to_item(
            item,
            scrollview=popup_get_point.scrollview,
            threshold_y=weapon_point_y,
            items_per_row=4,
            all_items=popup_get_point.items
        )

        # Option 2: Or use the popup's scroll_to_item method (which uses the helper internally)
        # popup_get_point.scroll_to_item(item, items_per_row=4)

        # Now interact with the item
        item.root.click()


# Example 5: Reusable scroll helper for any grid-based popup
def scroll_and_interact_with_all_items(popup, items_per_row=4):
    """
    Generic function to scroll through and interact with all items in any popup.

    Args:
        popup: Any popup object with .items, .weapon_points, and .scrollview attributes
        items_per_row: Number of items per row in the grid
    """
    # Get threshold from weapon points
    if hasattr(popup, 'weapon_points') and popup.weapon_points:
        threshold_y = popup.weapon_points[0].root.get_position()[1]
    else:
        threshold_y = None  # Will scroll to all items without threshold check

    # Process each item
    for idx, item in enumerate(popup.items):
        print(f"Processing item {idx + 1}/{len(popup.items)}")

        # Scroll to item if needed
        scroll_to_item(
            item,
            scrollview=popup.scrollview if hasattr(popup, 'scrollview') else popup.middle_panel,
            threshold_y=threshold_y,
            items_per_row=items_per_row,
            all_items=popup.items
        )

        # Your interaction logic here
        if item.root.exists():
            print(f"Item {item.root} is now visible and ready for interaction")
            # item.root.click()
            # check_item(item)
            # etc.

