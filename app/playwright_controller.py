# === FILE: app/playwright_controller.py ===
from playwright.sync_api import sync_playwright


class PlaywrightController:
    def __init__(self, profile_path, proxy=None, headless=False):
        self.profile_path = profile_path
        self.proxy = proxy
        self.headless = headless
        self._pw = None
        self.context = None
        self.page = None

    def start(self):
        self._pw = sync_playwright().start()
        launch_opts = {"user_data_dir": self.profile_path, "headless": self.headless, "args": ["--no-sandbox"]}
        if self.proxy:
            launch_opts['proxy'] = {"server": self.proxy}
        self.context = self._pw.chromium.launch_persistent_context(**launch_opts)
        self.page = self.context.new_page()
        return self.page

    def close(self):
        try:
            if self.context:
                self.context.close()
        finally:
            if self._pw:
                self._pw.stop()

    def goto(self, url):
        if not self.page:
            raise RuntimeError('Context not started')
        self.page.goto(url, wait_until='networkidle')