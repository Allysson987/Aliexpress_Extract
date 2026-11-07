from app.application.use_cases.aliexpress.home_page import homePageExtract


class AliExpressController:

    def __init__(self, home_page: homePageExtract):
        self.home_page = home_page

    def execute_service(self, handler):
        self.home_page.open_session()

        try:
            return handler()
        finally:
            self.home_page.close_session()