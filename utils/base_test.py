from utils.device_setup import PocoManager
from poco.drivers.unity3d import UnityPoco

class BaseTest:
    poco = None

    def __init__(self):
        self.poco = PocoManager.get_poco()
        self.pocoAndroid = PocoManager.get_pocoAndroid()
        self.setup()

    def setup(self):
        pass

    def teardown(self):
        pass
