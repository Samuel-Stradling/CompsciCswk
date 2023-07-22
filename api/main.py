import json

def call_api(company: str, dateRange: int) -> json:
    """Data comes back as dictionary
    Dictionary has two master keys: symbol, and historical
    The historical key contains {dateRange} arrays, each with keys such as date, open
    close, change"""
    import requests
    import os
    from dotenv import load_dotenv
    load_dotenv()
    api_key = os.environ.get("api-token")
    url = f'https://financialmodelingprep.com/api/v3/historical-price-full/{company}?timeseries={dateRange}&apikey={api_key}'
    return requests.get(url).json()

def cleanse_data(originalIn: json) -> json:
    dirtyData = originalIn.copy()

    for dictionary in dirtyData["historical"]:
        del dictionary["open"]
        del dictionary["high"]
        del dictionary["low"]
        del dictionary["unadjustedVolume"]
        del dictionary["vwap"]
        del dictionary["label"]
        del dictionary["changeOverTime"]

    return dirtyData


if __name__ == "__main__":
    a = cleanse_data(call_api("AAPL", 2))








