from dataclasses import dataclass
from enum import Enum
from typing import Any


@dataclass
class BaseConfig:
    api_base_url: str

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
