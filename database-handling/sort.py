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
            self.conn = sqlite3.connect("data/main.sql")
            self.cursor = self.conn.cursor()
        except:
            raise ConnectionError("Unable to open database at the specified path")

        self.__select_values(self.__select_dates())

    values = []

    def __check_sort_method(self):
        sortMethods = ["bubble", "merge", "quick", "heap"]
        if self.sortMethod.lower() not in sortMethods:
            raise ValueError("Invalid sort method")

    def __check_sort_metric(self):
        sortMetrics = ["high", "close", "open", "volume", "weighted_volume"]
        if self.sortMetric.lower() not in sortMetrics:
            raise ValueError("Invalid sort metric")

    def __check_date_validity(self):
        if self.endDate == self.today:  # if the end date is set to the current date
            self.endDate = str(
                (datetime.today() - timedelta(days=1)).date()
            )  # set end date to yesterday

        elif not (
            datetime.strptime(self.startDate, "%Y-%m-%d")
            < datetime.strptime(
                self.endDate, "%Y-%m-%d"
            )  # start date must be before end date
            and datetime.strptime(self.endDate, "%Y-%m-%d")
            <= datetime.strptime(
                self.today, "%Y-%m-%d"
            )  # and end date must be before or equal to today
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
        """Standard format:
        [
            {date:yyyy-mm-dd, ticker:aaaa, SORTMETRIC:...},
            {date:yyyy-mm-dd, ticker:aaaa, SORTMETRIC:...},
            ...
        ]
        Note: if market closed on a day, instead of a dictionary, a string "data not available for yyyy-mm-dd"

        """

        for date in dates:
            # this is done like this because I was not able to set variable select parameters
            if self.sortMetric == "open":
                self.cursor.execute(
                    "SELECT open, ticker FROM StockPrices WHERE date = ?", (date,)
                )

            elif self.sortMetric == "close":
                self.cursor.execute(
                    "SELECT close, ticker FROM StockPrices WHERE date = ?", (date,)
                )

            elif self.sortMetric == "high":
                self.cursor.execute(
                    "SELECT high, ticker FROM StockPrices WHERE date = ?", (date,)
                )

            elif self.sortMetric == "volume":
                self.cursor.execute(
                    "SELECT volume, ticker FROM StockPrices WHERE date = ?", (date,)
                )

            elif self.sortMetric == "weighted_volume":
                self.cursor.execute(
                    "SELECT weighted_volume, ticker FROM StockPrices WHERE date = ?",
                    (date,),
                )

            result = self.cursor.fetchall()
            count = 0
            if result == []:
                print(f"Data not available for {date}")
            while count < len(result):
                self.values.append(
                    {
                        "date": date,
                        "ticker": result[count][1],
                        self.sortMetric: result[count][0],
                    }
                )
                count += 1

        self.conn.commit()
        self.cursor.close()
        self.conn.close()

    def bubble_sort(self):
        # checker = sorted(self.values, key=lambda x: x[self.sortMetric])

        swapMade = True
        while swapMade:
            swapMade = False
            index = 0
            while index != len(self.values) - 1:
                if (
                    self.values[index][self.sortMetric]
                    > self.values[index + 1][self.sortMetric]
                ):
                    temp = self.values[index + 1]
                    self.values[index + 1] = self.values[index]
                    self.values[index] = temp
                    swapMade = True

                index += 1

        # if self.values == checker:
        #     print("worked")

    def merge_sort(self):
        """principle: adjacent sublists are merged in order, until there is only 1 ordered sublist."""

        def merge(lst: list, sortMetric: str) -> list:
            """merges two given sub lists in order size"""
            leftSubList = lst[0]
            rightSubList = lst[1]
            combinedLen = len(leftSubList) + len(rightSubList)
            newList = []
            while len(newList) != combinedLen:
                if len(leftSubList) == 0:
                    for remaining in rightSubList:
                        newList.append(remaining)
                    return newList
                if len(rightSubList) == 0:
                    for remaining in leftSubList:
                        newList.append(remaining)
                    return newList


                if leftSubList[0][sortMetric] < rightSubList[0][sortMetric]:
                    newList.append(leftSubList.pop(0))
                elif leftSubList[0][sortMetric] > rightSubList[0][sortMetric]:
                    newList.append(rightSubList.pop(0))
                elif leftSubList[0][sortMetric] == rightSubList[0][sortMetric]:
                    newList.append(leftSubList.pop(0))
                    newList.append(rightSubList.pop(0))

            return newList

        def controller(sortMetric, toBeSorted):


            newList =[]

            if len(toBeSorted) % 2 != 0:
                #odd number of items
                index = 0
                while not (len(newList) == len(toBeSorted)//2 + 1):
                    newList.append(merge([toBeSorted[index], toBeSorted[index+1]], sortMetric))
                    if index + 2 != len(toBeSorted) - 1:
                        #if end of list not reached
                        index += 2
                    else:
                        newList.append(toBeSorted[index+2]) #append the remaining value
                return newList

            else:
                # even values in list path
                index = 0
                while not (len(newList) == len(toBeSorted)/2):
                    newList.append(merge([toBeSorted[index], toBeSorted[index+1]], sortMetric))
                    if index + 2 != len(toBeSorted) - 1:
                        index += 2
                    else:
                        newList.append(toBeSorted[index+2])
                return newList

        values = [[x] for x in self.values]
        while len(values[0]) != len(self.values):
            values = controller(self.sortMetric, values)

        return values[0]




    
        

        

    def quick_sort(self):
        pass

    def heap_sort(self):
        pass


sorter = SortItems(
    sortMethod="bubble",
    sortMetric="high",
    startDate="2023-09-11",
    endDate="2023-09-13",
)
for value in sorter.merge_sort():
    print(value)


