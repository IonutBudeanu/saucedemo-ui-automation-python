from __future__ import annotations

from playwright.sync_api import expect

from .base import BasePage


class CheckoutStepOnePage(BasePage):
    TITLE = "span.title"
    FIRST = "#first-name"
    LAST = "#last-name"
    ZIP = "#postal-code"
    CONTINUE = "#continue"
    ERROR = "h3[data-test='error']"

    def is_at(self) -> None:
        expect(self.page.locator(self.TITLE)).to_contain_text("Checkout: Your Information")

    def fill(self, first: str, last: str, zip_code: str) -> None:
        self.page.fill(self.FIRST, first)
        self.page.fill(self.LAST, last)
        self.page.fill(self.ZIP, zip_code)

    def continue_checkout(self) -> None:
        self.page.click(self.CONTINUE)

    def error_text(self) -> str:
        return self.page.locator(self.ERROR).inner_text()


class CheckoutOverviewPage(BasePage):
    TITLE = "span.title"
    FINISH = "#finish"

    def is_at(self) -> None:
        expect(self.page.locator(self.TITLE)).to_contain_text("Checkout: Overview")

    def finish(self) -> None:
        self.page.click(self.FINISH)


class CheckoutCompletePage(BasePage):
    TITLE = "span.title"
    COMPLETE_HEADER = "h2.complete-header"

    def is_at(self) -> None:
        expect(self.page.locator(self.TITLE)).to_contain_text("Checkout: Complete!")

    def confirmation_message(self) -> str:
        return self.page.locator(self.COMPLETE_HEADER).inner_text()
