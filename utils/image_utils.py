from airtest.core.api import Template
import os

def get_resource_path(filename):
    return os.path.join(os.path.dirname(__file__), "..", "image", filename)