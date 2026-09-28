from pages.tutorials_ninja.login_page import LoginPage
from utils.csv_reader import read_csv
from framework.logger import get_logger


logger = get_logger()


def test_login(driver, config):

    logger.info("Starting login test")

    data = read_csv(
        "data/login_data.csv"
    )[0]

    page = LoginPage(driver)

    page.open(
        config["app"]["url"]
    )

    page.open_login_page()

    logger.info("Entering login credentials")

    page.login(
        data["username"],
        data["password"]
    )

    logger.info("Checking login result")

    assert "account" in driver.current_url.lower()

    logger.info("Login test completed successfully")