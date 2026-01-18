import pytest

from pages import LoginPage
from pages import InventoryPage


@pytest.mark.regression
def test_menu_open_close(standard_inventory: InventoryPage):
    standard_inventory.open_menu()
    standard_inventory.close_menu()


@pytest.mark.regression
def test_menu_items_exist(standard_inventory: InventoryPage):
    for item in ["All Items", "About", "Logout", "Reset App State"]:
        standard_inventory.assert_menu_item_exists(item)


@pytest.mark.regression
@pytest.mark.compatibility
def test_about_navigates_away(standard_inventory: InventoryPage):
    standard_inventory.click_menu_item("About")
    assert "saucelabs" in standard_inventory.page.url.lower()


@pytest.mark.regression
def test_reset_app_state_clears_cart(standard_inventory: InventoryPage):
    standard_inventory.add_all_items()
    assert standard_inventory.cart_count() == 6
    standard_inventory.click_menu_item("Reset App State")
    # Reset navigates? Either way, ensure badge clears.
    assert standard_inventory.cart_count() == 0


@pytest.mark.smoke
@pytest.mark.regression
def test_logout_returns_to_login(page, base_url, users_data):
    lp = LoginPage(page, base_url)
    lp.open()
    lp.login("standard_user", users_data["password"])
    inv = InventoryPage(page)
    inv.is_at()
    inv.click_menu_item("Logout")
    # Back on login
    assert "login" in page.url.lower() or page.locator("#login-button").is_visible()
