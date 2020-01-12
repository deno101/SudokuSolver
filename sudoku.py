#!/usr/bin/env python3

dataSet = [
    [0, 6, 4 ,0, 0, 0, 7, 5, 0],
    [9, 0, 0, 0, 4, 3, 6, 8, 1],
    [1, 0, 7, 9, 0, 0, 2, 0, 3],

    [0, 0, 1, 6, 2, 0, 0, 0, 0],
    [0, 0, 6, 0, 0, 0, 8, 0, 0],
    [0, 0, 0, 0, 7, 5, 1, 0, 0],

    [6, 0, 9, 0, 0, 4, 5, 0, 8],
    [8, 1, 3, 5, 9, 0, 0, 0, 2],
    [0, 4, 5, 0, 0, 0, 9, 3, 0]
]


class Solver:

    missing = []
    rowData = []
    columnData = []

    def __init__(self):
        self.main()
        print(self.missing)

    # args = 2d array representing 3x3 cell
    # return all missing values for a 3x3 cell
    def getMissing(self, array):
        complete = {1, 2, 3, 4, 5, 6, 7, 8, 9}
        set1 = set()

        for x in array:
            for y in x:
                if not y == 0:
                    set1.add(y)

        # largerSet.difference(smallerSet)
        return complete.difference(set1)

    def main(self):

        countx = 0
        county = 0

        # loop through all 9 cells
        for i in range(9):
            array = []
            for k in range(3):
                temp = []
                for j in range(countx, countx + 3, 1):
                    temp.append(dataSet[county][j])

                array.append(temp)
                county += 1


            if county > 8:
                county = 0
                countx += 3

            # misssind => array containing set of all missing nubers in a 3x3 cell
            self.missing.append(self.getMissing(array))

    '''
        function divides data into 1d lists containing all 9x9 rows and columns
        making it easy for searching
        
        populates global vars rowData, columnData
    '''
    def cleanData(self):
        self.rowData = dataSet

        for y in range(0, 9, 1):
            temp = []
            for x in range(0, 9, 1):
                temp.append(dataSet[x][y])
            self.columnData.append(temp)

    def posibility(self):
        pass

    def populate(self, target, value):
        pass


if __name__=="__main__":
    Solver()
