RESOURCE_SPRITE_MAPPING = {
    "gold": "icon_coin",
    "energy": "icon_daily_quest_enegy",
    "gem": "icon_daily_quest_gem",

    # #list card
    # "ITEM_CARD_PLANE_GENERAL" : "card_A0",
    # "ITEM_CARD_PLANE_1" : "card_A1",
    # "ITEM_CARD_PLANE_2" : "card_A2",
    # "ITEM_CARD_PLANE_3" : "card_A3",
    # "ITEM_CARD_PLANE_6" : "card_A6",
    # "ITEM_CARD_PLANE_7": "card_A7",
    # "ITEM_CARD_PLANE_8": "card_A8",
    # "ITEM_CARD_PLANE_9": "card_A9",
    # "ITEM_CARD_PLANE_10": "card_A10",
    # "ITEM_CARD_PLANE_11": "card_A11",
    # "ITEM_CARD_PLANE_12": "card_A12",
    # "ITEM_CARD_PLANE_13": "card_A13",
    # "ITEM_CARD_PLANE_14": "card_A14",
    # "ITEM_CARD_PLANE_15": "card_A15",
    # "ITEM_CARD_PLANE_16": "card_A16",
    # "ITEM_CARD_PLANE_21": "card_A21",
    # "ITEM_CARD_PLANE_22": "card_A22",
    # "ITEM_CARD_PLANE_24": "card_A24",
    # "ITEM_CARD_PLANE_25": "card_A25",
    #
    # "ITEM_CARD_WINGMAN_GENERAL": "card_D0",
    # "ITEM_CARD_WINGMAN_1": "card_D1",
    # "ITEM_CARD_WINGMAN_2": "card_D2",
    # "ITEM_CARD_WINGMAN_3": "card_D3",
    # "ITEM_CARD_WINGMAN_4": "card_D4",
    # "ITEM_CARD_WINGMAN_5": "card_D5",
    # "ITEM_CARD_WINGMAN_6": "card_D6",
    # "ITEM_CARD_WINGMAN_7": "card_D7",
    # "ITEM_CARD_WINGMAN_8": "card_D8",
    # "ITEM_CARD_WINGMAN_9": "card_D9",
    # "ITEM_CARD_WINGMAN_10": "card_D10",
    # "ITEM_CARD_WINGMAN_11": "card_D11",
    # "ITEM_CARD_WINGMAN_12": "card_D12",
    # "ITEM_CARD_WINGMAN_19": "card_D19",
    # "ITEM_CARD_WINGMAN_20": "card_D20",
    # "ITEM_CARD_WINGMAN_22": "card_D22",
    # "ITEM_CARD_WINGMAN_23": "card_D23",
    #
    # "ITEM_CARD_WING_GENERAL": "card_W0",
    # "ITEM_CARD_WING_1": "card_W1",
    # "ITEM_CARD_WING_2": "card_W2",
    # "ITEM_CARD_WING_3": "card_W3",
    # "ITEM_CARD_WING_4": "card_W4",
    # "ITEM_CARD_WING_5": "card_W5",
    # "ITEM_CARD_WING_6": "card_W6",
    # "ITEM_CARD_WING_7": "card_W7",
    # "ITEM_CARD_WING_8": "card_W8",
    # "ITEM_CARD_WING_9": "card_W9",
    # "ITEM_CARD_WING_10": "card_W10",
    # "ITEM_CARD_WING_11": "card_W11",
    # "ITEM_CARD_WING_12": "card_W12",
    # "ITEM_CARD_WING_19": "card_W19",
    # "ITEM_CARD_WING_20": "card_W20",
    # "ITEM_CARD_WING_22": "card_W22",
    # "ITEM_CARD_WING_23": "card_W23",
}

def get_sprite_name(item_name):
    """
    Get the sprite name equivalent for a given item name.

    :param item_name: The name of the item.
    :return: The sprite name if it exists, otherwise None.
    """
    print("!!!!!!!!!!!!!"+RESOURCE_SPRITE_MAPPING.get(item_name))
    return RESOURCE_SPRITE_MAPPING.get(item_name)

def check_sprite_known_resource(name, sprite_name):

    print("========"+sprite_name)
    print("========"+get_sprite_name(name))
    if sprite_name== get_sprite_name(name):
        print(f"Item '{name}' has a sprite equivalent: '{sprite_name}'")

    else:
        raise ValueError(f"No sprite equivalent found for item: '{name}'")
