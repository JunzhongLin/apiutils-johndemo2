import json
import logging
import requests
from typing import Optional
from apiutils.api_config import ApiConfig


logger = logging.getLogger()
logger.setLevel("INFO")


class TokenHandler:
    """
    A handler for getting tokens for API.

    This class is responsible for getting tokens for the Weather API. The tokens are
    retrieved from Key vault or secret manager.

    Attributes:
        config (ApiConfig): An instance of the ApiConfig class containing configuration details.

    Methods:
        get_token() -> Optional[str]:
            Retrieves an authentication token.

    """
    def __init__(self, config: ApiConfig):
        self.config = config

    def get_token(self) -> Optional[str]:
        """
        Gets authentication token

        Args:
            None

        Returns:
            Optional[str]: Authentication token or None
        """

        try:
            logger.info("Getting token from key vault based on client_id and client_secret in api_config")
        except Exception as e:
            raise e

        logger.info("returning token")
        pass


