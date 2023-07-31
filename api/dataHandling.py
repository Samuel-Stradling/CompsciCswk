import json


def call_api(date: int) -> json:
    """date is yyyy-mm-dd"""

    import requests
    import os
    from dotenv import load_dotenv

    load_dotenv()
    api_key = os.environ.get("api-token")

    url = f"https://api.polygon.io/v2/aggs/grouped/locale/us/market/stocks/{date}?adjusted=true&apiKey={api_key}"

    data = requests.get(url).json()
    return data


def cleanse_data(originalIn: json) -> json:
    from companies import company_dictionary

    i = 0
    sortedData = []
    while i < len(originalIn["results"]):
        diction = originalIn["results"][i]
        if diction["T"] in company_dictionary:
            sortedData.append(diction)
        i += 1
    print(len(sortedData))
    return sortedData


# data = call_api(company_dictionary, 1)

# with open("out.json", "w") as jsonFile:
#     json.dump(data, jsonFile, indent=4)
