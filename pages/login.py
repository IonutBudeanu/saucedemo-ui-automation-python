from __future__ import annotations

from playwright.sync_api import Page, expect

from .base import BasePage


class LoginPage(BasePage):
    USERNAME = "#user-name"
    PASSWORD = "#password"
    LOGIN_BTN = "#login-button"
    ERROR = "h3[data-test='error']"

    def __init__(self, page: Page, base_url: str):
        super().__init__(page)
        self.base_url = base_url

    def open(self) -> None:
        self.page.goto(self.base_url)
        expect(self.page.locator(self.LOGIN_BTN)).to_be_visible()

    def login(self, username: str, password: str) -> None:
        self.page.fill(self.USERNAME, username)
        self.page.fill(self.PASSWORD, password)
        self.page.click(self.LOGIN_BTN)

    def error_text(self) -> str:
        return self.page.locator(self.ERROR).inner_text()
