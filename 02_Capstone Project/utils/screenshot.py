import os


def take_screenshot(driver, test_name):

    os.makedirs("screenshots", exist_ok=True)

    file_path = f"screenshots/{test_name}.png"

    driver.save_screenshot(file_path)

    return file_path