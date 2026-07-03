def pytest_addoption(parser):
    group = parser.getgroup("playwright", "Playwright")
    group.addoption("--api", action="store", type=str, help="Run api tests")


def pytest_collection_modifyitems(config, items):
    is_api_flag_active = config.getoption("--api")

    selected_items = []
    deselected_items = []

    for item in items:
        has_api_marker = item.get_closest_marker("api") is not None
        if is_api_flag_active:
            if has_api_marker:
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


pytest_plugins = ["src.fixtures.services", "src.fixtures.setup"]
