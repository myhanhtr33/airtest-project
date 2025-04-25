from airtest.core.api import Template
from utils.image_utils import get_resource_path  # adjust path as needed

goldNavigatePanel = Template(get_resource_path("goldPanelTitle.png"), record_pos=(-0.002, -0.38), resolution=(900, 1800))
energyNavigatePanel = Template(get_resource_path("energyPanelTitle.png"), record_pos=(-0.001, -0.381), resolution=(900, 1800))
gemNavigatePanel = Template(get_resource_path("gemPanelTitle.png"), record_pos=(-0.001, -0.378), resolution=(900, 1800))