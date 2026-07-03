from playwright.sync_api import Page


class BasePage:
    def __init__(self, page: Page, url: str) -> None:
        self.page = page
        self.url = url

    def get_url(self) -> str:
        return self.page.url

    def open(self) -> None:
        self.page.goto(self.url)

    def click(self, selector: str) -> None:
        self.page.click(selector)

    def send_keys(self, keys: str, selector: str) -> None:
        self.page.locator(selector).fill(keys)

    def get_text(self, selector: str) -> str:
        return self.page.locator(selector).first.inner_text()

    def submit(self, selector: str) -> None:
        self.page.locator(selector).press("Enter")
