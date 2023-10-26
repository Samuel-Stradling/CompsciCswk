import sqlite3


def check_dates(startDate: str, endDate: str):
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

    return (startDate, endDate)


def get_data(dates: tuple, *companies: str) -> tuple:
    import pandas as pd

    startDate = dates[0]
    endDate = dates[1]

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


def get_company_name_from_ticker(ticker: str) -> str:
    """Helper function to get the company name of tickers, so that they can be displayed on the title of the graph"""
    try:
        conn = sqlite3.connect("data/main.sql")
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM Companies where ticker = ?", (ticker,))
        result = cursor.fetchall()
        return result[0][0]

    except sqlite3.Error as error:
        print("Error: {}".format(error))

    finally:
        # Close the cursor and connection
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def generate_graph(data: tuple, graphType: str, displayOnSameGraph: bool = True):
    import plotly.express as px

    startDate = data[1]
    endDate = data[2]
    data = data[0]
    companies = data["ticker"].unique()
    companiesFullNames = [
        get_company_name_from_ticker(x).replace(".", "") for x in companies
    ]

    if displayOnSameGraph:
        if graphType == "bar":
            fig = px.bar(
                data,  # use entire data frame for one plot
                x="date",
                y="close",
                color="ticker",
                title=f"{', '.join(companiesFullNames)}'s prices from {startDate} to {endDate}",
            )
            fig.update_xaxes(title_text="Date")
            fig.update_yaxes(title_text="Price in USD")
            fig.show()
        elif graphType == "line":
            fig = px.line(
                data,
                x="date",
                y="close",
                color="ticker",
                title=f"{', '.join(companiesFullNames)}'s prices from {startDate} to {endDate}",
            )
            fig.update_xaxes(title_text="Date")
            fig.update_yaxes(title_text="Price in USD")
            fig.show()
        else:
            raise ValueError(
                "Unsupported graphType. Supported graph types are 'bar', 'line'"
            )
    else:  # if not display on same graph
        for company in companies:
            filteredData = data[
                data["ticker"] == company
            ]  # filter dataframe to only get for specific company
            if graphType == "bar":
                fig = px.bar(
                    filteredData,
                    x="date",
                    y="close",
                    color="ticker",
                    title=f"{get_company_name_from_ticker(company).replace('.', '')}'s prices from {startDate} to {endDate}",
                )
            elif graphType == "line":
                fig = px.line(
                    filteredData,
                    x="date",
                    y="close",
                    color="ticker",
                    title=f"{get_company_name_from_ticker(company).replace('.', '')}'s prices from {startDate} to {endDate}",
                )
            fig.update_xaxes(title_text="Date")
            fig.update_yaxes(title_text="Price in USD")
            fig.show()


generate_graph(
    get_data(
        check_dates("2022-09-19", "2023-10-21"), "AAPL", "PYPL", "XEL", "TXN", "CRWD"
    ),
    "line",
    displayOnSameGraph=False,
)
