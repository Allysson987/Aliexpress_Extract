from app.infrastructure.browser.brownser_aliexpress import BrowserAliexpress
from app.infrastructure.parsers.aliexpress.home_page_parser import HomePageParser 
import time


class homePageExtract:

    def __init__(self):
        self.browser_aliexpress = BrowserAliexpress()
        self.browser_aliexpress.start_playwright()
        self.page = None
        self.home_page_parser=HomePageParser()

    def open_session(self):
        self.page = self.browser_aliexpress.start_browser()

    def validate_pop(self, html: str) -> bool:
        return "pop-content" in html

    def extract_page(self) -> str:
        return self.page.content()

    def close_pop(self):
        close_button = self.page.locator(".pop-close-btn")

        if close_button.is_visible():
            close_button.click()

    def close_session(self):
        try:
            self.browser_aliexpress.close_browser()
        finally:
            self.page = None

    def full_page_for_scroll(self) -> str:
        last_height = 0

        while True:
            current_height = self.page.evaluate(
                "document.documentElement.scrollHeight"
            )

            self.page.evaluate(
                f"window.scrollTo(0, {current_height})"
            )

            self.page.wait_for_timeout(2000)

            new_height = self.page.evaluate(
                "document.documentElement.scrollHeight"
            )

            if new_height == last_height:
                break

            last_height = new_height

        return self.page.content()

    def navigator_homePage(self):
        self.page.goto(
            "https://pt.aliexpress.com/",
            wait_until="load"
        )

        html_home_page = self.extract_page()

        if self.validate_pop(html_home_page):
            self.close_pop()

        html_full_page_home = self.full_page_for_scroll()
        offers=self.home_page_parser.offerts_day(html_full_page_home)
        return offers