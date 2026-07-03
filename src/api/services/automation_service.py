from src.api.constants.controllers import AutomationTestingService
from src.api.core.http_client import HttpClient
from src.api.models.room import Room


class AutomationService(HttpClient):
    def get_booking_room(self, room_number=1) -> Room:
        return (
            self.build_request(
                endpoint=AutomationTestingService.GET_ROOM.format(
                    room_number=room_number
                ),
                params=None,
                payload=None,
            )
            .get()
            .parse_response(Room)
        )
