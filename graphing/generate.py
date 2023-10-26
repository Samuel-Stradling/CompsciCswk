def check_dates(startDate: str, endDate: str):
    """
    Check the validity of input dates and raise errors where applicable.

    Parameters:
    - startDate (str): The start date in the format "YYYY-MM-DD".
    - endDate (str): The end date in the format "YYYY-MM-DD".

    Returns:
        Does not return anything.

    Raises:
    - ValueError: If any of the following conditions are met:
      - The start date is before the year 2020.
      - Either the start date or end date is not in the format "YYYY-MM-DD".
      - The start date is after the end date.
      - The end date is after the current date.

    Dependencies:
    - This function depends on the 'datetime' and 'timedelta' classes from the 'datetime' module.

    Note:
    - This function should be run before any other functions using the dates, to ensure that they are able
    to work as intended (i.e. with valid dates)
    """
    from datetime import datetime, timedelta

    today = str(datetime.today().date())
    if endDate == today:
        endDate = str((datetime.today() - timedelta(days=1)).date())

    if int(startDate[:4]) < 2020:
        raise ValueError("Invalid start date")

    try:
        a = datetime.strptime(startDate, "%Y-%m-%d")
        b = datetime.strptime(endDate, "%Y-%m-%d")
    except:
        raise ValueError("Incorrect date format")

    if not (
        datetime.strptime(startDate, "%Y-%m-%d")
        < datetime.strptime(endDate, "%Y-%m-%d")  # start date must be before end date
        and datetime.strptime(endDate, "%Y-%m-%d")
        <= datetime.strptime(today, "%Y-%m-%d")
    ):
        raise ValueError("The entered dates were not valid")


def get_data(startDate: str, endDate: str, *companies: str) -> tuple:
    """
    Retrieve stock price data for a variable number of companies (1 or more) within a date range.

    Parameters:
    - startDate (str): The start date in the format "YYYY-MM-DD".
    - endDate (str): The end date in the format "YYYY-MM-DD".
    - *companies (str): Variable-length argument list of company ticker symbols.

    Returns:
    - tuple: A tuple containing the following elements respectively:
      - data (pd.DataFrame): A DataFrame containing stock price data for the specified companies within the date range.
      - startDate (str): The provided start date.
      - endDate (str): The provided end date.

    Raises:
    - sqlite3.Error: If there is an error while connecting to the SQLite database or executing the SQL query.

    Dependencies:
    - This function depends on the 'pandas' library and 'sqlite3' module for database operations.

    Example:
    ```python
    data, start_date, end_date = get_data("2023-01-01", "2023-01-05", "AAPL", "GOOGL", "MSFT")
    print(data)
    print(start_date)
    print(end_date)
    # Output: DataFrame with stock price data, '2023-01-01', '2023-01-05'
    ```

    Note:
    - This function retrieves stock price data for specified companies within the given date range by querying an SQLite database. It returns a tuple containing the data, start date, and end date. An example of how to use the function is provided.
    """
    import pandas as pd
    import sqlite3

    try:
        conn = sqlite3.connect("data/main.sql")

        query = f"""
            SELECT date, close, ticker
            FROM StockPrices
            WHERE date >= '{startDate}' AND date <= '{endDate}'
            AND ticker IN ({','.join([f"'{c}'" for c in companies])})
        """

        # Execute the query and fetch the results into a DataFrame
        data = pd.read_sql_query(query, conn)

    except sqlite3.Error as error:
        print("Error: {}".format(error))

    finally:
        conn.close()

    return (data, startDate, endDate)


def generate_candlestick(startDate, endDate, *companies):
    """not possible unfortunately due to previous ommital of 'low' from data. Foolish"""
    pass
    # import pandas as pd
    # import sqlite3
    # import plotly.graph_objects as go
    # import plotly.express as px

    # try:
    #     conn = sqlite3.connect("data/main.sql")

    #     query = f"""
    #         SELECT date, high, open, close, ticker
    #         FROM StockPrices
    #         WHERE date >= '{startDate}' AND date <= '{endDate}'
    #         AND ticker IN ({','.join([f"'{c}'" for c in companies])})
    #     """

    #     # Execute the query and fetch the results into a DataFrame
    #     data = pd.read_sql_query(query, conn)

    # except sqlite3.Error as error:
    #     print("Error: {}".format(error))

    # finally:
    #     conn.close()

    # fig = go.Figure(data=[go.Candlestick(x=data['date'], open=data['open'], high=data['high'], low=['low'], close=data['close'])])
    # fig.update_layout(title=f"{', '.join(companies)}'s price from {startDate} to {endDate}", xaxis_title='Date', yaxis_title='Price in USD')
    # fig.show()


def generate_graph(data: tuple, graphType: str):
    """
    Generate and display a plotly graph based on stock price data.

    Parameters:
    - data (tuple): A tuple containing stock price data, start date, and end date.
    - graphType (str): The type of graph to generate ("bar" or "line").

    Returns:
    - None

    Raises:
    - ValueError: If an unsupported 'graphType' is provided.

    Dependencies:
    - This function depends on the 'plotly.express' library for graph generation.

    Example:
    ```python
    generate_graph((data, "2023-01-01", "2023-01-05"), "line")
    ```

    Note:
    - This function generates and displays a plotly graph based on stock price data. 
    The 'data' parameter should be a tuple containing stock price data in the form of a DataFrame, along with the start and end date. 
    The 'graphType' specifies whether to generate a bar or line graph. An example of how to use the function is provided.
    - The graph is opened with localhost on the default browser. Here, an image of the graph at a specific point can be saved.
    """
    import plotly.express as px

    startDate = data[1]
    endDate = data[2]
    data = data[0]
    companies = data["ticker"].unique()

    if graphType == "bar":
        fig = px.bar(
            data,
            x="date",
            y="close",
            color="ticker",
            title=f"{', '.join(companies)}'s price from {startDate} to {endDate}",
        )
    elif graphType == "line":
        fig = px.line(
            data,
            x="date",
            y="close",
            color="ticker",
            title=f"{', '.join(companies)}'s price from {startDate} to {endDate}",
        )
    else:
        raise ValueError(
            "Unsupported graphType. Supported graph types are 'bar', 'line'"
        )

    fig.update_xaxes(title_text="Date")
    fig.update_yaxes(title_text="Price in USD")
    fig.show()


generate_graph(get_data("2022-09-19", "2023-10-20", "AAPL"), "line")
