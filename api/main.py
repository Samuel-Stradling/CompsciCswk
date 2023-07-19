import requests
import json
import os
from dotenv import load_dotenv
from companies import company_dictionary
#
def get_data(companies: dict, dateRange:int):


    load_dotenv()
    api_key = os.environ.get("api-token")
    for company in companies:
        url = f'https://financialmodelingprep.com/api/v3/historical-price-full/{company}?timeseries={dateRange}&apikey={api_key}'
        print(requests.get(url).json())


    


def main():
    get_data(company_dictionary, 3)

if __name__ == "__main__":
    main()