import pytest

from pages import InventoryPage, CartPage
from pages import CheckoutStepOnePage, CheckoutOverviewPage, CheckoutCompletePage


@pytest.mark.smoke
@pytest.mark.regression
def test_add_all_and_remove_all_from_cart(standard_inventory: InventoryPage):
    inv_count = standard_inventory.inventory_count()
    standard_inventory.add_all_items()
    assert standard_inventory.cart_count() == inv_count

    standard_inventory.open_cart()
    cart = CartPage(standard_inventory.page)
    cart.wait_for_ready()
    cart.assert_item_count(inv_count)

    cart.remove_all_items()
    cart.assert_item_count(0)


@pytest.mark.smoke
@pytest.mark.regression
def test_place_order_happy_path_all_products(standard_inventory: InventoryPage):
    standard_inventory.add_all_items()
    standard_inventory.open_cart()
    cart = CartPage(standard_inventory.page)
    cart.start_checkout()

    c1 = CheckoutStepOnePage(standard_inventory.page)
    c1.is_at()
    c1.fill("John", "Doe", "12345")
    c1.continue_checkout()

    c2 = CheckoutOverviewPage(standard_inventory.page)
    c2.is_at()
    c2.finish()

    done = CheckoutCompletePage(standard_inventory.page)
    done.is_at()
    assert "thank" in done.confirmation_message().lower()


@pytest.mark.regression
@pytest.mark.negative
@pytest.mark.parametrize(
    "first,last,zip_code,expected_fragment",
    [
        ("", "Doe", "12345", "First Name"),
        ("John", "", "12345", "Last Name"),
        ("John", "Doe", "", "Postal Code"),
    ],
)
def test_checkout_required_field_validation(standard_inventory: InventoryPage, first, last, zip_code,
                                            expected_fragment):
    standard_inventory.add_all_items()
    standard_inventory.open_cart()
    cart = CartPage(standard_inventory.page)
    cart.start_checkout()

    c1 = CheckoutStepOnePage(standard_inventory.page)
    c1.fill(first, last, zip_code)
    c1.continue_checkout()
    assert expected_fragment.lower() in c1.error_text().lower()
