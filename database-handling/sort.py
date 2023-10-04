import sqlite3
from datetime import datetime, timedelta


class SortItems:
    """
    the double underscores infront of some methods means that they are private, and can only be accessed by the __init__ method
    single underscores mean protected attributes (viewable but not modifiable)
    """

    def __init__(
        self,
        startDate: str,
        sortMetric: str = "price",
        endDate: str = str(datetime.today().date() - timedelta(days=1)),
    ):
        self._startDate = startDate
        self._sortMetric = sortMetric
        self._endDate = endDate
        self._today = str(datetime.today().date())

        self.__check_date_validity()
        # self.__check_sort_method()
        self.__check_sort_metric()

        try:
            self.conn = sqlite3.connect("data/main.sql")
            self.cursor = self.conn.cursor()
        except:
            raise ConnectionError("Unable to open database at the specified path")

        self.__select_values(self.__select_dates())

    values = []
    
    @property
    def sortMetric(self):
        return self._sortMetric
    
    @property
    def startDate(self):
        return self._startDate
    
    @property
    def endDate(self):
        return self._endDate
    
    @property
    def today(self):
        return self._today
    
    def __write_results_to_file(self, data: list):
        import os
        FolderName = 'database-handling/sort-search-results'
        FileName = f"{self._today}-{self._sortMetric}.txt"

        folderPath = os.path.join(os.getcwd(), FolderName)


        filePath = os.path.join(folderPath, FileName)
        
        if os.path.exists(filePath):
            # Append a unique identifier to the filename
            file_base_name, file_extension = os.path.splitext(FileName)
            count = 1
            while os.path.exists(filePath):
                new_file_name = f"{file_base_name}{count}{file_extension}"
                filePath = os.path.join(folderPath, new_file_name)
                count += 1
                

        with open(filePath, 'w') as file:
            file.write(f"from {self._startDate} to {self._endDate}")
            file.write("\n\n")
            for item in data:
                file.write(str(item))
                file.write("\n")


    # def __check_sort_method(self):
    #     sortMethods = ["bubble", "merge", "quick", "heap"]
    #     if self._sortMethod.lower() not in sortMethods:
    #         raise ValueError("Invalid sort method")

    def __check_sort_metric(self):
        sortMetrics = ["high", "close", "open", "volume", "weighted_volume"]
        if self._sortMetric.lower() not in sortMetrics:
            raise ValueError("Invalid sort metric")

    def __check_date_validity(self):
        if self._endDate == self._today:  # if the end date is set to the current date
            self._endDate = str(
                (datetime.today() - timedelta(days=1)).date()
            )  # set end date to yesterday

        elif not (
            datetime.strptime(self._startDate, "%Y-%m-%d")
            < datetime.strptime(
                self._endDate, "%Y-%m-%d"
            )  # start date must be before end date
            and datetime.strptime(self._endDate, "%Y-%m-%d")
            <= datetime.strptime(
                self._today, "%Y-%m-%d"
            )  # and end date must be before or equal to today
        ):
            raise ValueError("The entered dates were not valid")

    def __select_dates(self):
        dates = []
        workingDate = (
            self._startDate
        )  # a copy of startDate is automatically made here, so no need for manual copy
        workingDate = datetime.strptime(workingDate, "%Y-%m-%d").date()
        while str(workingDate) != str(
            (datetime.strptime(self._endDate, "%Y-%m-%d") + timedelta(days=1)).date()
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
            if self._sortMetric == "open":
                self.cursor.execute(
                    "SELECT open, ticker FROM StockPrices WHERE date = ?", (date,)
                )

            elif self._sortMetric == "close":
                self.cursor.execute(
                    "SELECT close, ticker FROM StockPrices WHERE date = ?", (date,)
                )

            elif self._sortMetric == "high":
                self.cursor.execute(
                    "SELECT high, ticker FROM StockPrices WHERE date = ?", (date,)
                )

            elif self._sortMetric == "volume":
                self.cursor.execute(
                    "SELECT volume, ticker FROM StockPrices WHERE date = ?", (date,)
                )

            elif self._sortMetric == "weighted_volume":
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
                        self._sortMetric: result[count][0],
                    }
                )
                count += 1

        self.conn.commit()
        self.cursor.close()
        self.conn.close()

    def bubble_sort(self):
        # checker = sorted(self.values, key=lambda x: x[self._sortMetric])

        values = self.values[:]  # copy of self.values

        swapMade = True
        while swapMade:
            swapMade = False
            index = 0
            while index != len(values) - 1:
                if values[index][self._sortMetric] > values[index + 1][self._sortMetric]:
                    temp = values[index + 1]
                    values[index + 1] = values[index]
                    values[index] = temp
                    swapMade = True

                index += 1
        
        self.__write_results_to_file(values)
        return values

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
            newList = []

            if len(toBeSorted) % 2 != 0:
                # odd number of items
                index = 0
                while not (len(newList) == len(toBeSorted) // 2 + 1):
                    newList.append(
                        merge([toBeSorted[index], toBeSorted[index + 1]], sortMetric)
                    )
                    if index + 2 != len(toBeSorted) - 1:
                        # if end of list not reached
                        index += 2
                    else:
                        newList.append(
                            toBeSorted[index + 2]
                        )  # append the remaining value
                return newList

            else:
                # even values in list path
                index = 0
                while not (len(newList) == len(toBeSorted) / 2):
                    newList.append(
                        merge([toBeSorted[index], toBeSorted[index + 1]], sortMetric)
                    )
                    if index + 2 != len(toBeSorted) - 1:
                        index += 2
                    else:
                        newList.append(toBeSorted[index + 2])
                return newList

        values = [[x] for x in self.values]
        while len(values[0]) != len(self.values):
            values = controller(self._sortMetric, values)
        
        self.__write_results_to_file(values[0])
        return values[0]

    def quick_sort(self):
        # This will be added given enough time
        pass

    def heap_sort(self):
        # This will be added given enough time
        pass


sorter = SortItems(
    sortMetric="high",
    startDate="2023-09-11",
    endDate="2023-09-13",
)
sorter.bubble_sort()
sorter.merge_sort()

# for item in sorter.bubble_sort():
#     print(item)
# print(sorter.sortMethod)
# print(sorter.today)
# sorter.today = "test"
# sorter.sortMethod = "test"
