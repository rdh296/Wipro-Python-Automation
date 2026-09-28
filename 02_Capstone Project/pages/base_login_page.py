from pages.base_page import BasePage


class BaseLoginPage(BasePage):

    def login(self, username, password):

        self.type(
            self.USERNAME,
            username
        )

        self.type(
            self.PASSWORD,
            password
        )

        self.click(
            self.LOGIN_BUTTON
        )