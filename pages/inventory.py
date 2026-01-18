from __future__ import annotations

from dataclasses import dataclass

from playwright.sync_api import expect

from .base import BasePage


@dataclass(frozen=True)
class SortOption:
    name: str
    assert_mode: str


class InventoryPage(BasePage):
    TITLE = "span.title"
    ITEM = ".inventory_item"
    ITEM_NAME = ".inventory_item_name"
    ITEM_PRICE = ".inventory_item_price"
    CART_LINK = "a.shopping_cart_link"
    CART_BADGE = "span.shopping_cart_badge"
    BTN_INVENTORY = "button.btn_inventory"
    SORT_SELECT = "select[data-test='product-sort-container']"
    ACTIVE_SORT = "[data-test='active-option']"

    # Menu
    MENU_BTN = "#react-burger-menu-btn"
    MENU_CLOSE = "#react-burger-cross-btn"
    MENU_PANEL = ".bm-menu-wrap"
    MENU_ALL_ITEMS = "#inventory_sidebar_link"
    MENU_ABOUT = "#about_sidebar_link"
    MENU_LOGOUT = "#logout_sidebar_link"
    MENU_RESET = "#reset_sidebar_link"

    def is_at(self) -> None:
        expect(self.page.locator(self.TITLE)).to_contain_text("Products")

    def inventory_count(self) -> int:
        return self.page.locator(self.ITEM).count()

    def cart_count(self) -> int:
        badge = self.page.locator(self.CART_BADGE)
        if badge.count() == 0:
            return 0
        txt = badge.first.inner_text().strip()
        return int(txt) if txt else 0

    def open_cart(self) -> None:
        self.page.click(self.CART_LINK)

    def add_all_items(self) -> None:
        expect(self.page.locator(self.ITEM).first).to_be_visible()
        buttons = self.page.locator(self.BTN_INVENTORY)
        for i in range(buttons.count()):
            btn = buttons.nth(i)
            label = btn.inner_text().strip().lower()
            if "add to cart" in label:
                btn.click()

    def remove_all_items(self) -> None:
        buttons = self.page.locator(self.BTN_INVENTORY)
        for i in range(buttons.count()):
            btn = buttons.nth(i)
            label = btn.inner_text().strip().lower()
            if "remove" in label:
                btn.click()

    def item_names(self) -> list[str]:
        expect(self.page.locator(self.ITEM).first).to_be_visible()
        loc = self.page.locator(self.ITEM_NAME)
        return [loc.nth(i).inner_text().strip() for i in range(loc.count())]

    def item_prices(self) -> list[float]:
        loc = self.page.locator(self.ITEM_PRICE)
        return [float(loc.nth(i).inner_text().replace("$", "").strip()) for i in range(loc.count())]

    def select_sort(self, visible_text: str) -> None:
        self.page.select_option(self.SORT_SELECT, label=visible_text)
        # Wait for UI to reflect selected option (prevents race conditions)
        expect(self.page.locator(self.ACTIVE_SORT)).to_have_text(visible_text)

    def assert_sorted_name_asc(self) -> None:
        names = self.item_names()
        assert names == sorted(names, key=str.casefold)

    def assert_sorted_name_desc(self) -> None:
        names = self.item_names()
        assert names == sorted(names, key=str.casefold, reverse=True)

    def assert_sorted_price_asc(self) -> None:
        prices = self.item_prices()
        assert prices == sorted(prices)

    def assert_sorted_price_desc(self) -> None:
        prices = self.item_prices()
        assert prices == sorted(prices, reverse=True)

    # Menu
    def open_menu(self) -> None:
        self.page.click(self.MENU_BTN)
        expect(self.page.locator(self.MENU_PANEL)).to_be_visible()

    def close_menu(self) -> None:
        self.page.click(self.MENU_CLOSE)
        expect(self.page.locator(self.MENU_PANEL)).to_be_hidden()

    def assert_menu_item_exists(self, item: str) -> None:
        self.open_menu()
        mapping = {
            "all items": self.MENU_ALL_ITEMS,
            "about": self.MENU_ABOUT,
            "logout": self.MENU_LOGOUT,
            "reset app state": self.MENU_RESET,
        }
        locator = mapping.get(item.strip().lower())
        assert locator, f"Unknown menu item: {item}"
        expect(self.page.locator(locator)).to_be_visible()
        self.close_menu()

    def click_menu_item(self, item: str) -> None:
        self.open_menu()
        mapping = {
            "all items": self.MENU_ALL_ITEMS,
            "about": self.MENU_ABOUT,
            "logout": self.MENU_LOGOUT,
            "reset app state": self.MENU_RESET,
        }
        locator = mapping.get(item.strip().lower())
        assert locator, f"Unknown menu item: {item}"
        self.page.click(locator)
