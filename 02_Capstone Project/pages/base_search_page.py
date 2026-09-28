from pages.base_page import BasePage


class BaseSearchPage(BasePage):

    def search(self, keyword):

        self.type(
            self.SEARCH_BOX,
            keyword
        )

        self.click(
            self.SEARCH_BUTTON
        )