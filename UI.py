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

                self.grids[str(x)+str(y)] = tk.Label(self, text="", font=('Heveltica', 18,), width=2)

                # give extra padding after every 3 rows or colums
                if x in xpadding:
                    xp = (0, 3)

                if y in ypadding:
                    yp = (0, 3)

                # create separation for top most row and first column=left
                if x == 0:
                    xp = (1, 1)

                if y == 0:
                    yp = (1, 1)

                self.grids[(str(x) + str(y))].grid(column=y, row=x, padx=yp, pady=xp)
                x += 1

            y += 1
        self.pack(pady=(8, 0))


class Command(tk.Frame):
    editBtn = None
    solveBtn = None
    clearBtn = None

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.createWidgets()

    def createWidgets(self):
        self.editBtn = tk.Button(self, text="Edit")
        self.solveBtn = tk.Button(self, text="Solve")
        self.clearBtn = tk.Button(self, text="Clear")

        self.editBtn.grid(row=0, column=0, padx=5, pady=8)
        self.solveBtn.grid(row=0, column=1, padx=5, pady=8)
        self.clearBtn.grid(row=0, column=2, padx=5, pady=8)

        self.pack()


class mainUI(Board, Command):
    grids = {}
    root = tk.Tk()

    def __init__(self):
        self.root.title("Sudoku")
        self.root.resizable(0, 0)
        self.root.geometry("500x400")

        Board.__init__(self, self.root)
        Command.__init__(self, self.root)

        # create status bar
        statusBar = tk.Label(self.root, width=500, text="Welcome", borderwidth=2, relief="sunken", anchor="w", height=5)
        statusBar.pack()

        self.grids = self.getGrids()

        self.root.mainloop()


if __name__ == '__main__':
    mainUI()