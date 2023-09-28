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
    """
    Adds missing dates to the 'DateStatuses' table in the database.

    This function calculates the missing dates between the latest date recorded in
    the 'DateStatuses' table and yesterday's date. It then inserts records for these
    missing dates with default values into the table.

    Parameters:
        None

    Raises:
        sqlite3.Error: If there is an error while executing the database query.

    Dependencies:
        - The function requires the 'datetime' and 'sqlite3' modules.
        - Assumes a connection to an SQLite database named "main.sql" stored with a local path of "data/main.sql"

    Note:
        - This function assumes that the 'DateStatuses' table has columns 'date',
          'complete_data', and 'market_open'.

    Example:
        >>> add_missing_dates_to_database()
        # Adds missing dates between the latest recorded date and yesterday's date to the database.
    """

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
    Finds the last date with a full set of data from the database.

    Parameters:
        None

    Returns:
        str: The last date with a full set of data in the format 'YYYY-MM-DD',
             or None if no data is found.

    Raises:
        sqlite3.Error: If there is an error while executing the database query.

    Dependencies:
        - Assumes a connection to an SQLite database named "main.sql" stored with a local path of "data/main.sql"
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
    """
    Inserts data returned from call_all_companies into the stockprices table.

    This function takes a list of dictionaries containing stock price data for multiple
    companies and inserts this data into a SQLite database table named 'StockPrices'.

    Parameters:
        data (list): A list of dictionaries containing stock price data for each company in the following format: ['2023-08-20', {...company_data...}, {...company_data...}, ...]

    Returns:
        None.

    Raises:
        sqlite3.Error: If there is an error while executing the database insertion query.

    Dependencies:
        - Assumes a connection to an SQLite database named "main.sql" stored with a local path of "data/main.sql"
    """
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
    Updates the date status table based on the stock prices table.

    This function checks the number of entries for a given date in the StockPrices table
    and updates the DateStatuses table accordingly. If the count is greater than or equal
    to 90, it sets the 'complete_data' field to True. Otherwise, it sets the 'market_open'
    field to False.

    Parameters:
        date (str): The date for which to update the status in the DateStatuses table.

    Returns:
        None

    Raises:
        sqlite3.Error: If there is an error while working with the SQLite database.

    Dependencies:
        - This function requires the sqlite3 library to be imported.

    Note:
        - The list of companies stored is not always available in the data, but the function
          still operates based on the count of entries.

    Example:
        update_date_statuses("2023-08-21")
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


def backfill(lastFullDate: str) -> int:
    """
    Controls the backfilling process for stock data.

    This function uses all of the other functions in autoBackfill.py, and essentially acts as a master controller function, actually responsible
    for corroborating all of the data into all of the right places

    Parameters:
        lastFullDate (str): The most recent date with a full set of data.

    Returns:
        int: The count of dates processed and accounted for during the backfill.
    
    Raises:
        ValueError: when the length of the query returned from the api is 0, indicating that the market was closed. This exception is caught and handled.

    Dependencies:
        - This function uses the 'time' and 'datetime' modules.
        - This function uses the 'add_missing_dates' procedure.

    Example:
        backfill("2023-08-19")
        backfill(find_last_full_date())
    """
    import time
    from datetime import timedelta, datetime

    add_missing_dates()

    yesterday = datetime.now() - timedelta(days=1)

    if lastFullDate != yesterday:
        datesToFill = []
        startDate = (
            datetime.strptime(lastFullDate, "%Y-%m-%d") + timedelta(days=1)
        ).date() # the last full date has data, hence the start date is one day after the last full date
        yesterday = yesterday.date()

        currentDate = startDate
        while currentDate != yesterday:
            datesToFill.append(str(currentDate))
            currentDate += timedelta(days=1)
        datesToFill.append(str(yesterday))
    
    count = 0

    for date in datesToFill:
        try:
            time.sleep(12) # the free api plan stipulates a max of 5 calls per min. This ensures that the limit is never possibly exceeded

            data = call_all_companies(date)

            print("item count:", len(data) - 1) # prints number of companies returned (the -1 is because the first value of data is the date)

            insert_data_into_stockprices(data) # inserts the data into the stockprices table

            update_date_statuses(date) # updates the dateStatuses table accordingly

            print(date, "\n") # prints date to indicate that it is accounted for
            count += 1

        except ValueError: # this is raised from call_all_companies, and happens when the length of the query returned from the api is 0 = the market was closed
            update_date_statuses(date) # the dateStatuses table is updated accordingly
            print(date)# prints date to indicate that it is accounted for
            count += 1 
    return count

backfill(find_last_full_date())
