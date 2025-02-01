import requests
import json
import logging
import concurrent.futures
from copy import copy
from collections import defaultdict
from typing import Dict, List, Optional, Union

import apiutils.data_model as dm
from apiutils.api_config import ApiConfig
from apiutils.token_handler import TokenHandler
from apiutils import exceptions as ex


logger = logging.getLogger(__name__)


class GetWeatherData:
    """
    Get data from external api for specific location. 
    
    Methods:
        get_data: Get Weather data for specific locations

    Args:
        user_defined_config (ApiConfig): Class with configuration details
        max_workers (int): Number of threads
        max_retries (int): Number of retries for API calls
        allow_failure (bool): If False, non existing locations will be returned as empty list

    Raises:
        Exception: BASE_URL not defined

    Examples:
        weather_api = GetWeatherData()
        weather_api.get_data(locations=['location1', 'location2'])
    """

    def __init__(
        self,
        user_defined_config: Optional[ApiConfig] = None,
        max_workers: int = 8,
        max_retries: int = 3,
        allow_failure: bool = True,
    ):
        if user_defined_config is None:
            config = ApiConfig()
        else:
            config = user_defined_config

        self.token_handler = TokenHandler(config)
        self.base_url = config.base_url

        self.data = defaultdict(list)

        self.headers = None
        self.params = None

        self.max_workers = max_workers
        self.max_retries = max_retries
        self.allow_failure = allow_failure

    def _urljoin(self, elems: List[str]) -> str:
        """
        Join elements to an url

        Args:
            elems (List[str]): List of url elements

        Returns:
            str: Joined url elements

        Examples:
            urljoin(['https://www.john.com', 'bla', 'ola'])
            'https://www.john.com/bla/ola'
        """

        return "/".join(map(lambda x: str(x).strip("/"), elems))

    def _reset_data(self) -> None:
        """
        Reset data - will be called before each separate api call
        """

        logger.info("Reset data")

        self.data = defaultdict(list)

        return None

    def _set_header(self) -> None:
        """
        Checks if token is available and sets header for authentication

        Args:
            None

        Returns:
            None

        raises:
            Exception: No Authentication Token found
        """
        logger.info("Set header token for Authentication")

        token = self.token_handler.get_token()

        if token:
            self.headers = {"Authorization": f"Bearer {token}"}
        else:
            raise ex.NoAuthentication("No Authentication Token found")

    def get_requests(self, urls: List[Dict]) -> None:
        """
        Get requests for urls - calls threaded requests defined by max_workers

        This method will be called by every api method. Data from previous calls
        will be deleted!

        Args:
            urls (List[Dict]): List with location and url
        """
        self._reset_data()

        if self.headers is None:
            self._set_header()

        max_workers = max(1, min(self.max_workers, len(urls)))

        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            _ = executor.map(self.get_request, urls)

        return None

    def get_request(self, url: Dict) -> None:
        """
        Gets data from url and stores it in self.data. Allowing multiple retries.

        Args:
            url (Dict): Dict with location and url

        Raises:
            Exception: If max_retries is reached
        """

        failed_retries = 0

        _location = url.get("location")
        logger.info(f"Get Request for weather forecast of location: {_location}")

        session = requests.Session()  
        session.headers = self.headers

        params = copy(self.params)

        while failed_retries < self.max_retries:
            response = self._get_request(session, url.get("url"), params)

            if response.status_code != 200:
                status_code = response.status_code
                text = f"Retry request for {_location} because {response.text}"

                logging.error(ex.ApiException(status_code, text))

                if response.status_code == 403:
                    self._set_header()
                    session.headers = self.headers

                failed_retries += 1

                continue

            response = json.loads(response.text)

            self._update_data(response, _location)


        if failed_retries >= self.max_retries:
            raise ex.ApiException(response.status_code, response.text)

        return None

    def _get_request(
        self, session: requests.Session, url: str, params: Dict
    ) -> requests.Response:
        """
        Get request for url 

        Args:
            session (requests.Session): Session object
            url (str): Url for API call

        Returns:
            requests.Response: Response from API call
        """
        logger.info(f"API call for url: {url}")

        try:
            response = session.get(url, params=params, verify=False, timeout=60)

        except Exception as e:
            raise e

        return response

    def _update_data(self, response: Dict, _location: str) -> None:
        """
        Update data with response 

        Args:
            response (Dict): Response from API call
            _location (str): location

        Returns:
            None
        """

        logger.info(f"Update data for location: {_location}")

        self.data[_location].append(response)

        return None

    def _manipulate_data(self, locations: Union[List[str], str]) -> None:
        """
        Non existing locations will be manipulated to return an empty list

        This assures, that all locations in the request will be present in the output

        Args:
            locations (Union[List[str], str]): List of locations

        Returns:
            None

        Examples:
            self.data = {'location1': ["test"]}
            _manipulate_data(locations=['location1', 'location2'])
            self.data = {'location1': ["test"], 'location2': []}
        """
        if isinstance(locations, str):
            locations = [locations]

        for _location in locations:
            if _location in self.data:
                continue

            self.data[_location] = []

        return None


    def get_data(self, locations: Union[List[str], str], params={}) -> dm.WeatherDataOutput:
        """
        Get data for specific locations by calling the external api

        Args:
            locations (Union[List[str], str]): List of locations
            params (Dict): Parameters for API endpoint call

        Returns:
            Dict: WeatherDataOutput
        """
        if isinstance(locations, str):
            locations = [locations]

        self.params = dm.ApiDataParams(**params).model_dump(exclude_none=True)

        urls = []

        for _location in locations:
            temp = {
                "location": _location,
                "url": self._urljoin([self.base_url,  _location, "data"]),
            }
            urls.append(temp)

        self.get_requests(urls)

        if not self.allow_failure:
            self._manipulate_data(locations)

        return dm.WeatherDataOutput(**self.data).model_dump()