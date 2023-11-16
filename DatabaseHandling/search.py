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
        return {
            "high": data["currentHigh"],
            "low": data["currentLow"],
            "currentPrice": data["currentPrice"],
            "currentPercentageChange": data["currentPercentageChange"],
            "currentVolume": data["currentVolume"],
            "open": data["currentOpen"]
        }
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


def search_by_metrics():
    # these results need to be saved locally in txt

    # LOW PRIORITY

    # metrics to search by:
    #     Stock Price Metrics:

    # Closing Price: Allow users to search for companies based on their closing stock prices on specific dates.
    # Opening Price: Similar to closing price but for the opening price.
    # High and Low Prices: Users can search for companies based on the highest and lowest stock prices on specific dates.
    # Volume: Provide the ability to search for companies based on their trading volume on specific dates.
    # Market Capitalization Metrics:

    # Market Cap: Users can search for companies based on their market capitalization, which is the total market value of their outstanding shares.
    # Financial Ratios:

    # Price-to-Earnings (P/E) Ratio: Allow users to search for companies with specific P/E ratios, which can indicate a company's valuation relative to its earnings.
    # Price-to-Sales (P/S) Ratio: Similar to P/E ratio but based on revenue.
    # Price-to-Book (P/B) Ratio: Indicate a company's valuation relative to its book value.
    # Dividend Yield: Users can search for companies with specific dividend yields, which is the dividend income relative to the stock price.
    # Performance Metrics:

    # Return on Investment (ROI): Users may want to search for companies based on their historical ROI over specific periods.
    # Earnings per Share (EPS): Allow users to search for companies with specific EPS values.
    # Revenue Growth: Provide the ability to search for companies based on their revenue growth rates.
    # Market Index Metrics:

    # Comparison to Market Indices: Users can search for companies that outperformed or underperformed market indices like the S&P 500.
    # Technical Indicators:

    # Moving Averages: Allow users to search for companies that have recently crossed specific moving average lines.
    # Relative Strength Index (RSI): Users can search for companies based on their RSI values, indicating overbought or oversold conditions.
    # Volatility Metrics:

    # Historical Volatility: Users may want to search for companies with specific historical volatility levels.
    # Implied Volatility: Search for companies with specific implied volatility levels for options trading.
    # Fundamental Metrics:

    # Debt-to-Equity Ratio: Users can search for companies with specific debt-to-equity ratios, indicating their financial leverage.
    # Profit Margin: Allow users to search for companies with specific profit margin percentages.
    # Dividend Metrics:

    # Dividend History: Users can search for companies with specific dividend payment histories or dividend growth rates.
    # Economic Indicators:

    # Interest Rates: Allow users to search for companies in specific interest rate environments.
    # Sector and Industry Metrics:

    # Sector Performance: Users can search for companies within specific sectors or industries.
    # Industry Metrics: Provide industry-specific metrics such as same-store sales growth for retail companies.
    # Custom Metrics:

    # Allow users to define custom metrics or combinations of metrics to search for companies that meet their specific criteria.
    # Adding these metrics to your search functionality will make your finance app more versatile and useful for a wide range of investors and traders who have different investment strategies and preferences.
    pass


# search with metrics
