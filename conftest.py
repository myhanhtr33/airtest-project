import datetime
import os, pytest
from airtest.core.api import snapshot
from poco.exceptions import PocoNoSuchNodeException
import pytest
import pytest_html
# from logging_config import setup_logger
import builtins

# Initialize logger before any tests run
# log_file_path = setup_logger()
# ensure the reports/screenshots folder exists
os.makedirs("reports/screenshots", exist_ok=True)

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    After each test call, if it failed, take a screenshot and
    attach it to the HTML report.
    """
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call":
        screenshot_filename = f"{datetime.datetime.now().strftime('%Y-%m-%d_%Hh%M')}_{item.name}.png"
        screenshot_path = os.path.join("reports", "screenshots", screenshot_filename)
        if rep.failed:
            try:
                snapshot(screenshot_path) #= full path for saving the screenshot
                # attach to report
                extra = getattr(rep, "extra", [])
                # use relative path when attach it to HTML report (screenshots/filename)
                extra.append(pytest_html.extras.image(os.path.join("screenshots", screenshot_filename)))
                rep.extra = extra
            except PocoNoSuchNodeException:
                # if Poco isn’t ready, just skip screenshot
                pass

        # Capture printed output
        captured = call.excinfo and call.excinfo.value and getattr(call.excinfo.value, 'stdout', None)
        if captured:
            extra = getattr(rep, "extra", [])
            extra.append(pytest_html.extras.text(captured))
            rep.extra = extra



# @pytest.hookimpl(tryfirst=True, hookwrapper=True)
# def pytest_runtest_call(item):
#     test_file = item.module.__name__
#     test_case = item.name
#     suite_name = item.parent.name
#     layer = "low_level"
#
#     logger, _ = setup_logger(context={
#         "test_file": test_file,
#         "test_case": test_case,
#         "layer": layer,
#         "suite": suite_name
#     })
#
#     builtins.logger = logger
#     yield