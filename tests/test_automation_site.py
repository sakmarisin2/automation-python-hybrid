import pytest


@pytest.mark.api
def test_get_automation_site_room(automation_service):
    res = automation_service.get_booking_room()

    assert res.room_id
    assert res.accessible
