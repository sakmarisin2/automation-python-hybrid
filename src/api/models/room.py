from pydantic import BaseModel, ConfigDict, Field


class Room(BaseModel):
    model_config = ConfigDict(populate_by_name=True, from_attributes=True)

    room_id: int = Field(..., alias="roomid")
    room_name: str = Field(..., alias="roomName")
    room_price: int = Field(..., alias="roomPrice")
    room_type: str = Field(..., alias="type")

    accessible: bool
    description: str
    image: str
    features: list[str]
