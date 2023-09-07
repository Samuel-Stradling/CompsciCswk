import sqlite3


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
    import requests

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
            pattern = r"(-\d+\.\d{2}%|\+\d+\.\d{2}%) (\d+\.?\d+?)"  # first group is for the percentage, accounting for a +ve & -ve. second group for current price
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


# search for date and company


def search_by_date_and_company(company: str, date: str) -> float | dict:
    """
    Retrieve the close price of a company on a specific date, or the high and low for a company today.

    Parameters:
    - company (str): The ticker symbol of the company for which you want to retrieve the stock prices.
    - date (str): The date in the format 'yyyy-mm-dd' for which you want to retrieve the stock prices.

    Returns:
    - dictionary: A dictionary containing the high and low stock prices of the specified company on the provided date.
      The tuple format is (high_price, low_price). ONLY IF the date is the current date, otherwise:
    - float: A float holding the close price of the selected company on the selected date

    Raises:
    - ValueError: If the data is not available for the specified company on the provided date.
      This can occur if the market was closed on the given date or if data for the company is unavailable.

    Dependencies:
    - The 'datetime' module for obtaining the current date and time.
    - Access to a SQLite database named "data/main.sql" to fetch historical stock price data.
    - The 'sqlite3' module for accessing and searching the database
    - The 'call_ticker_current' function for accessing real time data

    Example:
    ```
    >>> search_by_date_and_company("AAPL", "2023-09-06")
    (150.29, 149.70)
    ```
    """

    from datetime import datetime

    today = str(datetime.now().date())

    if date == today:
        data = call_ticker_current(company)[1]
        return {"high": data["currentHigh"], "low": data["currentLow"]}
    try:
        conn = sqlite3.connect("data/main.sql")
        cursor = conn.cursor()
        cursor.execute(
            "SELECT close FROM StockPrices WHERE ticker = ? AND date = ?",
            (company, date),
        )
        result = cursor.fetchone()
        if result == None:
            raise ValueError(
                f"Data is not available for {company} on {date}. The market may have been closed, or data for that company is not available"
            )
        return float(result[0])

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


print(search_by_date_and_company("CSCO", "2023-09-06"))


def search_by_metrics():
    # these results need to be saved locally in txt
    pass


# search with metrics
