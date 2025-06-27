from airtest.core.api import Template
from utils.image_utils import get_resource_path  # adjust path as needed

engine_pack_panel = Template(get_resource_path("engine_pack_panel.png"), record_pos=(-0.083, 0.299), resolution=(900, 1800))
royal_pack_panel = Template(get_resource_path("royal_pack_panel.png"), record_pos=(-0.083, 0.106), resolution=(900, 1800))
boss_pack_panel = Template(get_resource_path("boss_slayer_panel.png"), record_pos=(-0.074, -0.112), resolution=(900, 1800))
unlock_pack_panel = Template(get_resource_path("unlock_pack_panel.png"), record_pos=(-0.016, -0.696), resolution=(900, 1800))
daiy_pack_panel = Template(get_resource_path("daily_pack_panel.png"), record_pos=(-0.077, 0.46), resolution=(900, 1800))