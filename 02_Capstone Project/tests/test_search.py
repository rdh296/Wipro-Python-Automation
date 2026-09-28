from pages.tutorials_ninja.search_page import SearchPage
from framework.logger import get_logger
import time

logger = get_logger()


def test_product_search(driver, config):

    logger.info("Starting product search test")

    page = SearchPage(driver)

    page.open(
        config["app"]["url"]
    )

    page.search("MacBook")

    logger.info("Checking search result")

    assert page.product_exists("MacBook")

    logger.info(
        "Product search test completed successfully"
    )

    time.sleep(5)