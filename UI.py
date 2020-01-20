import tkinter as tk
from pynput import keyboard
import sudoku

# Global var  kepping track of the currently clicked label
currentPressed = None

mode ={
    "edit": True,
    "Solve": False
}

normalColor = None

class Board(tk.Frame):

    def __init__(self, parent):
        self.grids = dict()
        self.originCol = None

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

                l = tk.Label(self, text="", font=('Heveltica', 18,), width=2)

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

                l.grid(column=y, row=x, padx=yp, pady=xp)
                l.__name__ = (str(x) + str(y))
                l.bind("<Button-1>", lambda e, widget=l: self.onclick(e, widget))

                self.grids[l.__name__] = l

                x += 1

            y += 1
        self.originCol = l.cget("background")
        self.pack(pady=(8, 0))

    def onclick(self, event, widget):
        global currentPressed, normalColor

        normalColor = self.originCol
        if not currentPressed == None:
            currentPressed.config(bg=self.originCol)
        widget.config(bg="yellow")
        currentPressed = widget


class Command(tk.Frame):
    editBtn = None
    solveBtn = None
    clearBtn = None

    def __init__(self, parent, Super):
        tk.Frame.__init__(self, parent)
        self.Super = Super
        self.createWidgets()

    def createWidgets(self):
        self.editBtn = tk.Button(self, text="Edit", command=self.editMode)
        self.solveBtn = tk.Button(self, text="Solve", command=self.solve)
        self.clearBtn = tk.Button(self, text="Clear", command=self.clear)

        self.editBtn.grid(row=0, column=0, padx=5, pady=8)
        self.solveBtn.grid(row=0, column=1, padx=5, pady=8)
        self.clearBtn.grid(row=0, column=2, padx=5, pady=8)

        self.pack()

    def editMode(self):
        global mode

        mode["edit"] = True

    def clear(self):
        global currentPressed, normalColor

        for key in self.Super.grids:
            self.Super.grids[key].config(text="")
            self.editMode()

        currentPressed.config(background=normalColor)

    def solve(self):
        global currentPressed, normalColor

        currentPressed.config(background=normalColor)
        rawPuzzle = self.getBoard(self.Super.grids)

        sudoku.Solver(rawPuzzle, self.Super)

    def getBoard(self, grid):
        array = []

        for y in range(0, 9, 1):
            temp = []
            for x in range(0, 9, 1):
                key = str(y) + str(x)

                value = grid[key].cget("text")
                if value == "":
                    value = 0
                value = int(value)

                temp.append(value)

            array.append(temp)
        return array


class Listener:

    def __init__(self, Super):
        self.keyboardLs()
        self.Super = Super

    def onPress(self, key):
        global currentPressed, mode

        try:
            if int(key.char) in [1, 2, 3, 4, 5, 6, 7, 8, 9] and mode["edit"]:

                self.change(currentPressed, key.char)
            else:
                self.Super.change("invalid input")
        except ValueError:
            self.Super.changeText("invalid input")
        except AttributeError:
            self.Super.changeText("invalid input")

    def onRelease(self, key):
        pass

    def keyboardLs(self):
        listener = keyboard.Listener(
            on_press=self.onPress,
            on_release=self.onRelease,
        )

        listener.start()

    def change(self, widget, text):
        if not widget == None:
            widget.config(text=text)
            self.Super.changeText("")
        else:
            self.Super.changeText("Click on grid location first")


class mainUI(Board, Command, Listener):
    grids = {}
    root = tk.Tk()
    statusBar = None

    def __init__(self):
        self.root.title("Sudoku")
        self.root.resizable(0, 0)
        self.root.geometry("500x400")

        Board.__init__(self, self.root)
        Command.__init__(self, self.root, self)

        # create status bar
        self.statusBar = tk.Label(self.root, width=500, text="Welcome", borderwidth=2, relief="sunken", anchor="w", height=5)
        self.statusBar.pack()

        Listener.__init__(self, self)

        self.grids = self.getGrids()

        self.root.mainloop()

    # function to change text in status bar
    def changeText(self, text=""):
        self.statusBar.config(text=text)

    def showChanges(self, cordinates, value):
        target = self.grids[cordinates]

        target.config(background="blue")
        target.config(text=value)


if __name__ == '__main__':
    mainUI()