import json
from typing import Optional, Dict, Any, Union, List, Type, TypeVar
import httpx
from pydantic import BaseModel

from src.api.core.serializer import get_serializer
from src.api.core.base_models import RequestData, HttpStatus, DataType
from src.config.base import BaseConfig

T = TypeVar("T", bound=BaseModel)


class Builder:
    def __init__(
        self,
        session: httpx.Client,
        config: BaseConfig,
        headers: Optional[Dict[str, str]] = None,
    ):
        self.session = session
        self.config = config
        self.status_code = HttpStatus.OK.value
        self.headers = headers or {}
        self.request_data: Optional[RequestData] = None
        self.response_data: Optional[httpx.Response] = None
        self._current_data_type: str = DataType.JSON.value

    def get_url(self, endpoint: str) -> str:
        return self.config.base_url + endpoint

    def get_headers(self) -> Dict[str, str]:
        return {**self.headers}

    def build_request(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        payload: Optional[Union[BaseModel, List[BaseModel], Dict[str, Any]]] = None,
        data_type: str = DataType.JSON.value,
    ):
        self._current_data_type = data_type

        serializer = get_serializer(data_type)
        serialized_payload = serializer.serialize(payload)
        final_json_payload = None

        if serialized_payload is not None:
            if isinstance(serialized_payload, str):

                final_json_payload = json.loads(serialized_payload)
            else:
                final_json_payload = serialized_payload

        self.request_data = RequestData(
            uri=self.get_url(endpoint),
            params=params or {},
            headers=self.get_headers(),
            json=final_json_payload,
        )

        return self

    def parse_response(self, schema: Type[T]) -> Union[T, List[T], None]:
        if self.response_data is None:
            raise ValueError(
                "No response data available. Please execute the request first."
            )

        serializer = get_serializer(self._current_data_type)
        return serializer.deserialize(self.response_data, schema)
