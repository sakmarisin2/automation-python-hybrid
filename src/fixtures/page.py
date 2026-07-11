import pytest

from src.web.core.base_page import BasePage


@pytest.fixture
def page_factory(page, base_config):
    def _wrapper(pageobj: type[BasePage]):
        _page = pageobj(page=page, url=base_config.api_base_url)
        _page.open()
        return _page

    return _wrapper
