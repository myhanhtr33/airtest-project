# UI Scrollview Helper

A reusable utility module for handling scrollview interactions in grid-based UI layouts.

## Location
`utils/UI_scrollview_helper.py`

## Functions

### 1. `calculate_row_distance(items, items_per_row=4)`

Calculates the average vertical distance between rows in a grid layout.

**Parameters:**
- `items` - List of items with `root.get_position()` method
- `items_per_row` - Number of items in each row (default: 4)

**Returns:** `float` - Average vertical distance between rows, or 0 if cannot calculate

**Example:**
```python
from utils.UI_scrollview_helper import calculate_row_distance

items = popup.items
row_distance = calculate_row_distance(items, items_per_row=4)
print(f"Distance between rows: {row_distance}px")
```

---

### 2. `is_item_below_threshold(item, threshold_y, items_per_row=4, all_items=None)`

Checks if an item is below a threshold y-position (accounting for item height).

**Parameters:**
- `item` - The item to check
- `threshold_y` - The y-position threshold (e.g., weapon_points y-position)
- `items_per_row` - Number of items per row (default: 4)
- `all_items` - List of all items for calculating row distance (optional)

**Returns:** `bool` - True if item needs scrolling, False if visible

**Example:**
```python
from utils.UI_scrollview_helper import is_item_below_threshold

weapon_point_y = popup.weapon_points[0].root.get_position()[1]
needs_scroll = is_item_below_threshold(
    item, 
    threshold_y=weapon_point_y, 
    items_per_row=4,
    all_items=popup.items
)
```

---

### 3. `scroll_to_item(item, scrollview, threshold_y=None, items_per_row=4, all_items=None)`

Scrolls to make an item visible if it's below the threshold.

**Parameters:**
- `item` - The item to scroll to
- `scrollview` - The scrollview element to perform swipe on
- `threshold_y` - The y-position threshold for visibility (optional)
- `items_per_row` - Number of items per row (default: 4)
- `all_items` - List of all items for calculating row distance (optional)

**Returns:** `bool` - True if scrolling was performed, False if already visible

**Example:**
```python
from utils.UI_scrollview_helper import scroll_to_item

weapon_point_y = popup.weapon_points[0].root.get_position()[1]
scrolled = scroll_to_item(
    item,
    scrollview=popup.scrollview,
    threshold_y=weapon_point_y,
    items_per_row=4,
    all_items=popup.items
)
```

---

## Usage in Tests

### Basic Usage

```python
from utils.UI_scrollview_helper import scroll_to_item

def test_scroll_through_items(poco):
    popup = PopupMilitaryGetPoint(poco, "Air")
    weapon_point_y = popup.weapon_points[0].root.get_position()[1]
    
    for item in popup.items:
        # Scroll to item if needed
        scroll_to_item(
            item,
            scrollview=popup.scrollview,
            threshold_y=weapon_point_y,
            items_per_row=4,
            all_items=popup.items
        )
        
        # Interact with the item
        item.root.click()
```

### Using with Popup's Built-in Method

The `PopupMilitaryGetPoint` class wraps the helper function:

```python
def test_using_popup_method(poco):
    popup = PopupMilitaryGetPoint(poco, "Air")
    
    for item in popup.items:
        # This internally uses the helper function
        popup.scroll_to_item(item, items_per_row=4)
        item.root.click()
```

### Reusable Pattern for Any Grid Popup

```python
from utils.UI_scrollview_helper import scroll_to_item

def scroll_and_process_items(popup, items_per_row=4):
    """Generic function for any grid-based popup."""
    # Get threshold
    threshold_y = None
    if hasattr(popup, 'weapon_points') and popup.weapon_points:
        threshold_y = popup.weapon_points[0].root.get_position()[1]
    
    # Process all items with auto-scrolling
    for item in popup.items:
        scroll_to_item(
            item,
            scrollview=popup.scrollview,
            threshold_y=threshold_y,
            items_per_row=items_per_row,
            all_items=popup.items
        )
        
        # Your logic here
        yield item
```

---

## How It Works

### Problem
In grid-based scrollviews, items arranged in rows may be partially or fully hidden below the viewport. Simply checking if an item's y-position is below a threshold doesn't account for the item's height.

### Solution
1. **Calculate Row Distance**: Measures the vertical distance between the first and second rows
2. **Adjust Item Position**: Adds row distance to item's y-position to check the bottom edge
3. **Smart Scrolling**: Only scrolls if the adjusted position is below the threshold

```
Item Top Y: 800
Row Distance: 150 (item height + spacing)
Adjusted Y: 950 (800 + 150)
Threshold: 900

Is 950 >= 900? YES → Scroll needed
```

---

## Files

- **Core Module**: `utils/UI_scrollview_helper.py`
- **Examples**: `utils/UI_scrollview_helper_examples.py`
- **Used In**: 
  - `Hierarchy/PopupMilitary.py` → `PopupMilitaryGetPoint` class
  - `tests/Military/test_PopupMilitary.py` → `test_frozen_UI` method

---

## Benefits

✅ **Reusable** - Use in any test file with grid-based scrollviews  
✅ **Accurate** - Accounts for item height and spacing  
✅ **Flexible** - Works with any number of items per row  
✅ **Well-tested** - Already integrated in PopupMilitary tests  
✅ **Documented** - Clear examples and usage patterns

