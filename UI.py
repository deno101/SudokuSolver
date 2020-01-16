import tkinter as tk
import random


class Board(tk.Frame):
    grids = {}

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.createBoard()

    def getGrids(self):
        return self.grids

    def createBoard(self):
        self.configure(background="black")

        x, y = 0, 0
        ypadding = [2, 5]
        xpadding = [2, 5]
        for i in range(9):
            x = 0
            xp, yp = (0, 1), (0, 1)

            for x in range(9):
                xp, yp = (0, 1), (0, 1)

                self.grids[str(x)+str(y)] = tk.Label(self, text=str(random.randint(1, 9)), font=('Heveltica', 18,), width=2)

                if x in xpadding:
                    xp = (0, 3)

                if y in ypadding:
                    yp = (0, 3)
                if x == 0:
                    xp = (1, 3)
                self.grids[str(x) + str(y)].grid(column=y, row=x, padx=yp, pady=xp)
                x += 1

            y += 1
        self.pack()


class mainUI(Board):
    grids = {}
    root = tk.Tk()

    def __init__(self):
        Board.__init__(self, self.root)
        self.root.mainloop()


if __name__ == '__main__':
    mainUI()