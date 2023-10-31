import sqlite3


class Generate:
    def __init__(self, startDate: str, endDate: str, *companies):
        self._startDate = startDate
        self._endDate = endDate
        self._companies = companies
        self._data = None

        self.__check_dates()

        self.__get_data()

    def __check_dates(self):
        from datetime import datetime, timedelta

        today = str(datetime.today().date())
        if self._endDate == today:
            self._endDate = str((datetime.today() - timedelta(days=1)).date())

        if int(self._startDate[:4]) < 2020:
            raise ValueError("Invalid start date")

        try:
            a = datetime.strptime(self._startDate, "%Y-%m-%d")
            b = datetime.strptime(self._endDate, "%Y-%m-%d")
        except:
            raise ValueError("Incorrect date format")

        if not (
            datetime.strptime(self._startDate, "%Y-%m-%d")
            < datetime.strptime(
                self._endDate, "%Y-%m-%d"
            )  # start date must be before end date
            and datetime.strptime(self._endDate, "%Y-%m-%d")
            <= datetime.strptime(today, "%Y-%m-%d")
        ):
            raise ValueError("The entered dates were not valid")

    def __get_data(self):
        import pandas as pd

        try:
            conn = sqlite3.connect("data/main.sql")

            query = f"""
                SELECT date, close, ticker
                FROM StockPrices
                WHERE date >= '{self._startDate}' AND date <= '{self._endDate}'
                AND ticker IN ({','.join([f"'{c}'" for c in self._companies])})
            """

            # Execute the query and fetch the results into a DataFrame
            self._data = pd.read_sql_query(query, conn)

        except sqlite3.Error as error:
            print("Error: {}".format(error))

        finally:
            conn.close()

    def __get_company_name_from_ticker(self, ticker):
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

    def generate_line_graph(self, displayOnSameGraph=True):
        import plotly.express as px

        companies = self._data["ticker"].unique()
        companiesFullNames = [
            self.__get_company_name_from_ticker(x).replace(".", "") for x in companies
        ]

        if displayOnSameGraph:
            fig = px.line(
                self._data,
                x="date",
                y="close",
                color="ticker",
                title=f"{', '.join(companiesFullNames)}'s prices from {self._startDate} to {self._endDate}",
            )
            fig.update_xaxes(title_text="Date")
            fig.update_yaxes(title_text="Price in USD")
            fig.show()

        else:  # if not display on same graph
            for company in companies:
                filteredData = self._data[
                    self._data["ticker"] == company
                ]  # filter dataframe to only get for specific company

                fig = px.line(
                    filteredData,
                    x="date",
                    y="close",
                    color="ticker",
                    title=f"{self.__get_company_name_from_ticker(company).replace('.', '')}'s prices from {self._startDate} to {self._endDate}",
                )
                fig.update_xaxes(title_text="Date")
                fig.update_yaxes(title_text="Price in USD")
                fig.show()

    def generate_bar_graph(self, displayOnSameGraph=True):
        import plotly.express as px

        companies = self._data["ticker"].unique()
        companiesFullNames = [
            self.__get_company_name_from_ticker(x).replace(".", "") for x in companies
        ]

        if displayOnSameGraph:
            fig = px.bar(
                self._data,
                x="date",
                y="close",
                color="ticker",
                title=f"{', '.join(companiesFullNames)}'s prices from {self._startDate} to {self._endDate}",
            )
            fig.update_xaxes(title_text="Date")
            fig.update_yaxes(title_text="Price in USD")
            fig.show()

        else:  # if not display on same graph
            for company in companies:
                filteredData = self._data[
                    self._data["ticker"] == company
                ]  # filter dataframe to only get for specific company

                fig = px.bar(
                    filteredData,
                    x="date",
                    y="close",
                    color="ticker",
                    title=f"{self.__get_company_name_from_ticker(company).replace('.', '')}'s prices from {self._startDate} to {self._endDate}",
                )
                fig.update_xaxes(title_text="Date")
                fig.update_yaxes(title_text="Price in USD")
                fig.show()

    def generate_candlestick_graph(self, displayOnSameGraph=True):
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


gen1 = Generate("2022-09-09", "2023-09-28", "AAPL", "CSCO", "GOOG")
gen1.generate_bar_graph(False)
