from Hierarchy.PopupMilitary import *
from utils.device_setup import PocoManager
def main():
    poco = PocoManager.get_poco()
    popup = PopupMilitary(poco)
    level = popup.level_text
    print(f"before click: {popup.level_text}")
    poco("BtnUpdate").click()
    print(f"after click: {popup.level_text}")

if __name__ == "__main__":
    main()