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
    """
    @Board => creates the 9X9 sudoku board
    """
    def __init__(self, parent):
        self.grids = dict()
        self.originCol = None

        tk.Frame.__init__(self, parent)
        self.createBoard()

    def getGrids(self):
        # return all the labels in a dict
        return self.grids

    def createBoard(self):
        # creates the actual sudoku board
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
                l.bind("<Button-1>", lambda e, widget=l, xc=x, yc=y: self.onclick(e, widget, xc, yc))

                self.grids[l.__name__] = l

                x += 1

            y += 1
        self.originCol = l.cget("background")
        self.pack(pady=(8, 0))

    def onclick(self, event, widget, x, y):
        # onclick listener for all the labels
        global currentPressed, normalColor

        normalColor = self.originCol
        if not currentPressed == None:
            currentPressed[0].config(bg=self.originCol)
        widget.config(bg="yellow")
        currentPressed = [widget, x, y]


class Command(tk.Frame):
    editBtn = None
    solveBtn = None
    clearBtn = None
    loadBtn = None
    saveBtn = None
    """
        @Command => Create all command buttons,
                    handle all button click functionality
    """
    def __init__(self, parent, Super):
        tk.Frame.__init__(self, parent)
        self.Super = Super
        self.createWidgets()

    def createWidgets(self):
        """ Create all button widgets"""

        self.editBtn = tk.Button(self, text="Edit", command=self.editMode)
        self.solveBtn = tk.Button(self, text="Solve", command=self.solve)
        self.clearBtn = tk.Button(self, text="Clear", command=self.clear)
        self.saveBtn = tk.Button(self, text="Save", command=self.save)
        self.loadBtn = tk.Button(self, text="Load", command=self.load)

        self.editBtn.grid(row=0, column=0, padx=5, pady=8)
        self.solveBtn.grid(row=0, column=1, padx=5, pady=8)
        self.clearBtn.grid(row=0, column=2, padx=5, pady=8)
        self.saveBtn.grid(row=0, column=3, padx=5, pady=8)
        self.loadBtn.grid(row=0, column=4, padx=5, pady=8)

        self.pack()

    def editMode(self):
        # when edit button is pressed
        global mode

        mode["edit"] = True

    def clear(self):
        # when clear button is pressed
        global currentPressed, normalColor

        for key in self.Super.grids:
            self.Super.grids[key].config(text="")
            self.Super.grids[key].config(background=normalColor)
            self.editMode()

    def solve(self):
        # when solve button is pressed
        global currentPressed, normalColor

        if currentPressed is not None:
            currentPressed[0].config(background=normalColor)

        rawPuzzle = self.getBoard(self.Super.grids)
        sudoku.Solver(rawPuzzle, self.Super)

    def getBoard(self, grid):
        # get the  numbers in the board when solve os clicked
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

    def load(self):
        pass

    def save(self):
        pass

class Listener:
    """
        @Listener -- contains all the code for keyboard press events
    """
    def __init__(self, Super):
        self.keyboardLs()
        self.Super = Super

    def onPress(self, key):
        global currentPressed, mode

        # listen for special keys up, down, left, right, del
        try:
            if key == key.up:
                self.Super.moveUp()
                return
            elif key == key.right:
                self.Super.moveRight()
                return
            elif key == key.left:
                self.Super.moveLeft()
                return
            elif key == key.down:
                self.Super.moveDown()
                return
            elif key == key.delete:
                self.Super.delete()
                return
        except AttributeError:
            pass

        try:
            if int(key.char) in [1, 2, 3, 4, 5, 6, 7, 8, 9] and mode["edit"]:

                self.change(currentPressed[0], key.char)
                self.Super.changeText("")
            else:
                self.Super.changeText("invalid input")
        except ValueError:
            self.Super.changeText("invalid input")
        except AttributeError:
            self.Super.changeText("invalid input")

    def onRelease(self, key):
        pass

    # start the keyboard listener
    def keyboardLs(self):
        listener = keyboard.Listener(
            on_press=self.onPress,
            on_release=self.onRelease,
        )

        listener.start()

    # Changes the text on the currently clicked label
    def change(self, widget, text):
        if widget is not None:
            widget.config(text=text)
            self.Super.changeText("")
        else:
            self.Super.changeText("Click on grid location first")


class mainUI:
    grids = {}
    root = tk.Tk()
    statusBar = None

    def __init__(self):
        self.root.title("Sudoku")
        self.root.resizable(0, 0)
        self.root.geometry("500x400")

        board = Board(self.root)
        Command(self.root, self)

        # create status bar
        self.statusBar = tk.Label(self.root, width=500, text="Welcome", borderwidth=2, relief="sunken", anchor="w", height=5)
        self.statusBar.pack()

        Listener(self)

        self.grids = board.getGrids()

        self.root.mainloop()

    # function to change text in status bar
    def changeText(self, text=""):
        self.statusBar.config(text=text)

    def showChanges(self, cordinates, value):
        target = self.grids[cordinates]

        target.config(background="blue")
        target.config(text=value)

    def moveRight(self):
        global currentPressed, normalColor

        if normalColor is None:
            normalColor = self.grids['88'].cget('background')

        if currentPressed is not None:
            currentPressed[0].config(background=normalColor)

            x, y = currentPressed[1], currentPressed[2]
            self.changeText("")
            if y == 8:
                self.changeText("Invalid move")
                currentPressed[0].config(bg="yellow")
                return

            y += 1
            currentPressed = [self.grids[str(x) + str(y)], x, y]
            currentPressed[0].config(bg="yellow")
        else:
            currentPressed = [self.grids['00'], 0, 0]
            currentPressed[0].config(bg="yellow")

    def moveLeft(self):
        global currentPressed, normalColor

        if normalColor is None:
            normalColor = self.grids['88'].cget('background')

        if currentPressed is not None:
            currentPressed[0].config(background=normalColor)

            x, y = currentPressed[1], currentPressed[2]
            self.changeText("")
            if y == 0:
                self.changeText("Invalid move")
                currentPressed[0].config(bg="yellow")
                return

            y -= 1
            currentPressed = [self.grids[str(x) + str(y)], x, y]
            currentPressed[0].config(bg="yellow")
        else:
            currentPressed = [self.grids['00'], 0, 0]
            currentPressed[0].config(bg="yellow")

    def moveDown(self):
        global currentPressed, normalColor
        if normalColor is None:
            normalColor = self.grids['88'].cget('background')

        if currentPressed is not None:
            currentPressed[0].config(background=normalColor)

            x, y = currentPressed[1], currentPressed[2]
            self.changeText("")
            if x == 8:
                self.changeText("Invalid move")
                currentPressed[0].config(bg="yellow")
                return

            x += 1
            currentPressed = [self.grids[str(x) + str(y)], x, y]
            currentPressed[0].config(bg="yellow")
        else:
            currentPressed = [self.grids['00'], 0, 0]
            currentPressed[0].config(bg="yellow")

    def moveUp(self):
        global currentPressed, normalColor
        if normalColor is None:
            normalColor = self.grids['88'].cget('background')

        if currentPressed is not None:
            currentPressed[0].config(background=normalColor)

            x, y = currentPressed[1], currentPressed[2]
            self.changeText("")
            if x == 0:
                self.changeText("Invalid move")
                currentPressed[0].config(bg="yellow")
                return

            x -= 1
            currentPressed = [self.grids[str(x) + str(y)], x, y]
            currentPressed[0].config(bg="yellow")
        else:
            currentPressed = [self.grids['00'], 0, 0]
            currentPressed[0].config(bg="yellow")

    def delete(self):
        global currentPressed, normalColor
        if currentPressed is not None:
            currentPressed[0].config(text="")


if __name__ == '__main__':
    mainUI()
