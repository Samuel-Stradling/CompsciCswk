# The raw data from the api follows this format: {key:value, key:value, results:[ticker:"APPL", ...]}

# The cleansed data is as follows: [date, {ticker:"AAPL", ...}]


import requests


def call_all_companies(date: str) -> list:
    """date is yyyy-mm-dd"""

    import os
    from dotenv import load_dotenv
    from companies import company_dictionary

    load_dotenv()
    api_key = os.environ.get("api-token")

    url = f"https://api.polygon.io/v2/aggs/grouped/locale/us/market/stocks/{date}?adjusted=true&apiKey={api_key}"

    rawData = requests.get(url).json()

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
print(call_ticker_current("GOOG"))
