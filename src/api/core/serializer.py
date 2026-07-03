from abc import ABC, abstractmethod

import httpx
from pydantic import json

from src.api.core.base_models import DataType


class Serializer(ABC):

    @abstractmethod
    def serialize(self, payload):
        pass

    @abstractmethod
    def deserialize(self, response_data, schema):
        pass


class JSONSerializer(Serializer):
    exclude_none = True

    def serialize(self, payload):
        if payload is None:
            return payload

        elif isinstance(payload, list):
            payload = [
                i.model_dump(by_alias=True, exclude=self.exclude_none) for i in payload
            ]
            return json.dumps(payload)

        elif isinstance(payload, dict):
            return json.dumps(payload)

        dict_payload = payload.model_dump(by_alias=True, exclude=self.exclude_none)
        return json.dumps(dict_payload)

    def deserialize(self, response_data: httpx.Response, schema):
        if not response_data.text:
            return None
        json_repr = response_data.json()

        if isinstance(json_repr, list):
            return [schema(**i) for i in json_repr]

        return schema(**json_repr)


class FormDataSerializer(Serializer):
    def serialize(self, payload):
        if payload is None:
            return payload
        return payload.model_dump(by_alias=True)

    def deserialize(self, response_data, schema):
        pass


class JsonWithNullValuesSerializer(JSONSerializer):
    exclude_none = False


_mapper = {
    DataType.JSON.value: JSONSerializer,
    DataType.FORM_DATA.value: FormDataSerializer,
    DataType.JSON_WITH_NULL.value: JsonWithNullValuesSerializer,
}


def get_serializer(data_type: str):
    Serializer = _mapper.get(data_type)
    return Serializer()
