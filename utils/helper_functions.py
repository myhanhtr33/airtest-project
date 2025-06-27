import time
from poco.exceptions import PocoNoSuchNodeException
from utils.get_resource_amount import *

def wait_for_element(poco_obj, timeout=3, interval=0.5, condition="appear"):
    """
    Wait for a Poco object to appear or disappear.
    :param poco_obj: Poco element to check (must be a live query, not stale).
    :param timeout: How long to wait in seconds.
    :param interval: How frequently to check.
    :param condition: 'appear' or 'disappear'.
    :return: True if condition met within timeout, False otherwise.
    """
    elapsed = 0
    while elapsed < timeout:
        exists = poco_obj.exists()
        if (condition == "appear" and exists) or (condition == "disappear" and not exists):
            return True
        time.sleep(interval)
        elapsed += interval
    return False

def maybe_handle_vip_congrats(poco, timeout=5.0, poll_interval=0.5):
    """
    If the VIP “Congratulations” popup ever appears, close it. Otherwise do nothing.

    :param timeout: total seconds to wait for the popup to appear
    :param poll_interval: how often (seconds) to poll
    """
    popup = poco("PopupVipCongratulation(Clone)")
    elapsed = 0.0

    # 1) Poll until either the popup appears or we exceed the timeout
    while elapsed < timeout:
        try:
            if popup.exists():
                print(f"[Info] VIP‐Congrats popup detected after {elapsed:.1f}s.")
                # 2) Once it’s detected, click its “Close” button:
                close_btn = popup.offspring("btnTaptoclose")
                if close_btn.exists():
                    close_btn.click()
                    # 3) Wait for it to actually disappear before returning
                    end_time = 0.0
                    while end_time < timeout:
                        if not popup.exists():
                            print("[Info] VIP‐Congrats popup closed successfully.")
                            return
                        time.sleep(poll_interval)
                        end_time += poll_interval
                    # If we get here, the popup never vanished, but we’ll bail anyway
                    print("[Warning] VIP‐Congrats popup did not disappear after clicking Close.")
                    return
                else:
                    # If close button is unexpectedly missing, bail out
                    print("[Warning] VIP‐Congrats popup had no BtnClose child!")
                    return
            # If popup isn’t present yet, wait and retry
        except PocoNoSuchNodeException:
            # Means “PopupVipCongrats(Clone)” itself hasn’t been added/dumped yet
            pass

        time.sleep(poll_interval)
        elapsed += poll_interval

    # If we reach here, the popup never appeared in the given timeout
    print(f"[Info] No VIP‐Congrats popup appeared in {timeout}s.")

def check_noti(poco, expected_text):
    noti= poco("PanelNotification").offspring("lNotification")
    assert wait_for_element(noti, condition="appear"), "Notification not found!"
    print("✅ Notification appeared.")
    actual_text = noti.get_text().strip()
    assert actual_text == expected_text, f"Unexpected notification text: '{expected_text}'"
    # 3. Wait for disappearance
    assert wait_for_element(noti, condition="disappear"), "Notification did not disappear!"
    print("✅ Notification disappeared.")

def check_popup_claim_known_resourcce(poco,expected_amount,expected_sprite,logger):
    """
        Validates the appearance and content of a reward popup, ensuring the displayed
        reward matches the expected sprite and amount, and then claims the reward.
        """
    if "pilot" in expected_sprite.lower():
        popupPilot=poco("PopupReceivePilot(Clone)")
        wait_for_element(popupPilot, condition="appear", timeout=5)
        popupPilot.offspring("B_Skip").click()
        return
    popupClaim = poco("PopupRewardItem(Clone)")
    wait_for_element(popupClaim, condition="appear", timeout=5)
    #enigne dont have lQuantity
    actual_amount=clean_number(popupClaim.offspring("lQuantity").get_text()) if popupClaim.offspring("lQuantity").exists() else 1

    if popupClaim.exists():
        actual_reward = {
            "sprite": popupClaim.offspring("sIcon").attr("texture"),
            "amount": actual_amount
        }
    else:
        raise RuntimeError(f"Reward popup did not appear after 5 seconds.")
    assert actual_reward["sprite"] == expected_sprite, f"reward sprite mismatch: expected {expected_sprite}, got {actual_reward['sprite']}"
    logger.info(f"actual reward sprite {actual_reward["sprite"]} meet expected {expected_sprite}")
    assert actual_reward["amount"] == expected_amount, f"reward amount mismatch: expected {expected_amount}, got {actual_reward['amount']}"
    logger.info(f"actual reward amount {actual_reward['amount']} meet expected {expected_amount}")
    btnClaim = popupClaim.offspring("bClaim")
    btnClaim.click()