from app.application.use_cases.aliexpress.pages.home_page import homePageExtract
from app.infrastructure.browser.brownser_aliexpress import BrowserAliexpress

class AliExpressController:

    def __init__(self):
        self.browser_aliexpress = BrowserAliexpress()
        self.page = None

    def open_session(self):
        self.browser_aliexpress.start_playwright()
        self.page = self.browser_aliexpress.start_browser()

    def close_session(self):
        try:
            self.browser_aliexpress.close_browser()
        finally:
            self.page = None

    def execute_service(self, handler: str):

        self.open_session()

        try:
            use_case = homePageExtract(page=self.page)

            use_case.navigator_homePage()

            method = getattr(use_case, handler)

            return method()

        finally:
            self.close_session()