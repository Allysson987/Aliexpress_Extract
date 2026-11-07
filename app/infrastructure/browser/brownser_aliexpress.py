from pathlib import Path
from playwright.sync_api import (
    sync_playwright,
    Playwright,
    Browser,
    BrowserContext,
    Page
)


class BrowserAliexpress:

    def __init__(self):
        self.storage_file = "aliexpress.json"

        self.playwright: Playwright | None = None
        self.browser: Browser | None = None
        self.context: BrowserContext | None = None
        self.page: Page | None = None

    def start_playwright(self) -> None:
        self.playwright = sync_playwright().start()

    def start_browser(self) -> Page:
        if self.playwright is None:
            raise RuntimeError("Playwright não foi iniciado.")

        self.browser = self.playwright.chromium.launch(
            headless=False
        )

        if Path(self.storage_file).exists():
            self.context = self.browser.new_context(
                storage_state=self.storage_file
            )
        else:
            self.context = self.browser.new_context()

        self.page = self.context.new_page()
        return self.page

    def save_session(self) -> None:
        if self.context:
            self.context.storage_state(
                path=self.storage_file
            )

    def close_browser(self) -> None:
        if self.context:
            self.context.close()

        if self.browser:
            self.browser.close()

        if self.playwright:
            self.playwright.stop()