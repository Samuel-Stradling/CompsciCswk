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
        self.endDate = endDate
        self.sortMetric = sortMetric
        try:
            self.conn = sqlite3.connect("data/main.sql")
            self.cursor = self.conn.cursor()
        except:
            raise ConnectionError("Unable to open database at the specified path")
        self.select_values(self.select_dates())

    values = []

    def select_dates(self):
        dates = []
        workingDate = self.startDate # a copy of startDate is automatically made here, so no need for manual copy
        workingDate = datetime.strptime(workingDate, "%Y-%m-%d").date()
        while str(workingDate) != self.endDate:
            dates.append(str(workingDate))
            workingDate = workingDate + timedelta(days=1)
        return dates
    
    def select_values(dates):
        pass




sorter = SortItems("bubble", "price", "2022-08-09", "2022-09-09")
