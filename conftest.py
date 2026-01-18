import json
import os
from pathlib import Path
from typing import Any, Dict, Optional, Generator

import pytest
from playwright.sync_api import Playwright, Page, BrowserContext
from playwright.sync_api import Browser
from playwright.sync_api import BrowserContext
from playwright.sync_api import Page
from playwright.sync_api import sync_playwright

from pages import InventoryPage
from pages import LoginPage


@pytest.fixture(scope="session")
def users_data() -> Dict[str, Any]:
    data_path = Path(__file__).parent / "data" / "users.json"
    with data_path.open("r", encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture(scope="session")
def base_url(pytestconfig: pytest.Config) -> str:
    """Base URL for AUT.

    Prefer pytest-playwright's built-in --base-url option when present.
    Fall back to BASE_URL env var, then SauceDemo default.
    """

    cli_value: Optional[str]
    try:
        # Provided by pytest-playwright (if installed): --base-url
        cli_value = pytestconfig.getoption("base_url")
    except Exception:
        cli_value = None

    if cli_value:
        return str(cli_value)

    return os.getenv("BASE_URL", "https://www.saucedemo.com/")


@pytest.fixture(scope="session")
def playwright_instance() -> Playwright:
    """Session-scoped Playwright instance.

    We keep this explicit rather than relying on pytest-playwright's fixtures so we can
    create a persistent Chromium context and apply browser profile preferences.
    """
    with sync_playwright() as p:
        yield p


def _is_headless(pytestconfig: pytest.Config) -> bool:
    """Resolve headless mode.

    - If pytest-playwright is installed, it provides --headed (default is headless).
    - We also support HEADLESS env var for CI convenience.
    """

    env = os.getenv("HEADLESS")
    if env is not None:
        return str(env).strip().lower() in {"1", "true", "yes", "y"}

    try:
        headed = bool(pytestconfig.getoption("headed"))
        return not headed
    except Exception:
        # If the option doesn't exist, default to headless=false for local dev.
        return False


def _resolve_browser_name(pytestconfig: pytest.Config) -> str:
    """Resolve desired browser name.

    If pytest-playwright is installed, it provides --browser. Otherwise default to chromium.
    """
    try:
        browser_opt = pytestconfig.getoption("browser")
    except Exception:
        return os.getenv("BROWSER", "chromium")

    if isinstance(browser_opt, (list, tuple)):
        return (browser_opt[0] if browser_opt else "chromium")
    return browser_opt or "chromium"


def _resolve_channel(pytestconfig: pytest.Config) -> Optional[str]:
    """Resolve browser channel (e.g., msedge).

    If pytest-playwright is installed, it provides --browser-channel.
    """
    try:
        channel = pytestconfig.getoption("browser_channel")
    except Exception:
        channel = None

    channel = (str(channel).strip() if channel else "")
    if channel:
        return channel

    env = os.getenv("BROWSER_CHANNEL")
    return env.strip() if env else None


def _write_chromium_preferences(user_data_dir: Path) -> None:
    """Pre-create Chromium Preferences to disable password leak detection popup.

    This prevents the native (non-DOM) 'Change your password' breach dialog from blocking tests.
    Mirrors the Java framework fix: profile.password_manager_leak_detection = false.
    """

    default_dir = user_data_dir / "Default"
    default_dir.mkdir(parents=True, exist_ok=True)
    preferences_path = default_dir / "Preferences"

    prefs = {
        "credentials_enable_service": False,
        "profile": {
            "password_manager_enabled": False,
            "password_manager_leak_detection": False,
        },
    }

    preferences_path.write_text(json.dumps(prefs, indent=2), encoding="utf-8")


@pytest.fixture
def context(
    playwright_instance: Playwright,
    pytestconfig: pytest.Config,
    tmp_path_factory: pytest.TempPathFactory,
) -> Generator[BrowserContext, Any, None]:
    """Provides a clean browser context per test.

    Strategy:
    - Chromium (default) -> persistent context with isolated user-data-dir, allowing profile prefs.
    - Firefox/WebKit     -> regular incognito context.

    Browser selection options (when pytest-playwright is installed):
      --browser chromium|firefox|webkit
      --browser-channel msedge
      --headed
    """

    browser_name = _resolve_browser_name(pytestconfig)
    channel = _resolve_channel(pytestconfig)
    headless = _is_headless(pytestconfig)

    width = int(os.getenv("WINDOW_WIDTH", "1366"))
    height = int(os.getenv("WINDOW_HEIGHT", "768"))

    if browser_name == "chromium":
        user_data_dir = tmp_path_factory.mktemp("pw-chromium-profile")
        _write_chromium_preferences(user_data_dir)

        launch_args: Dict[str, Any] = {
            "headless": headless,
            "viewport": {"width": width, "height": height},
            # Extra hardening: disable the feature flags as well.
            "args": [
                "--disable-features=PasswordLeakDetection,PasswordManager",
                "--disable-notifications",
            ],
        }
        if channel:
            launch_args["channel"] = channel

        ctx = playwright_instance.chromium.launch_persistent_context(str(user_data_dir), **launch_args)
        yield ctx
        ctx.close()
        return

    # Non-Chromium browsers
    browser_type = getattr(playwright_instance, browser_name)
    browser: Browser = browser_type.launch(headless=headless)
    ctx = browser.new_context(viewport={"width": width, "height": height})
    yield ctx
    ctx.close()
    browser.close()


@pytest.fixture
def page(context: BrowserContext) -> Generator[Page, Any, None]:
    p = context.new_page()
    yield p
    p.close()


@pytest.fixture
def login(page: Page, base_url: str, users_data: Dict[str, Any]):
    def _login(username: str, password: Optional[str] = None) -> InventoryPage:
        lp = LoginPage(page, base_url)
        lp.open()
        lp.login(username, password or users_data["password"])
        return InventoryPage(page)

    return _login


@pytest.fixture
def standard_inventory(login) -> InventoryPage:
    inv = login("standard_user")
    inv.is_at()
    return inv
