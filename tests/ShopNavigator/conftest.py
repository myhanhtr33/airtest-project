import pytest
from logger_config import get_logger
from Hierarchy.ShopNavigator import ShopNavigator

@pytest.fixture(scope="function")
def navigator(poco):
    return ShopNavigator(poco)

logger = get_logger("ShopNavigator")
@pytest.fixture(scope="session", autouse=True)
def setup_logger():
    logger.info("🔥 Logger initialized for pytest session.")