from Hierarchy.CurrencyBar import CurrencyBar
from airtest.core.api import *
import re
from utils.sprite_mapping import *

def get_single_resource_amount(poco, resource_type):
    """
    Get the amount of a specific resource from the currency bar.

    :param poco: The Poco instance for interacting with the UI.
    :param resource_type: The type of resource to get (e.g., "gold", "energy", "gem").
    :return: The amount of the specified resource.
    """
    bar = CurrencyBar(poco)

    if resource_type == "gold":
        return clean_number(bar.gold_home.gold_amount().get_text())
    elif resource_type == "energy":
        return clean_number(bar.energy_home.energy_amount().get_text())
    elif resource_type == "gem":
        return clean_number(bar.gem_home.gem_amount().get_text())
    else:
        raise ValueError("Invalid resource type specified.")

def get_all_resource_amounts(poco):
    """
    Get the amounts of all resources from the currency bar.

    :param poco: The Poco instance for interacting with the UI.
    :return: A dictionary containing the amounts of all resources.
    """
    return {
        "gold": get_single_resource_amount(poco, "gold"),
        "energy": get_single_resource_amount(poco, "energy"),
        "gem": get_single_resource_amount(poco, "gem"),
        # "cardA1": poco.invoke("get_card_amount", cardType="ITEM_CARD_PLANE_1"),
        # "cardA2": poco.invoke("get_card_amount", cardType="ITEM_CARD_PLANE_2"),
        # "cardA3": poco.invoke("get_card_amount", cardType="ITEM_CARD_PLANE_3"),

    }

def get_all_card_amounts(poco):
    dictionaryCard = {}
    for key in CARD_SPRITE_MAPPING.keys():
        dictionaryCard[key] = get_single_card_amount(poco, key)
    return dictionaryCard

def get_single_card_amount(poco, card_type):
    result= poco.invoke("get_card_amount", cardType=card_type)
    amount= result.get("amount")
    name= result.get("card_id")
    return amount,name
def get_single_card_amount_by_sprite(poco, sprite_name):
    """
    Get the amount of a specific card by its sprite name.

    :param poco: The Poco instance for interacting with the UI.
    :param sprite_name: The sprite name of the card.
    :return: The amount of the specified card.
    """
    for key, value in CARD_SPRITE_MAPPING.items():
        if value == sprite_name:
            result= poco.invoke("get_card_amount", cardType=key)
            if result.get("status") != "success":
                raise ValueError(f"Failed to get card amount for {key}: {result.get('message', 'Unknown error')}")
            amount = result.get("amount")
            name = result.get("card_id")
            return amount, name

    raise ValueError(f"No card found with sprite name: {sprite_name}")


def clean_number(text):
    """
    Convert shorthand like '13.38K', '1M8', '12B5' into full integers.
    Handles formats like:
        - '13.38K' → 13380
        - '1M8'    → 1,800,000
        - '12B5'   → 12,500,000,000
    """
    if not text:
        return 0

    # Clean raw text
    cleaned = text.replace(",", "").replace(" ", "").replace(" ", "").strip().upper()

    # Case 1: Normal decimal + suffix (e.g., 13.5K)
    match = re.match(r"^(\d+(?:\.\d+)?)([KMB])$", cleaned)
    if match:
        num = float(match.group(1))
        suffix = match.group(2)
        multiplier = {"K": 1_000, "M": 1_000_000, "B": 1_000_000_000}[suffix]
        return int(num * multiplier)

    # Case 2: Special pattern like 1M8 → 1.8M
    match = re.match(r"^(\d+)([KMB])(\d+)$", cleaned)
    if match:
        base = int(match.group(1))
        suffix = match.group(2)
        addon = int(match.group(3))
        base_multiplier = {"K": 1_000, "M": 1_000_000, "B": 1_000_000_000}[suffix]
        addon_multiplier = base_multiplier // 10  # e.g., 1M8 → 1,000,000 + 800,000
        return base * base_multiplier + addon * addon_multiplier

    # Case 3: Plain integer (already cleaned)
    try:
        return int(cleaned)
    except ValueError:
        raise ValueError(f"Cannot convert '{text}' to a number")

def verify_resource_amount_change( item, actualResource, expectResource):
    buffer=2
    if item == "gold":
        buffer=2000
    if abs(expectResource - actualResource) in range(buffer):
        print(f"expect {item} amount: {expectResource}, after {item} amount: {actualResource}")
        return True
    else:
        return False
