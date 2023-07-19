import json
from companies import company_dictionary

def call_api(company: str, dateRange: int) -> json:
    import requests
    import os
    from dotenv import load_dotenv
    load_dotenv()
    api_key = os.environ.get("api-token")
    url = f'https://financialmodelingprep.com/api/v3/historical-price-full/{company}?timeseries={dateRange}&apikey={api_key}'
    return requests.get(url).json()

def cleanse_data(originalIn: json) -> json:
    dirtyData = originalIn.copy()

    # for key in dirtyData:
    #     print(key)

    del dirtyData["historical"]["open"]
    del dirtyData["high"]
    del dirtyData["low"]
    del dirtyData["unadjustedVolume"]
    del dirtyData["vwap"]
    del dirtyData["label"]
    del dirtyData["changeOverTime"]

    return dirtyData

a = cleanse_data(call_api("AAPL", 4))








