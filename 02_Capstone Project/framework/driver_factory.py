from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def create_driver(config):

    options = Options()

    if config["browser"]["headless"]:
        options.add_argument("--headless")

    options.add_argument("--start-maximized")

    driver = webdriver.Chrome(options=options)

    driver.implicitly_wait(
        config["browser"]["implicit_wait"]
    )

    driver.set_page_load_timeout(
        config["browser"]["page_load_timeout"]
    )

    return driver