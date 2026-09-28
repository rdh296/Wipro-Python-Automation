from selenium.webdriver.common.by import By

from pages.tutorials_ninja.login_page import LoginPage


class BrokenLoginPage(LoginPage):

    # Intentionally broken locator
    USERNAME = (
        By.ID,
        "this-id-does-not-exist"
    )

    # AdaptiveQA knows how to recover
    LOCATOR_ALTERNATIVES = {

        USERNAME: [

            (
                By.ID,
                "input-email"
            )
        ]
    }


def test_self_healing(driver, config):

    page = BrokenLoginPage(driver)

    page.open(
        config["app"]["url"]
    )

    page.open_login_page()

    # The primary locator is deliberately broken.
    # AdaptiveQA should recover using input-email.

    page.type(
        page.USERNAME,
        "ritishadhar2005@gmail.com"
    )

    assert page.healer.healed is True