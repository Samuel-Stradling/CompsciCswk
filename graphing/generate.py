# import plotly.express as px
# fig = px.bar(x=["a", "b", "c"], y=[1, 3, 2])
# fig.show()

# fig.write_image("graphing/graphs/fig1.svg")


# given a date range and company and graph type, show stock price against time
def get_dates(startDate: str, endDate: str) -> list:
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

    dates = []
    workingDate = startDate
    workingDate = datetime.strptime(workingDate, "%Y-%m-%d").date()
    while str(workingDate) <= str(endDate):
        dates.append(str(workingDate))
        workingDate = workingDate + timedelta(days=1)
    return dates


def get_data(dates: list, company: str) -> list:
    import sqlite3

    try:
        conn = sqlite3.connect("data/main.sql")
        cursor = conn.cursor()

        data = []

        for date in dates:
            cursor.execute(
                "SELECT close FROM StockPrices WHERE date = ? AND ticker = ?",
                (date, company),
            )
            result = cursor.fetchall()
            if result != []:  # if data available
                data.append({"date": date, "price": result[0][0]})

    except sqlite3.Error as error:
        print("Error: {}".format(error))
    finally:
        # Close the cursor and connection
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    return data


def generate_graph(
    data: list,
    graphType: str,
):
    pass


# given a number of companies and graph type, show stock prices against time

print(get_data(get_dates("2022-09-19", "2022-09-26"), "AAPL"))
