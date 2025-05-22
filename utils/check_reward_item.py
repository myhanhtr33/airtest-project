from utils.get_resource_amount import *
from utils.sprite_mapping import *

def check_sprite_known_resource(name, sprite_name):

    print("========"+sprite_name)
    print("========"+get_sprite_name(name))
    if sprite_name== get_sprite_name(name):
        print(f"Item '{name}' has a sprite equivalent: '{sprite_name}'")

    else:
        raise ValueError(f"No sprite equivalent found for item: '{name}'")
