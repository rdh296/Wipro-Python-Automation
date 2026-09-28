from selenium.webdriver.common.by import By

from pages.base_search_page import BaseSearchPage
from framework.logger import get_logger


logger = get_logger()


class SearchPage(BaseSearchPage):

    SEARCH_BOX = (
        By.NAME,
        "search"
    )

    SEARCH_BUTTON = (
        By.CSS_SELECTOR,
        "button.btn.btn-default"
    )

    # ==========================================
    # AdaptiveQA fallback locators
    # ==========================================

    LOCATOR_ALTERNATIVES = {

        SEARCH_BOX: [

            (
                By.CSS_SELECTOR,
                "input[name='search']"
            ),

            (
                By.XPATH,
                "//input[contains(@placeholder, 'Search')]"
            )
        ],

        SEARCH_BUTTON: [

            (
                By.CSS_SELECTOR,
                "button[type='button']"
            ),

            (
                By.XPATH,
                "//button[contains(@class, 'btn-default')]"
            )
        ]
    }

    def open(self, url):

        logger.info(
            "Opening TutorialsNinja: %s",
            url
        )

        self.driver.get(url)

    def product_exists(self, product_name):

        logger.info(
            "Checking product: %s",
            product_name
        )

        return (
            product_name.lower()
            in self.driver.page_source.lower()
        )