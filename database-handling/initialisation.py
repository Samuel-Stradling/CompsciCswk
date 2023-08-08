import sqlite3


def init_all():
    # creates database if doesn't exist
    conn = sqlite3.connect("data\main.sql")
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
    conn.close()


def fill_Companies_table():
    # this will require some manual input, to fill the companies info table
    pass


def add_historic_data():
    # this will be very complex
    pass


init_all()

# MAKE DATAHANDLING.PY INTO CLASS WITH TOOL METHODS???
