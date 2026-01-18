from __future__ import annotations

from playwright.sync_api import expect

from .base import BasePage


class CartPage(BasePage):
    TITLE = "span.title"
    CART_ITEM = ".cart_item"
    REMOVE_BTN = "button.cart_button"
    CHECKOUT_BTN = "#checkout"

    def is_at(self) -> None:
        expect(self.page.locator(self.TITLE)).to_contain_text("Your Cart")

    def item_count(self) -> int:
        return self.page.locator(self.CART_ITEM).count()

    def remove_all(self) -> None:
        btns = self.page.locator(self.REMOVE_BTN)
        for i in range(btns.count()):
            btns.nth(i).click()

    def start_checkout(self) -> None:
        self.page.click(self.CHECKOUT_BTN)
