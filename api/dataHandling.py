import json
import requests
import os
import sys
from companies import company_dictionary


def call_api(company_dictionary, dateRange: int) -> json:
    """Call the Financial Modeling Prep API to get historical price data for a given company.

    This function takes a company symbol and a date range as input, and returns a JSON
    object with historical price data for the specified company.

    Args:

        company (str): The symbol of the company whose historical price data is to be retrieved.
        dateRange (int): The number of days of historical data to be retrieved.


    Returns:

        dict: A dictionary containing historical price data for the given company. The dictionary
        has two master keys: 'symbol' and 'historical'. The 'historical' key contains an array
        of dictionaries, each representing a specific date's data with keys like 'date', 'open',
        'close', and 'change'.


    Raises:

        N/A: This function does not raise any specific exceptions on its own, but it may raise
        exceptions related to network connectivity, invalid API response, or missing API key.


    Note:

        The function expects an environment
        variable named 'api-token' to be set with the valid API key from Financial Modeling Prep
        (https://financialmodelingprep.com/). Make sure to set the API key as an environment
        variable before calling this function.

        Example API endpoint for retrieving historical price data:
        https://financialmodelingprep.com/api/v3/historical-price-full/{company}?timeseries={dateRange}&apikey={api_key}
    """

    from dotenv import load_dotenv

    load_dotenv()
    api_key = os.environ.get("api-token")
    return_format = "json"

    url = f"https://api.polygon.io/v2/aggs/grouped/locale/us/market/stocks/2023-01-09?adjusted=true&apiKey={api_key}"
    try:
        data = requests.get(url).json()
        i=0
        sortedData = []
        while i < len(data['results']):
            print(i)
            diction = data['results'][i]
            if diction["T"] in company_dictionary:
                sortedData.append(diction)
            i+=1
        return sortedData
    except:
        sys.exit("An error occured")


def cleanse_data(originalIn: json) -> json:
    pass

print(call_api(company_dictionary, 1))