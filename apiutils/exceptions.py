import http
from typing import Optional

class NoAuthentication(Exception):
    def __init__(self, text: str):
        self.text = text


class ApiException(Exception):
    def __init__(
        self,
        status_code: int,
        detail: Optional[str] = None,
    ) -> None:
        if detail is None:
            detail = http.HTTPStatus(status_code).phrase
        self.status_code = status_code
        self.detail = detail

    def __str__(self) -> str:
        return f"{self.status_code}: {self.detail}"

    def __repr__(self) -> str:
        class_name = self.__class__.__name__
        return f"{class_name}(status_code={self.status_code!r}, detail={self.detail!r})"
