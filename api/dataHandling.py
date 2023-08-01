# The raw data from the api follows this format: {key:value, key:value, results:[ticker:"APPL", ...]}

# The cleansed data is as follows: [date, {ticker:"AAPL", ...}]


import requests


def call_all_companies(date: str) -> list:
    """
    Retrieves data about companies from an API based on the given date.

    Parameters:
        date (str): The date in the format 'yyyy-mm-dd' for which data is requested.

    Returns:
        list: A list containing the date (element 0) and relevant company data as dictionaries (subsequent elements are dictionaries).

    Raises:
        Exception: if the API call fails or returns an error

    Dependencies:
        - The function relies on the 'requests' module to make API calls.
        - The function also depends on a 'companies' module that contains the 'company_dictionary'.
        - The function requires the 'dotenv' module to load environment variables.

    Note:
        - Make sure to set up the 'api-token' environment variable with your API key.
        - The function will filter for relevant companies based on the 'company_dictionary'.

    Example:
        >>> data = call_all_companies('2023-07-31')
        >>> print(data)
        ['2023-07-31', {'c': 100.2, 'h': 105.0, 'l': 99.5, 'o': 101.0, 't': 166726400000, 'n': 1200, 'v': 500000}]
    """

    import os
    from dotenv import load_dotenv
    from companies import company_dictionary

    load_dotenv()
    api_key = os.environ.get("api-token")

    url = f"https://api.polygon.io/v2/aggs/grouped/locale/us/market/stocks/{date}?adjusted=true&apiKey={api_key}"

    try:
        rawData = requests.get(url).json()
    except:
        print("API did not return a result")
        return -1

    counter = 0
    companySortedData = [date]
    while counter < len(rawData["results"]):
        subDictionary = rawData["results"][counter]
        if (
            subDictionary["T"] in company_dictionary
        ):  # rawData contains many more companies then we need hence...
            companySortedData.append(subDictionary)
        counter += 1

    return companySortedData


def call_ticker_current(ticker: str) -> list:
    """
    Fetches the current stock data for a given ticker by webscraping the Polygon.io site.

    Parameters:
        ticker (str): The ticker symbol of the stock.

    Returns:
        list: A list containing the current stock data in the following format:
            [date, {"ticker": ticker, "currentOpen": open_price, "currentHigh": high_price,
            "currentLow": low_price, "currentVolume": volume, "prevClose": previous_close_price,
            "currentPrice": current_price, "currentPercentageChange": percentage_change}]
            - date (str): The current date in the format 'YYYY-MM-DD'.
            - ticker (str): The provided ticker symbol.
            - currentOpen (float): The opening price of the current trading session.
            - currentHigh (float): The highest price of the current trading session.
            - currentLow (float): The lowest price of the current trading session.
            - currentVolume (int): The current trading volume.
            - prevClose (float): The closing price of the previous trading session.
            - currentPrice (float): The current price of the stock.
            - currentPercentageChange (str): The percentage change of the stock price from the opening.

    Raises:
        NameError: If the provided ticker yields a non-200 status code response from the Polygon.io API.

    Dependencies:
        - bs4 (BeautifulSoup): For parsing HTML content.
        - re (Regular Expression): For pattern matching.
        - datetime: For capturing the current date and time.
        - json: For parsing JSON data.
        - requests: For making HTTP requests.

    Example:
        >>> call_ticker_current("GOOGL")
        ['2023-08-01', {'ticker': 'GOOGL', 'currentOpen': 2759.12, 'currentHigh': 2780.00,
        'currentLow': 2740.10, 'currentVolume': 1248000, 'prevClose': 2745.98, 'currentPrice': 2768.99,
        'currentPercentageChange': '+0.85%'}]
    """
    from bs4 import BeautifulSoup
    import re
    import datetime
    import json

    finalData = [(str(datetime.datetime.now())[:10]), {}]
    finalData[1]["ticker"] = ticker

    response = requests.get(f"https://polygon.io/quote/{ticker}")

    if response.status_code == 200:
        responseContents = response.text
        soup = BeautifulSoup(responseContents, "html.parser")

        currentPriceElement = soup.find(
            "title"
        )  # the current price is found from the title of the webpage, along with percentage change from open
        if currentPriceElement:
            currentPriceRaw = currentPriceElement.text.strip()
            pattern = r"(-\d+\.\d{2}%|\+\d+\.\d{2}%) (\d+\.\d+)"  # first group is for the percentage, accounting for a +ve & -ve. second group for current price
            currentPercentageChange = re.search(pattern, currentPriceRaw).group(1)
            currentPriceValue = float(re.search(pattern, currentPriceRaw).group(2))

        data = soup.find(
            id="__NEXT_DATA__"
        ).text  # data is held within a json inside a script tag in the html
        data = json.loads(data)
        currentOpen = data["props"]["pageProps"]["open"]
        prevClose = data["props"]["pageProps"]["close"]
        currentHigh = data["props"]["pageProps"]["high"]
        currentLow = data["props"]["pageProps"]["low"]
        currentVolume = data["props"]["pageProps"]["volume"]

        finalData[1]["currentOpen"] = currentOpen
        finalData[1]["currentHigh"] = currentHigh
        finalData[1]["currentLow"] = currentLow
        finalData[1]["currentVolume"] = currentVolume
        finalData[1]["prevClose"] = prevClose
        finalData[1]["currentPrice"] = currentPriceValue
        finalData[1]["currentPercentageChange"] = currentPercentageChange

        return finalData

    else:
        raise NameError(f"Provided ticker yielded {response.status_code} response")


def cleanse_data(originalIn: list) -> list:
    for index, dictionary in enumerate(originalIn):
        if index == 0:
            continue
        del dictionary["l"]  # low
        del dictionary["n"]  # number of transactions
        del dictionary["t"]  # time in unix msec

        dictionary["ticker"] = dictionary.pop("T")
        dictionary["volume"] = dictionary.pop("v")
        dictionary["volumeWeighted"] = dictionary.pop("vw")
        dictionary["open"] = dictionary.pop("o")
        dictionary["close"] = dictionary.pop("c")
        dictionary["high"] = dictionary.pop("h")

    return originalIn


# a = cleanse_data(call_all_companies("2023-07-27"))
# print(call_ticker_current("GOOG"))
