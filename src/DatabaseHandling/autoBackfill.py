import sqlite3


def call_all_companies(date: str) -> list:
    """
    Retrieves data about companies from the Polygon API based on the given date.

    Parameters:
        date (str): The date in the format 'yyyy-mm-dd' for which data is requested.

    Returns:
        list: A list containing the date (element 0) and relevant company data as dictionaries (subsequent elements are dictionaries).

    Raises:
        ConnectionError: if the API call fails or returns an error.
        ValueError: Raised when the market was closed on the specified date.

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
    from DatabaseHandling.companies import company_dictionary

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
    while counter < len(
        rawData["results"]
    ):  # raw data is a json where the value of the results key is a list of dictionaries, each holding data for distinct companies, hence this cleansing
        subDictionary = rawData["results"][counter]
        if (
            subDictionary["T"] in company_dictionary
        ):  # rawData contains many more companies then we need hence...
            companySortedData.append(subDictionary)
        counter += 1

    return companySortedData


def add_missing_dates():
    from datetime import datetime, timedelta

    yesterday = (datetime.now() - timedelta(days=1)).date()

    try:
        conn = sqlite3.connect("data/main.sql")
        cursor = conn.cursor()
        cursor.execute("SELECT MAX(date) AS latestDate FROM DateStatuses")
        latestDate = datetime.strptime(
            cursor.fetchone()[0], "%Y-%m-%d"
        ).date()  # converts string to datetime

        if latestDate != yesterday:
            workingDate = latestDate + timedelta(
                days=1
            )  # latest date is already full, so we need to start from the next date along
            while workingDate <= yesterday:
                cursor.execute(
                    "INSERT INTO DateStatuses (date, complete_data, market_open) VALUES (?, ?, ?)",
                    (
                        str(workingDate),
                        False,
                        True,
                    ),  # default values for new dates is always False for complete_data, and True for market_open
                )
                workingDate += timedelta(days=1)
            conn.commit()

    except sqlite3.Error as error:
        print("Error: {}".format(error))

    finally:
        # Close the cursor and connection
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def find_last_full_date() -> str:
    """
    Ensures that all dates from the latest recorded date in the 'DateStatuses' table
    up to yesterday are present, filling in missing dates with default values.

    Parameters:
    None

    Returns:
    None

    Raises:
    sqlite3.Error: If there is an error while connecting to or querying the SQLite database.

    Dependencies:
    - sqlite3
    - datetime
    - timedelta

    Note:
    This function assumes the existence of an SQLite database named 'data/main.sql' and a table
    named 'DateStatuses' with columns 'date', 'complete_data', and 'market_open'.

    Example Use:
    add_missing_dates()
    """
    try:
        conn = sqlite3.connect("data/main.sql")
        cursor = conn.cursor()
        cursor.execute(
            "SELECT MAX(date) AS oldestCompleteDate FROM DateStatuses WHERE complete_data = true;"
        )
        result = cursor.fetchone()

        if result[0] == None:
            cursor.execute(
                "SELECT MIN(date) AS oldestCompleteDate FROM DateStatuses"
            )  # if the datestatuses table has been initialised but not updated (remember by default complete_data is false so its possible that no results are yielded from the query)
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
    try:
        conn = sqlite3.connect("data/main.sql")
        cursor = conn.cursor()
        date = data[0]
        for company in data:
            if company == date:
                continue
            insertArgs = (
                company["T"],
                date,
                company["o"],  # open
                company["c"],  # close
                company["h"],  # high
                company["v"],  # volume traded
                company["vw"],  # weighted volume
            )
            cursor.execute(
                "INSERT INTO StockPrices (ticker, date, open, close, high, volume, weighted_volume) VALUES (?, ?, ?, ?, ?, ?, ?)",
                insertArgs,
            )
            conn.commit()

    except sqlite3.Error as error:
        print("Error: {}".format(error))

    finally:
        # Close the cursor and connection
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def update_date_statuses(date: str):
    """
    Inserts stock price data into the 'StockPrices' table in the SQLite database.

    Parameters:
    - data (list): A list of dictionaries containing stock price information for multiple companies.

    Returns:
    None

    Raises:
    sqlite3.Error: If there is an error while connecting to or querying the SQLite database.

    Dependencies:
    - sqlite3

    Note:
    This function assumes the existence of an SQLite database named 'data/main.sql' and a table
    named 'StockPrices' with columns 'ticker', 'date', 'open', 'close', 'high', 'volume', and 'weighted_volume'.

    Example Use:
    insert_data_into_stockprices(data)
    """

    try:
        conn = sqlite3.connect("data/main.sql")
        cursor = conn.cursor()

        cursor.execute(
            "SELECT COUNT(*) FROM StockPrices WHERE date = ?", (date,)
        )  # select number of entries for a particular date
        count = cursor.fetchone()[0]
        if (
            count >= 90
        ):  # note that the list of companies stored is not always available in the data, however we only drop to 97 companies returned from 101
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

    finally:
        # Close the cursor and connection
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def backfill(lastFullDate: str):
    """
    Backfills missing data for dates starting from the last fully updated date to yesterday.

    Parameters:
    - lastFullDate (str): The last fully updated date in the format "%Y-%m-%d".

    Returns:
    None

    Raises:
    ValueError: If there is an issue with the value returned from 'call_all_companies'.

    Dependencies:
    - time
    - datetime
    - timedelta
    - add_missing_dates
    - call_all_companies
    - insert_data_into_stockprices
    - update_date_statuses

    Note:
    This function relies on external functions 'add_missing_dates', 'call_all_companies',
    'insert_data_into_stockprices', and 'update_date_statuses'. It also uses a sleep duration of
    12 seconds to comply with the rate limits of the free API plan.

    Example Use:
    backfill("2023-01-01")
    """
    import time
    from datetime import timedelta, datetime

    add_missing_dates()

    yesterday = datetime.now() - timedelta(days=1)

    if lastFullDate != str(yesterday.date()):
        datesToFill = []
        startDate = (
            datetime.strptime(lastFullDate, "%Y-%m-%d") + timedelta(days=1)
        ).date()  # the last full date has data, hence the start date is one day after the last full date
        yesterday = yesterday.date()

        currentDate = startDate
        while currentDate != yesterday:
            datesToFill.append(str(currentDate))
            currentDate += timedelta(days=1)
        datesToFill.append(str(yesterday))
    else:
        print("Already up to date")
        return

    for date in datesToFill:
        try:
            time.sleep(
                12
            )  # the free api plan stipulates a max of 5 calls per min. This ensures that the limit is never possibly exceeded

            data = call_all_companies(date)

            print(
                "item count:", len(data) - 1
            )  # prints number of companies returned (the -1 is because the first value of data is the date)

            insert_data_into_stockprices(
                data
            )  # inserts the data into the stockprices table

            update_date_statuses(date)  # updates the dateStatuses table accordingly

            print(date, "\n")  # prints date to indicate that it is accounted for

        except (
            ValueError
        ):  # this is raised from call_all_companies, and happens when the length of the query returned from the api is 0 = the market was closed
            update_date_statuses(date)  # the dateStatuses table is updated accordingly
            print(date, "\n")  # prints date to indicate that it is accounted for


# backfill(find_last_full_date())
