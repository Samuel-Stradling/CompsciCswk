import sqlite3

# this is an intialisation file. It is not very pleasant, but it gets the job done, and only really needs to be done once. This can be 
# considered more of a devtools file

def init_all():
    # creates database if doesn't exist
    conn = sqlite3.connect("data\main.sql")
    try:
        cursor = conn.cursor()

        # Create Companies
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS Companies (
                ticker TEXT PRIMARY KEY,
                name TEXT,
                sector TEXT,
                description TEXT,
                incorporation_year INTEGER
            )
        """
        )

        # Create Date Statuses
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS DateStatuses (
                date DATE PRIMARY KEY,
                complete_data BOOLEAN,
                market_open BOOLEAN
            )
        """
        )

        # Create Stock Prices
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS StockPrices (
                priceid INTEGER PRIMARY KEY,
                ticker TEXT,
                date DATE,
                open REAL,
                close REAL,
                high REAL,
                volume INTEGER,
                weighted_volume REAL,
                FOREIGN KEY (ticker) REFERENCES Companies (ticker),
                FOREIGN KEY (date) REFERENCES DateStatuses (date)
            )
        """
        )

        conn.commit()

    except sqlite3.Error as error:
        print("Error: {}".format(error))

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def fill_Companies_table():
    # hard coded 🤷‍♂️🤢
    from companyDict import company_dictionary

    try:
        conn = sqlite3.connect("data\main.sql")
        cursor = conn.cursor()

        # SQL query to insert data into the Companies table
        insert_query = "INSERT INTO Companies (ticker, name, sector, description, incorporation_year) VALUES (?, ?, ?, ?, ?)"

        # Loop through the dictionary and insert each company's information
        for ticker, company_info in company_dictionary.items():
            name, sector, description, incorporation_year = company_info
            data = (ticker, name, sector, description, incorporation_year)
            cursor.execute(insert_query, data)

        # Commit the changes to the database
        conn.commit()

        print("Data inserted successfully.")

    except sqlite3.Error as error:
        print("Error: {}".format(error))

    finally:
        # Close the cursor and connection
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def check_historic_data():
    import sys

    sys.path.insert(1, "C:\\Users\Sam\\Documents\\Programming\\CompsciCswk\\api\\")

    from dataHandling import call_all_companies

    print(call_all_companies("2021-08-13"))


def fill_dates_for_historic_data():
    with open("database-handling\\baselineDatesForInit.txt", "r") as dateFile:
        dates = list(reversed(dateFile.readlines()))
        dates = [date.strip() for date in dates]
        try:
            conn = sqlite3.connect("data\main.sql")
            cursor = conn.cursor()
            for date in dates:
                cursor.execute(
                    "INSERT INTO DateStatuses (date, complete_data, market_open) VALUES (?, ?, ?)",
                    (date, False, True),
                )
            conn.commit()

        except sqlite3.Error as error:
            print("Error: {}".format(error))

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()


fill_dates_for_historic_data()

# MAKE DATAHANDLING.PY INTO CLASS WITH TOOL METHODS???
