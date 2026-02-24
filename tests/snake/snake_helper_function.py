def get_color_name(color_int: int) -> str:
    color_map = {
        -1: "None",
        0: "Red",
        1: "Orange",
        2: "Yellow",
        3: "Lime",
        4: "Green",
        5: "Sky",
        6: "Blue",
        7: "Violet",
        8: "Purple",
        9: "Copper",
        10: "Snow",
        11: "Onyx",
        12: "Red_Sub",
        13: "Orange_Sub",
        14: "Yellow_Sub",
        15: "Lime_Sub",
        16: "Green_Sub",
        17: "Sky_Sub",
        18: "Blue_Sub",
        19: "Violet_Sub",
        20: "Purple_Sub",
        21: "Copper_Sub",
        22: "Snow_Sub",
        23: "Onyx_Sub"
    }
    return color_map.get(color_int, f"Unknown({color_int})")

