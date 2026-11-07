from playwright.sync_api import (
    sync_playwright,
    Playwright,
    Browser,
    BrowserContext,
    Page
)

class BrowserAliexpress:

    def __init__(self):
        self.profile_user_data: str = "./browser"

        self.playwright: Playwright | None = None
        self.browser: Browser | None = None
        self.context: BrowserContext | None = None
        self.page: Page | None = None

    def start_playwright(self) -> None:
        self.playwright = sync_playwright().start()

    def start_browser_context_persistent(self) -> None:
        if self.playwright is None:
            raise RuntimeError("Playwright não foi iniciado.")

        self.context: BrowserContext = (
            self.playwright.chromium.launch_persistent_context(
                user_data_dir=self.profile_user_data,
                headless=False
            )
        )

        self.page: Page = self.context.pages[0] if self.context.pages else self.context.new_page()
        
