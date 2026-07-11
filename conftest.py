import configparser
import os
from typing import Any, Generator

import pytest
from playwright.sync_api import sync_playwright, Browser, Page, ViewportSize


def _get_ini_markers() -> list[str]:
    markers = []
    ini_path = os.path.join(os.path.dirname(__file__), "pytest.ini")

    if not os.path.exists(ini_path):
        return markers

    config = configparser.ConfigParser()
    try:
        config.read(ini_path)
        if "pytest" in config and "markers" in config["pytest"]:
            marker_lines = config["pytest"]["markers"].splitlines()
            for line in marker_lines:
                if ":" in line:
                    marker_name = line.split(":")[0].strip()
                    markers.append(marker_name)
    except Exception:
        pass
    return markers


def pytest_addoption(parser):
    available_markers = _get_ini_markers()

    for marker in available_markers:
        parser.addoption(
            f"--{marker}",
            action="store_true",
            default=False,
            help=f"Run only tests marked as {marker}",
        )


def pytest_collection_modifyitems(config, items):
    available_markers = _get_ini_markers()

    active_flags = [
        m for m in available_markers if config.getoption(f"--{m}", default=False)
    ]

    selected_items = []
    deselected_items = []

    for item in items:
        if active_flags:
            match = all(
                item.get_closest_marker(flag) is not None for flag in active_flags
            )
            if match:
                selected_items.append(item)
            else:
                deselected_items.append(item)

        else:
            has_native_marker_filter = config.getoption("-m") != ""

            if has_native_marker_filter:
                selected_items.append(item)
            else:
                if item.get_closest_marker("api") is None:
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
