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
        if subDictionary["T"] in company_dictionary:
            companySortedData.append(subDictionary)
        counter += 1

    return companySortedData


def call_ticker(ticker: str, date: str):
    # this will need web-scraping from: https://polygon.io/quote/{ticker}
    response = requests.get("https://polygon.io/quote/AAPL").text
    print(response)


def cleanse_data(originalIn: list) -> list:
    for index, dictionary in enumerate(originalIn):
        if index == 0:
            continue
        del dictionary["l"]
        del dictionary["n"]
        del dictionary["t"]

    return originalIn


# a = cleanse_data(call_all_companies("2023-07-27"))
call_ticker("a", 1)