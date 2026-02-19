from airtest.core.error import TargetNotFoundError
from cozy.ingame_popup import *
from utils.helper_functions import wait_for_element

def is_wait_for_parent_place(objName,parentMapping,placedObjs):
    # Determine whether the parent of the given object has been placed.Object can be placed only if its parent has been placed.
    parentID=None
    for obj in parentMapping:
        for child in obj['Children']:
            if child['ID']==objName:
                parentID= obj['ID']
                break
        if parentID is not None:
            break
    if parentID is None:
        return False
    return parentID not in placedObjs

def get_spawnable_items(poco):
    result = poco.invoke("get_level_data")
    level_data_phases = result['level_data']['phases']
    level_data = level_data_phases[0]['groups']
    spawn_exceptions = result['spawn_exceptions']
    spawnable_items = [
        item
        for group in level_data
        for item in group['items']
        if item not in spawn_exceptions
    ]
    return spawnable_items

def verify_popup_win(poco):
    fpoco = poco.freeze()
    popup_win = PopupWin(poco)
    if not wait_for_element(popup_win.root, timeout=5):
        raise TargetNotFoundError("PopupWin not found")
    popup_win= PopupWin(fpoco)
    assert popup_win.btn_ads.exists(), "Button B_Ads not found in PopupWin"
    assert popup_win.btn_next.exists(), "Button Next not found in PopupWin"
    gold_next=int(popup_win.gold_next)
    gold_ads=int(popup_win.gold_ads)
    multiplier=int(popup_win.gold_multiplier.replace("x",""))
    assert gold_ads== gold_next * multiplier, f"Gold amount mismatch: gold_ads({gold_ads}) != gold_next({gold_next}) * multiplier({multiplier})"
    popup_win.btn_next.click(sleep_interval=1)
    print("PopupWin verified and Next button clicked successfully.")

