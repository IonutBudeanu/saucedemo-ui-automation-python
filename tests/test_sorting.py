import pytest

from pages import InventoryPage


@pytest.mark.regression
def test_sort_name_asc(standard_inventory: InventoryPage):
    standard_inventory.select_sort("Name (A to Z)")
    standard_inventory.assert_sorted_name_asc()


@pytest.mark.regression
def test_sort_name_desc(standard_inventory: InventoryPage):
    standard_inventory.select_sort("Name (Z to A)")
    standard_inventory.assert_sorted_name_desc()


@pytest.mark.regression
def test_sort_price_low_high(standard_inventory: InventoryPage):
    standard_inventory.select_sort("Price (low to high)")
    standard_inventory.assert_sorted_price_asc()


@pytest.mark.regression
@pytest.mark.compatibility
def test_sort_price_high_low(standard_inventory: InventoryPage):
    standard_inventory.select_sort("Price (high to low)")
    standard_inventory.assert_sorted_price_desc()
