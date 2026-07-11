from src.web.constants.locators import MainPageLocators
from src.web.core.base_page import BasePage


class MainPage(BasePage):

    def get_header_text(self):
        self.page.locator(MainPageLocators.HEADER).wait_for(state="visible")
        return self.page.locator(MainPageLocators.HEADER).inner_text()
