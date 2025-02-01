import logging

logger = logging.getLogger(__name__)


class ApiConfig:
    """
    This class is responsible for handling the configuration for the API.

    It allows the user to set up the base URL for the API and the path to the secrets stored in GCP or Azure.

    Attributes:
        _base_url (str): The base URL for the API.
        _token_path (str): The client ID for the API.

    """
    def __init__(self,
        base_url: str = "https://some_dummy_weather_station/api",
        token_path: str = "some_dummy_weather_station/token",
    ):

        self._base_url = base_url
        self._token_path = token_path

    @property
    def base_url(self) -> str:
        return self._base_url

    @property
    def token_path(self) -> str:
        return self._token_path

