from httpx import Response

from src.api.core.builder import Builder
from src.api.core.base_models import DataType


class HttpClient(Builder):

    def _request(self, method: str) -> Response | None:
        if not self.request_data:
            raise ValueError("Request data is not built. Call build_request() first.")

        is_form_data = self._current_data_type == DataType.FORM_DATA.value

        self.response_data = self.session.request(
            method=method,
            url=self.request_data.uri,
            params=self.request_data.params,
            headers=self.request_data.headers,
            json=self.request_data.json if not is_form_data else None,
            data=self.request_data.json if is_form_data else None
        )

        assert self.response_data.status_code == self.status_code
        return self.response_data

    def get(self):
        self._request(method="GET")
        return self

    def post(self):
        self._request(method="POST")
        return self

    def put(self):
        self._request(method="PUT")
        return self

    def delete(self):
        self._request(method="DELETE")
        return self

    def patch(self):
        self._request(method="PATCH")
        return self
