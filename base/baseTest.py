from utils.device_setup import PocoManager, connect_to_unity
class BaseTest:
    def __init__(self):
        self.poco= PocoManager.get_poco()
