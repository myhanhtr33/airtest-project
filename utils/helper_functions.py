import time

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