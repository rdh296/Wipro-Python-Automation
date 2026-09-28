from selenium.webdriver.support.ui import WebDriverWait

from framework.locator_healer import LocatorHealer


class BasePage:

    def __init__(self, driver):

        self.driver = driver

        self.wait = WebDriverWait(
            driver,
            10
        )

        self.healer = LocatorHealer(
            driver,
            self.wait
        )

        # Register AdaptiveQA healer
        self.driver._adaptiveqa_healer = (
            self.healer
        )

    def _find(self, locator):

        alternatives = getattr(
            self,
            "LOCATOR_ALTERNATIVES",
            {}
        ).get(
            locator,
            []
        )

        return self.healer.find(
            locator,
            alternatives
        )

    def click(self, locator):

        element = self._find(locator)

        element.click()

    def type(self, locator, text):

        element = self._find(locator)

        element.clear()

        element.send_keys(text)

    def get_text(self, locator):

        return self._find(locator).text

    def is_visible(self, locator):

        return self._find(locator).is_displayed()