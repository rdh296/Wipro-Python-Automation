from selenium.webdriver.common.by import By

from pages.base_login_page import BaseLoginPage
from framework.logger import get_logger


logger = get_logger()


class LoginPage(BaseLoginPage):

    MY_ACCOUNT = (
        By.XPATH,
        "//span[text()='My Account']"
    )

    LOGIN_LINK = (
        By.LINK_TEXT,
        "Login"
    )

    USERNAME = (
        By.ID,
        "input-email"
    )

    PASSWORD = (
        By.ID,
        "input-password"
    )

    LOGIN_BUTTON = (
        By.CSS_SELECTOR,
        "input[type='submit']"
    )

    # ==========================================
    # AdaptiveQA fallback locators
    # ==========================================

    LOCATOR_ALTERNATIVES = {

        USERNAME: [

            (
                By.NAME,
                "email"
            ),

            (
                By.CSS_SELECTOR,
                "input[type='email']"
            ),

            (
                By.XPATH,
                "//input[contains(@placeholder, 'E-Mail')]"
            )
        ],

        PASSWORD: [

            (
                By.NAME,
                "password"
            ),

            (
                By.CSS_SELECTOR,
                "input[type='password']"
            )
        ],

        LOGIN_BUTTON: [

            (
                By.CSS_SELECTOR,
                "input.btn-primary"
            ),

            (
                By.XPATH,
                "//input[@value='Login']"
            )
        ]
    }

    def open(self, url):

        logger.info(
            "Opening TutorialsNinja: %s",
            url
        )

        self.driver.get(url)

    def open_login_page(self):

        logger.info(
            "Opening My Account menu"
        )

        self.click(
            self.MY_ACCOUNT
        )

        logger.info(
            "Opening Login page"
        )

        self.click(
            self.LOGIN_LINK
        )