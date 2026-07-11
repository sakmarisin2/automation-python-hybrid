import allure
import pytest

from src.web.pages.main_page import MainPage


@allure.epic("Web interface")
@pytest.mark.regression
@pytest.mark.ui
def test_main_page_header(page_factory):
    main_page = page_factory(MainPage)
    assert main_page.get_header_text() == "Shady Meadows B&B"
