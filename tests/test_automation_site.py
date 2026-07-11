import allure
import pytest


@allure.epic("Api interface")
@pytest.mark.regression
@pytest.mark.api
def test_get_automation_site_room(automation_service):
    res = automation_service.get_booking_room()

    assert (
        res.description
        == "Aenean porttitor mauris sit amet lacinia molestie. In posuere accumsan aliquet. Maecenas sit amet nisl massa. Interdum et malesuada fames ac ante."
    )
