import tests.test_Home
import utils.hierarchyDump
from tests import *
import os
from utils.device_setup import connect_to_unity

def run_all_tests():
    print("START tests...")
    tests.test_Home.run_all_home_tests()
    print("✅ DONE ALL!")

if __name__ == "__main__":
    print("helolheloo")
    run_all_tests()








