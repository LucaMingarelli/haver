"""  Created on 24/01/2024::
------------- haver.py -------------
 
DOCS at https://api.haverview.com/v4/docs

**Authors**: L. Mingarelli
"""

import requests

from haver.haver_maps import HAVER_COUNTRIES

import os, warnings
import pandas as pd
from collections.abc import Iterable
from typing import Optional, Union, Dict


class Haver:
    """Implementation of the Haver View REST API.
    """
    _HAVER_URL = 'https://api.haverview.com'
    __NO_TOKEN_WARNING = """
    Invalid or Expired Haver api_key.
    Please set as environment variable `HAVER_API_KEY` or initialise haver as  Haver(api_key='<your-token>').
        """

    def __init__(self, api_key: Optional[str] = None,
                 verify=None, proxies=None,
                 request_kwargs: Union[Dict, None] = None):
        self.__is_active = False
        self._headers = None
        self._request_kwargs = dict(headers=self._headers)
        if proxies:
            self._request_kwargs = {**self._request_kwargs, **dict(proxies=proxies)}
        if verify:
            self._request_kwargs = {**self._request_kwargs, **dict(verify=verify)}
        if request_kwargs:
            self._request_kwargs = {**self._request_kwargs, **request_kwargs}
        self.__api_key = None
        self.__api_key = api_key or self._get_token()
        if self.__api_key:
            self.__is_active = self.__test_connection(api_key=api_key)



    def __make_headers(self, api_key):
        return {'Content-Type': 'application/json',
                'X-API-Key': api_key}
    
    def __make__request_kwargs(self, headers=None):
        return {**self._request_kwargs, **dict(headers=headers or self._headers)}

    def __test_connection(self, api_key):
        _headers = self.__make_headers(api_key=api_key)
        _request_kwargs = self.__make__request_kwargs(headers=_headers)
        try:
            _active = requests.get('https://api.haverview.com/v4/docs',
                                   **_request_kwargs).status_code == 200
        except:
            _active = False
        if _active:
            self._headers = _headers
            self._request_kwargs = _request_kwargs

        return _active

    def connect(self, api_key: Optional[str] = None):
        """Connect with private token.

        Args:
            api_key: Personal access token.
        """
        self.__init__(api_key=api_key)
        if not self._is_connected:
            warnings.warn(self.__NO_TOKEN_WARNING)

    def _get_token(self):
        if self.__api_key is not None:
            return self.__api_key
        if 'HAVER_API_KEY' in os.environ:
            api_key = os.environ['HAVER_API_KEY']
            return api_key
        
        else:
            warnings.warn(self.__NO_TOKEN_WARNING)

    @property
    def _is_connected(self):
        return self.__test_connection(api_key=self._get_token())

    def get_databases(self) -> Dict:
        """
        Lists all available databases.

        Returns:
            Dict

        Examples:
            >>> import haver
            >>> haver.get_databases()
        """
        dbs = requests.get(f'{self._HAVER_URL}/v4/database?&per_page=1000', **self._request_kwargs).json()
        return {db['name']: db['description'] for db in dbs}

    def database_info(self, database: str) -> Dict:
        """
        Returns information on given database.

        Args:
            database: Name of Haver database.

        Returns:
            Dict

        Examples:
            >>> import haver
            >>> haver.database_info('USECON')
        """
        return requests.get(f'{self._HAVER_URL}/v4/database/{database}/series?&per_page=1', **self._request_kwargs).json()['data'][0]

    def get_series(self, database: str,
                   like: Union[str, None] = None,
                   full_info: bool = False, limit: int = 1000):
        """Returns list of series available in a given database.

        Args:
            database: Name of the Haver database.
            like: String used to search for similar series names. It does not necessarily need to be an existing series.
            full_info: Default is `False`, and will return alist of dictionaries with key the series names and description as values. If `True` instead, returns additional information: name, databaseName, datetimeLastModified, startingPeriod, dataPointCount, frequency, magnitude, decimalPrecision, differenceType, aggregationType, dataType, groupName, shortSourceName, sourceName,  description,  geography, geography2, startDate, originalFrequency.
            limit: Return at most `limit` items.

        Returns:
            Dict or List[Dict]

        Examples:
            >>> import haver
            >>> haver.get_series(database='USECON', limit=2, full_info=True)
        """
        series = requests.get(
            f"{self._HAVER_URL}/v4/database/{database}/series?{f'&page={like}' if like else ''}{f'&per_page={limit}' if limit else ''}",
            **self._request_kwargs).json()
        if not full_info:
            series = {s['name']: s['description'] for s in series['data']}
        return series

    def search(self, query: str):
        """
        Returns a list of all series with the specified keywords in their name,
        grouped by databases accessible to the user's organization.
        Args:
            query: string search by similarity.

        Returns:

        Examples:
            >>> import haver
            >>> haver.search(query='employment')
        """
        search_res = requests.get(f"{self._HAVER_URL}/v4/data/search?query={query}",
                             **self._request_kwargs).json()
        return search_res

    def recessions(self) -> pd.DataFrame:
        """
        Returns all available recessions with associated start and end dates, and country.
        """
        rec = requests.get(f"{self._HAVER_URL}/v4/data/recessions?&per_page=1000",
                      **self._request_kwargs).json()['data']
        return pd.DataFrame(rec).drop(columns='index')

    def read(self, database: str, series: str) -> Dict:
        """
        Args:
            database: An Haver database.
            series: A Haver series available within `database`.

        Returns:
            Dict

        Examples:
            >>> import haver
            >>> haver.read(database='EUDATA', series='N997CE')
        """

        if not isinstance(series, str):
            raise ValueError(f"The argument 'haver_codes' must be a string, instead {type(series)} was passed.")
        if not isinstance(database, str):
            raise ValueError(f"The argument 'haver_codes' must be a string, instead {type(database)} was passed.")

        # Put the URL for the Haver View API call together
        API_URL = f'{self._HAVER_URL}/v4/database/{database}/series/{series}'

        # Run the API call and get content in JSON format
        content_json = requests.get(API_URL, **self._request_kwargs).json()
        return content_json

    def read_df(self, haver_codes: list) -> pd.DataFrame:
        """

        Args:
            haver_codes: A list of haver codes constructed as `{series}@{database}`

        Returns:
            pandas.DataFrame

        Examples:
            >>> import haver
            >>> haver.read_df(['N997CE@EUDATA','N025CE@EUDATA'])
        """

        if not isinstance(haver_codes, Iterable) or isinstance(haver_codes, str):
            raise ValueError(
                f"The argument 'haver_codes' should be a list-like iterable, instead {type(haver_codes)} was received.")

        # Loop through the list of Haver codes
        df_final = pd.DataFrame()
        for haver_code in haver_codes:
            series, database = haver_code.split(sep='@')

            content_json = self.read(database=database, series=series)
            content_json_dp = content_json['dataPoints']

            # mapping of Haver country codes with ISO2 country codes and country names
            # https://www.haver.com/client/resources/geo-codes

            # Create pandas dataframe
            df = pd.DataFrame(content_json_dp).rename(columns={'nSeriesData': 'value'})
            df['variable'] = content_json['name'].lower()
            df['country'] = content_json['geography']
            df['country_alpha2'] = HAVER_COUNTRIES[content_json['geography']]['alpha2']
            df['country_name'] = HAVER_COUNTRIES[content_json['geography']]['name']
            df['database'] = database.lower()

            # Append to final dataframe
            df_final = pd.concat([df_final, df])

        # Rearrange columns
        df_final = df_final[['date', 'country', 'country_alpha2',
                             'country_name', 'database', 'variable', 'value']]

        return df_final



if __name__ == '__main__':
    import os
    haver = Haver(api_key=os.getenv('HAVER_API_KEY'))
    haver.get_series(database='EUDATA')
    tt = haver.read_df(haver_codes=['N997CE@EUDATA', 'N025CE@EUDATA'])

