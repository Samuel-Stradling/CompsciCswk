import sqlite3
from datetime import datetime, timedelta
import copy


class SortItems:
    """for dateRange it is a list, where the first item is the start date, and the second is the end date:
    [startdate, enddate]"""

    def __init__(
        self,
        sortMethod: str,
        sortMetric: str,
        startDate: str,
        endDate: str = str(datetime.today().date() - timedelta(days=1)),
    ):
        self.sortMethod = sortMethod
        self.startDate = startDate
        self.sortMetric = sortMetric
        self.endDate = endDate
        self.today = str(datetime.today().date())
        try:
            self.conn = sqlite3.connect("data\\main.sql")
            self.cursor = self.conn.cursor()
        except:
            raise ConnectionError("Unable to open database at the specified path")
        self.check_date_validity()
        self.select_values(self.select_dates())

    values = []

    def check_date_validity(self):
        if self.endDate == self.today:  # if the end date is set to the current date
            self.endDate = str((datetime.today() - timedelta(days=1)).date())
        elif not (
            datetime.strptime(self.startDate, "%Y-%m-%d")
            < datetime.strptime(self.endDate, "%Y-%m-%d") # start date must be before end date
            and datetime.strptime(self.endDate, "%Y-%m-%d")
            <= datetime.strptime(self.today, "%Y-%m-%d") # and end date must be before or equal to today
        ):
            raise ValueError("The entered dates were not valid")

    def select_dates(self):
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

    def select_values(self, dates):
        for date in dates:
            print(date)


sorter = SortItems("bubble", "price", "2023-08-29", "2023-09-05")
