import json
import requests
import os
import sys


def call_api(company: str, dateRange: int) -> json:
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
    url = f"https://financialmodelingprep.com/api/v3/historical-price-full/{company}?timeseries={dateRange}&apikey={api_key}"
    try:
        return requests.get(url).json()
    except:
        sys.exit("Invalid api URL")


def cleanse_data(originalIn: json) -> json:
    """Cleanse the original JSON data by removing unnecessary fields from the historical records.

    This function takes the original JSON data as input and creates a copy of it. It then iterates
    through the "historical" records in the copied data and removes specific fields that are
    considered unnecessary for further processing.

    Args:

        originalIn (json): The original JSON data containing historical price records.


    Returns:

        json: A modified JSON object with unnecessary fields removed from the historical records.


    Raises:

        N/A: This function does not raise any specific exceptions on its own.


    Note:

        The JSON given as the argument is not modified in place: a copy is made and this is modified and returned (for clarity
        and bug)
        The function assumes that the input JSON data follows a specific structure where there
        is a "historical" key containing an array of dictionaries, each representing a specific
        date's data with keys like 'date', 'open', 'high', 'low'. The function removes the following fields from
        each historical record: 'open', 'high', 'low', 'unadjustedVolume', 'vwap', 'label', and
        'changeOverTime'. If the input JSON structure deviates from this assumption, the function
        may not work as expected.
    """

    dirtyData = originalIn.copy()

    try:

        for dictionary in dirtyData["historical"]:
            del dictionary["open"]
            del dictionary["high"]
            del dictionary["low"]
            del dictionary["unadjustedVolume"]
            del dictionary["vwap"]
            del dictionary["label"]
            del dictionary["changeOverTime"]

        return dirtyData
    except KeyError:
        sys.exit("Invalid company acronym")


if __name__ == "__main__":
    # from companies import company_dictionary
    # for company in company_dictionary:
    #     print(cleanse_data(call_api(company, 1)))
