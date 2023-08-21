import sqlite3


def call_all_companies(date: str) -> list:
    """
    Fetches aggregated financial data for selected companies from the Polygon API and returns a list.

    This function retrieves historical aggregated financial data for specific companies
    based on the provided date. The function utilizes the Polygon API to gather data
    on stock prices, volumes, and other metrics.

    Parameters:
        date (str): The date for which financial data is to be fetched in the 'YYYY-MM-DD' format.

    Returns:
        list: A list containing financial data for the specified date. The first element
        in the list is the input date, followed by dictionaries containing aggregated data
        for selected companies. Each dictionary includes information such as stock symbol,
        stock prices, volumes, and other relevant metrics.

    Raises:
        ConnectionError: If the API request to Polygon fails with a non-200 status code.
        ValueError: If no data is available for the provided date or if the market was closed.

    Dependencies:
        - This function requires the 'os', 'requests', 'dotenv', and 'companies' (this is a local module containing a dictionary of all of the stored companies and their acronyms) modules.
        - The API token should be set as an environment variable named "api-token" using dotenv.

    Example:
        >>> call_all_companies("2023-08-20")
        ['2023-08-20', {...company_data...}, {...company_data...}, ...]
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
        raise ConnectionError(f"Request failed with status code {rawData.status_code}")

    rawData = rawData.json()

    if rawData["queryCount"] == 0:
        raise ValueError(f"The market was closed on {date}")

    counter = 0
    companySortedData = [date]
    while counter < len(rawData["results"]): # raw data is a json where the value of the results key is a list of dictionaries, each holding data for distinct companies, hence this cleansing
        subDictionary = rawData["results"][counter]
        if (
            subDictionary["T"] in company_dictionary
        ):  # rawData contains many more companies then we need hence...
            companySortedData.append(subDictionary)
        counter += 1

    return companySortedData


def add_missing_dates() -> int:
    """adds missing dates to the datestatuses table in the database"""
    from datetime import datetime, timedelta

    yesterday = (datetime.now() - timedelta(days=1)).date()

    try:
        conn = sqlite3.connect("data\main.sql")
        cursor = conn.cursor()
        cursor.execute("SELECT MAX(date) AS latestDate FROM DateStatuses")
        latestDate = datetime.strptime(cursor.fetchone()[0], "%Y-%m-%d").date()

        if latestDate != yesterday:
            workingDate = latestDate + timedelta(days=1)
            while workingDate <= yesterday:
                cursor.execute(
                    "INSERT INTO DateStatuses (date, complete_data, market_open) VALUES (?, ?, ?)",
                    (str(workingDate), False, True),
                )
                workingDate += timedelta(days=1)
            conn.commit()

    except sqlite3.Error as error:
        print("Error: {}".format(error))
        return -1

    finally:
        # Close the cursor and connection
        if cursor:
            cursor.close()
        if conn:
            conn.close()
        return 0


def find_last_full_date() -> str:
    """finds the last date with a full set of data"""
    try:
        conn = sqlite3.connect("data\main.sql")
        cursor = conn.cursor()
        cursor.execute(
            "SELECT MAX(date) AS oldestCompleteDate FROM DateStatuses WHERE complete_data = true;"
        )
        result = cursor.fetchone()

        if result[0] == None:
            cursor.execute("SELECT MIN(date) AS oldestCompleteDate FROM DateStatuses")
            result = cursor.fetchone()

    except sqlite3.Error as error:
        print("Error: {}".format(error))

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
        return result[0]


def insert_data_into_stockprices(data: list):
    """inserts data returned from call_all_companies into the stockprices table"""
    try:
        conn = sqlite3.connect("data\main.sql")
        cursor = conn.cursor()
        date = data[0]
        for company in data:
            if company == date:
                continue
            insertArgs = (
                company["T"],
                date,
                company["o"],
                company["c"],
                company["h"],
                company["v"],
                company["vw"],
            )
            cursor.execute(
                "INSERT INTO StockPrices (ticker, date, open, close, high, volume, weighted_volume) VALUES (?, ?, ?, ?, ?, ?, ?)",
                insertArgs,
            )
            conn.commit()

    except sqlite3.Error as error:
        print("Error: {}".format(error))
        return -1

    finally:
        # Close the cursor and connection
        if cursor:
            cursor.close()
        if conn:
            conn.close()
        return 0


def update_date_statuses(date: str):
    """updates the date status table based on the stockprices table"""
    try:
        conn = sqlite3.connect("data\main.sql")
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM StockPrices WHERE date = ?", (date,))
        count = cursor.fetchone()[0]
        if count >= 90:  # IDK WHY SOME OF THE RESPONSES DO NOT HAVE ALL COMPANIES??
            cursor.execute(
                "UPDATE DateStatuses SET complete_data = ? WHERE date = ?", (True, date)
            )
        else:
            cursor.execute(
                "UPDATE DateStatuses SET market_open = ? WHERE date = ?", (False, date)
            )

        conn.commit()

    except sqlite3.Error as error:
        print("Error: {}".format(error))
        return -1

    finally:
        # Close the cursor and connection
        if cursor:
            cursor.close()
        if conn:
            conn.close()
        return 0


def backfill(lastFullDate: str) -> int:
    """responsible for controlling all of the backfilling"""
    import time
    from datetime import timedelta, datetime

    yesterday = datetime.now() - timedelta(days=1)

    if lastFullDate != yesterday:
        datesToFill = []
        startDate = (
            datetime.strptime(lastFullDate, "%Y-%m-%d") + timedelta(days=1)
        ).date()
        yesterday = (datetime.now() - timedelta(days=1)).date()

        currentDate = startDate
        while currentDate != yesterday:
            datesToFill.append(str(currentDate))
            currentDate += timedelta(days=1)
        datesToFill.append(str(yesterday))

    for date in datesToFill:
        try:
            time.sleep(12)
            data = call_all_companies(date)
            print("item count:", len(data) - 1)
            insert_data_into_stockprices(data)
            update_date_statuses(date)
            print(date)
        except ValueError:
            update_date_statuses(date)
            print(date)


add_missing_dates()
backfill(find_last_full_date())
# backfill("2023-08-17")
# insert_data_into_stockprices(call_all_companies("2023-08-17"))
# update_date_statuses("2023-08-17")


# add_missing_dates()
