from app.infrastructure.parsers.aliexpress.home_page_parser import HomePageParser
from playwright.sync_api import Page


class homePageExtract:

    def __init__(self, page: Page):
        self.page = page
        self.home_page_parser = HomePageParser()
        self.html_full_page_home = ""

    def extract_page(self) -> str:
        return self.page.content()

    def validate_pop(self, html: str) -> bool:
        return "pop-content" in html

    def close_pop(self):
        close_button = self.page.locator(".pop-close-btn")

        if close_button.is_visible():
            close_button.click()

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

    def offers_day(self) -> dict | None:
        return self.home_page_parser.offerts_day(
            self.html_full_page_home
        )

    def all_offers_home(self) -> dict | None:
        return self.home_page_parser.all_products_home(
            self.html_full_page_home
        )

    def full(self) -> dict:
        return {
            "offers_day": self.offers_day(),
            "offers_all": self.all_offers_home()
        }

    def navigator_homePage(self):
        self.page.goto(
            "https://pt.aliexpress.com/",
            wait_until="load"
        )

        html_home_page = self.extract_page()

        if self.validate_pop(html_home_page):
            self.close_pop()

        self.html_full_page_home = self.full_page_for_scroll()