import pytest

from pages import LoginPage, InventoryPage


@pytest.mark.compatibility
@pytest.mark.smoke
def test_compat_login(page, base_url, users_data):
    lp = LoginPage(page, base_url)
    lp.open()
    lp.login("standard_user", users_data["password"])
    InventoryPage(page).is_at()


@pytest.mark.compatibility
def test_compat_sorting(page, base_url, users_data):
    lp = LoginPage(page, base_url)
    lp.open()
    lp.login("standard_user", users_data["password"])
    inv = InventoryPage(page)
    inv.is_at()
    inv.select_sort("Price (low to high)")
    inv.assert_sorted_price_asc()
