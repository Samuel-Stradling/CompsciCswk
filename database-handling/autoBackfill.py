import sqlite3


def call_all_companies(date: str) -> list:
    """
    Retrieves data about companies from an API based on the given date.

    Parameters:
        date (str): The date in the format 'yyyy-mm-dd' for which data is requested.

    Returns:
        list: A list containing the date (element 0) and relevant company data as dictionaries (subsequent elements are dictionaries).

    Raises:
        Exception: if the API call fails or returns an error
        ValueError: 'manually' raised for later use in the initialisation of the db

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
    import requests
    from dotenv import load_dotenv
    from companies import company_dictionary

    load_dotenv()
    api_key = os.environ.get("api-token")

    url = f"https://api.polygon.io/v2/aggs/grouped/locale/us/market/stocks/{date}?adjusted=true&apiKey={api_key}"

    rawData = requests.get(url)
    if rawData.status_code != 200:
        raise ValueError(f"Request failed with status code {rawData.status_code})")

    rawData = rawData.json()

    if rawData["queryCount"] == 0:
        raise ValueError(f"The market was closed on {date}")

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


def find_last_full_date() -> str:
    try:
        conn = sqlite3.connect("data\main.sql")
        cursor = conn.cursor()
        cursor.execute(
            "SELECT MIN(date) AS oldestCompleteDate FROM DateStatuses WHERE complete_data = true;"
        )
        result = cursor.fetchone()
        
        if result[0] == None:
            cursor.execute("SELECT MIN(date) AS oldestCompleteDate FROM DateStatuses")
            result = cursor.fetchone()

        print(result)

    except sqlite3.Error as error:
        print("Error: {}".format(error))

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def backfill(lastFullDate: str) -> int:
    pass


find_last_full_date()
