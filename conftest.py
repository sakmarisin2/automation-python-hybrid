from typing import Any, Generator

import pytest
from playwright.sync_api import sync_playwright, Browser, Page, ViewportSize


def pytest_addoption(parser):
    parser.addoption(
        "--api", action="store_true", default=False, help="Run only API tests"
    )
    parser.addoption(
        "--ui", action="store_true", default=False, help="Run only UI tests"
    )
    parser.addoption(
        "--regression",
        action="store_true",
        default=False,
        help="Run regression suite tests",
    )


def pytest_collection_modifyitems(config, items):
    is_api_active = config.getoption("--api")
    is_ui_active = config.getoption("--ui")
    is_regression_active = config.getoption("--regression")

    selected_items = []
    deselected_items = []

    for item in items:
        has_api_marker = item.get_closest_marker("api") is not None
        has_ui_marker = item.get_closest_marker("ui") is not None
        has_regression_marker = item.get_closest_marker("regression") is not None

        if is_regression_active:
            if has_regression_marker:
                selected_items.append(item)
            else:
                deselected_items.append(item)
        elif is_api_active:
            if has_api_marker:
                selected_items.append(item)
            else:
                deselected_items.append(item)
        elif is_ui_active:
            if has_ui_marker:
                selected_items.append(item)
            else:
                deselected_items.append(item)

        else:
            if not has_api_marker:
                selected_items.append(item)
            else:
                deselected_items.append(item)

    config.hook.pytest_deselected(items=deselected_items)
    items[:] = selected_items


@pytest.fixture(scope="session")
def browser() -> Generator[Browser, Any, None]:
    with sync_playwright() as playwright:
        browser_instance = playwright.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-gpu", "--window-size=1920,1080"],
        )
        yield browser_instance
        browser_instance.close()


@pytest.fixture(scope="function")
def page(browser: Browser) -> Generator[Page, Any, None]:
    view = ViewportSize(width=1920, height=1080)
    context = browser.new_context(viewport=view)

    page_instance = context.new_page()

    yield page_instance

    page_instance.close()
    context.close()


pytest_plugins = ["src.fixtures.services", "src.fixtures.setup", "src.fixtures.page"]
