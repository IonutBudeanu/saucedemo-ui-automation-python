import pytest

from pages import LoginPage, InventoryPage


@pytest.mark.regression
@pytest.mark.smoke
def test_standard_user_can_login(page, base_url, users_data):
    lp = LoginPage(page, base_url)
    lp.open()
    lp.login("standard_user", users_data["password"])
    inv = InventoryPage(page)
    inv.is_at()


@pytest.mark.regression
@pytest.mark.negative
def test_locked_out_user_rejected(page, base_url, users_data):
    lp = LoginPage(page, base_url)
    lp.open()
    lp.login("locked_out_user", users_data["password"])
    assert "locked" in lp.error_text().lower()


@pytest.mark.regression
@pytest.mark.negative
def test_invalid_password_rejected(page, base_url):
    lp = LoginPage(page, base_url)
    lp.open()
    lp.login("standard_user", "wrong_password")
    assert "do not match" in lp.error_text().lower()


@pytest.mark.regression
@pytest.mark.parametrize(
    "username",
    [
        pytest.param("problem_user", marks=pytest.mark.known_bug),
        pytest.param("performance_glitch_user", marks=pytest.mark.known_bug),
        pytest.param("error_user", marks=pytest.mark.known_bug),
        pytest.param("visual_user", marks=pytest.mark.known_bug),
    ],
)
def test_special_users_can_login_known_bug(username, page, base_url, users_data):
    lp = LoginPage(page, base_url)
    lp.open()
    lp.login(username, users_data["password"])
    inv = InventoryPage(page)
    inv.is_at()
