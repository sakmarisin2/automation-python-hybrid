from dataclasses import dataclass
from enum import Enum
from typing import Any


@dataclass
class RequestData:
    uri: str
    params: dict
    json: dict[str, Any] | None
    headers: dict


class DataType(Enum):
    JSON = "json"
    FORM_DATA = "form_data"
    JSON_WITH_NULL = "json_with_null"


class HttpStatus(Enum):
    OK = 200
    CREATED = 201
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    METHOD_NOT_ALLOWED = 405
    INTERNAL_SERVER_ERROR = 500
    NOT_IMPLEMENTED = 501
