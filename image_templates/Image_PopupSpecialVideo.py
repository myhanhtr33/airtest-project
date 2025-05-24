from airtest.core.api import Template
from utils.image_utils import get_resource_path  # adjust path as needed

offer_wall = Template(get_resource_path("offerWallTop.png"), record_pos=(0.001, -0.923), resolution=(900, 1800))
top_element_PopupSpecialVideo= Template(get_resource_path("top_element_PopupSpecialVideo.png"), record_pos=(-0.002, -0.55), resolution=(900, 1800))