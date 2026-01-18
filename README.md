# SauceDemo Demo Automation Framework (Python)

This is a **demo** regression framework for [https://www.saucedemo.com](https://www.saucedemo.com) using:

* Python 3.10+
* Pytest
* Playwright (sync API)
* Page Object Model (POM)

It covers: authentication (all users), menu, sorting (“filtering”), cart, and checkout.
Special-user scenarios are marked as `known_bug`.

## Quick start

### Prerequisites

* Python 3.10+ (3.11 recommended)
* Browsers installed by Playwright (`playwright install`)

### Setup

```bash
# Windows (recommended): use the Python Launcher (`py`) if `python` is not on PATH
py -m venv .venv
.\.venv\Scripts\activate
py -m pip install -r requirements.txt
py -m playwright install

# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
playwright install
```

## Run all tests

```bash
pytest -q
```

To **see the browser running**:

```bash
pytest --headed -q
```

## Run by marker

```bash
pytest -m smoke -q
pytest -m regression -q
pytest -m known_bug -q
pytest -m compatibility -q
```

(You can combine with `--headed` as needed.)

## Browser selection (Chromium / Firefox / Edge)

This demo supports:

* `chromium` (default)
* `firefox` (compatibility lane)
* `edge` via Playwright channel `msedge` (compatibility lane; requires Microsoft Edge installed)

Examples:

```bash
# Firefox
pytest -m compatibility --browser firefox -q

# Edge (requires Microsoft Edge installed on the machine)
pytest -m compatibility --browser chromium --browser-channel msedge -q
```

To run these **headed**:

```bash
pytest -m compatibility --browser firefox --headed -q
pytest -m compatibility --browser chromium --browser-channel msedge --headed -q
```

## Base URL override

By default, the framework targets `https://www.saucedemo.com/`. Override via:

```bash
pytest --base-url https://www.saucedemo.com/ -q
```

Or environment variable:

```bash
# PowerShell
$env:BASE_URL="https://www.saucedemo.com/"
pytest -q
```

## Window size and headless control

This framework uses a consistent viewport by default. You can override via environment variables:

```bash
# PowerShell
$env:WINDOW_WIDTH="1366"
$env:WINDOW_HEIGHT="768"
pytest --headed -q
```

You can also control headless mode via environment variable (useful for CI):

```bash
# PowerShell
$env:HEADLESS="true"
pytest -q
```

Note: `--headed` (when available) takes precedence for interactive runs.

## Framework structure

* `pages/` – Page Objects
* `tests/` – Pytest tests
* `data/` – test data (users)
* `conftest.py` – fixtures and browser lifecycle (persistent Chromium context, base_url resolution)

## Notes

* Designed to be readable and extensible, not a full enterprise solution.
* Recommended CI split: `smoke` on PR, `regression` nightly.
* For Chromium (Chrome/Edge channels), the framework uses an isolated persistent profile per test and disables
  password leak detection to prevent the native (non-DOM) “Change your password” dialog from blocking UI actions.
