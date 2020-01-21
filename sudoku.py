#!/usr/bin/env python3

dataSet = [
    [6, 0, 0, 3, 0, 0, 0, 0, 0],
    [3, 1, 5, 2, 0, 8, 0, 0, 6],
    [0, 9, 0, 0, 6, 0, 0, 3, 0],

    [0, 0, 0, 0, 8, 0, 6, 0, 0],
    [9, 0, 0, 0, 0, 0, 0, 0, 2],
    [0, 0, 1, 0, 4, 0, 0, 0, 0],

    [0, 6, 0, 0, 2, 0, 0, 8, 0],
    [2, 0, 0, 9, 0, 6, 5, 4, 1],
    [0, 0, 0, 0, 0, 4, 0, 6, 3]
]

dataSet2 = [
    [1, 9, 0, 0, 7, 6, 0, 0, 5],
    [4, 0, 0, 0, 1, 9, 0, 3, 7],
    [5, 0, 3, 0, 0, 2, 0, 0, 0],

    [0, 2, 1, 0, 0, 0, 5, 0, 6],
    [8, 0, 4, 0, 0, 0, 7, 0, 2],
    [7, 0, 6, 0, 0, 0, 3, 9, 0],

    [0, 0, 0, 9, 0, 0, 8, 0, 4],
    [2, 8, 0, 4, 6, 0, 0, 0, 3],
    [3, 0, 0, 2, 8, 0, 0, 7, 9]
]


class Solver:

    def __init__(self, rawPuzzle, mainUI):

        self.mainUI = mainUI
        self.missing = []
        self.rowData = []
        self.columnData = []
        self.rawPuzzle = rawPuzzle
        self.cellData  = []

        self.currentCell = None
        self.ischange = False
        self.helperMissing()
        self.cleanData()

        self.recursion()

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

    def helperMissing(self):
        countx = 0
        county = 0

        # loop through all 9 cells
        for i in range(9):
            array = []
            cell = []
            for k in range(3):
                temp = []
                for j in range(countx, countx + 3, 1):
                    temp.append(self.rawPuzzle[county][j])
                    cell.append(self.rawPuzzle[county][j])
                array.append(temp)
                county += 1

            if county > 8:
                county = 0
                countx += 3

            # missing => array containing set of all missing numbers in a 3x3 cell
            self.missing.append(self.getMissing(array))
            self.cellData.append(cell)

    # try to solve the puzzle using recursion
    # for very simple soduku puzzle
    def recursion(self):
        self.ischange = False

        # check if the puzzle is valid before starting solve
        print
        if (self.isValid(self.cellData)) and (self.isValid(self.rowData)) and (self.isValid(self.columnData)):
            posy = 0
            self.currentMissing(0, 0)
            for x in self.rawPuzzle:
                posx = 0
                count = 1
                for i in x:
                    self.currentMissing(posx, posy)
                    if i == 0:
                        self.posibility(posx, posy)

                    posx += 1
                    count += 1

                posy += 1
                self.currentMissing(posx, posy)

            if self.ischange:
                self.columnData = []
                self.cleanData()
                self.recursion()
            else:
                self.mainUI.changeText("Complete")
        else:
            self.mainUI.changeText("Invalid puzzle")

    '''
        function divides data into 1d lists containing all 9x9 rows and columns
        making it easy for searching
        
        populates global vars rowData, columnData
    '''
    def cleanData(self):
        self.rowData = self.rawPuzzle

        for y in range(0, 9, 1):
            temp = []
            for x in range(0, 9, 1):
                temp.append(self.rawPuzzle[x][y])
            self.columnData.append(temp)

    def isValid(self, ls):
        for y in ls:
            for x in y:
                if y.count(x) > 1 and not x == 0:
                    return False

        return True

    def posibility(self, x, y):
        temp = self.currentCell[0].copy()

        for i in self.currentCell[0]:
            if i in self.rowData[y]:
                temp.remove(i)
            elif i in self.columnData[x]:
                temp.remove(i)

        if len(temp) == 1:
            self.populate(x, y, list(temp)[0])

    def populate(self, x, y, value):
        self.rawPuzzle[y][x] = value
        self.mainUI.showChanges((str(y)+str(x)), value)
        self.ischange = True
        self.missing[self.currentCell[1]].remove(value)

    # Stupid logic
    def currentMissing(self, x, y):
        if x <= 2 and y <= 2:
            self.currentCell = (self.missing[0], 0)

        elif x <= 2 and y <= 5:
            self.currentCell = (self.missing[1], 1)

        elif x <= 2 and y <= 8:
            self.currentCell = (self.missing[2], 2)

        elif x <= 5 and y <= 2:
            self.currentCell = (self.missing[3], 3)

        elif x <= 5 and y <= 5:
            self.currentCell = (self.missing[4], 4)

        elif x <= 5 and y <= 8:
            self.currentCell = (self.missing[5], 5)

        elif x <= 8 and y <= 2:
            self.currentCell = (self.missing[6], 6)

        elif x <= 8and y <= 5:
            self.currentCell = (self.missing[7], 7)

        elif x <= 8 and y <= 8:
            self.currentCell = (self.missing[8], 8)

