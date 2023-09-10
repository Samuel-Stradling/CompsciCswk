import sqlite3
from datetime import datetime, timedelta


class SortItems:
    """for dateRange it is a list, where the first item is the start date, and the second is the end date:
    [startdate, enddate]
    
    the double underscores infront of some methods means that they are private, and can only be accessed by the __init__ method
    """

    def __init__(
        self,
        startDate: str,
        sortMethod: str = "bubble",
        sortMetric: str = "price",
        endDate: str = str(datetime.today().date() - timedelta(days=1)),
    ):
        
        self.sortMethod = sortMethod
        self.startDate = startDate
        self.sortMetric = sortMetric
        self.endDate = endDate
        self.today = str(datetime.today().date())

        self.__check_date_validity()
        self.__check_sort_method()
        self.__check_sort_metric()

        try:
            self.conn = sqlite3.connect("data\\main.sql")
            self.cursor = self.conn.cursor()
        except:
            raise ConnectionError("Unable to open database at the specified path")
        
        self.__select_values(self.__select_dates())

    values = []

    def __check_sort_method(self):
        sortMethods = ["bubble", "merge", "quick", "heap"]
        if self.sortMethod.lower() not in sortMethods: raise ValueError("Invalid sort method")

    def __check_sort_metric(self):
        sortMetrics = ["price", "high", "close", "open", "volume", "weighted_volume"]
        if self.sortMetric.lower() not in sortMetrics: raise ValueError("Invalid sort metric")

    def __check_date_validity(self):
        if self.endDate == self.today:  # if the end date is set to the current date
            self.endDate = str((datetime.today() - timedelta(days=1)).date())

        elif not (
            datetime.strptime(self.startDate, "%Y-%m-%d")
            < datetime.strptime(self.endDate, "%Y-%m-%d") # start date must be before end date
            and datetime.strptime(self.endDate, "%Y-%m-%d")
            <= datetime.strptime(self.today, "%Y-%m-%d") # and end date must be before or equal to today
        ):
            raise ValueError("The entered dates were not valid")

    def __select_dates(self):
        dates = []
        workingDate = (
            self.startDate
        )  # a copy of startDate is automatically made here, so no need for manual copy
        workingDate = datetime.strptime(workingDate, "%Y-%m-%d").date()
        while str(workingDate) != str(
            (datetime.strptime(self.endDate, "%Y-%m-%d") + timedelta(days=1)).date()
        ):
            dates.append(str(workingDate))
            workingDate = workingDate + timedelta(days=1)
        return dates

    def __select_values(self, dates):
        for date in dates:
            self.conn.execute("SELECT ")

            self.values.append({"date": date, "ticker": ticker, self.sortMetric: valueToSortBy })





        self.conn.commit()


        self.cursor.close()
        self.conn.close()


sorter = SortItems(sortMethod="bubble", sortMetric="price", startDate="2023-08-29", endDate="2023-09-05")
