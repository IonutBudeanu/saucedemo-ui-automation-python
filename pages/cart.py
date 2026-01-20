from __future__ import annotations

import re

from playwright.sync_api import Page, expect


class CartPage:
    def __init__(self, page: Page) -> None:
        self.page = page
        self._items = page.locator(".cart_item")
        self._remove_buttons = page.locator("button[data-test^='remove']")
        self._checkout_button = page.locator("[data-test='checkout']")
        self._continue_shopping = page.locator("[data-test='continue-shopping']")

    def wait_for_ready(self) -> None:
        expect(self.page).to_have_url(re.compile(r".*/cart\.html.*"))

    def item_count(self) -> int:
        return self._items.count()

    def assert_item_count(self, expected: int) -> None:
        expect(self._items).to_have_count(expected)

    def remove_all_items(self) -> None:
        while self._remove_buttons.count() > 0:
            self._remove_buttons.first.click()

    def checkout(self) -> None:
        self._checkout_button.click()

    def continue_shopping(self) -> None:
        self._continue_shopping.click()
