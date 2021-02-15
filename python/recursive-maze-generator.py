from tkinter import *
from random import *
from time import sleep

master = Tk()
master.title('Maze Generator (using Recursive Backtracking Algorithm)')

ROWS = 40
COLS = 40
HEIGHT = 800       # max: 800
WIDTH = 800         # max: 1425
UPDATE_INT = 0.001   # changes 'fps' :)
BG = "white"
CELL_OUTLINE = "blue"
CELL_LINE_WIDTH = 2

CELLH, CELLW = HEIGHT / ROWS, WIDTH / COLS

global playerx, playery
playerx, playery = 0, 0

global process
process = False


class Stack:
    items = []

    def push(self, element):
        self.items.append(element)

    def pop(self):
        if self.items != []:
            return self.items.pop(-1)
        else:
            return None

class Player:

    def __init__(self, cell, canvas, height, width, board):
        self.cell = cell
        self.c = canvas
        self.obj = self.c.create_oval(width*cell.getY()+3, height*cell.getX()+3, (width*cell.getY())+width-3, (height*cell.getX())+height-3, fill="red")
        self.board = board
        self.height = height
        self.width = width

    def render(self):
        x, y = self.cell.getX(), self.cell.getY()
        self.c.coords(self.obj, [(self.width*y)+3, (self.height*x)+3, (self.width*(y+1))-3, (self.height*(x+1))-3])

        #print("MOVING TO: (" + str(self.width*self.cell.getY()) + ", " + str(self.height*self.cell.getX()) + ")")
        #print("CELL: (" + str(x) + ", " + str(y) + ")")


    def move(self, dir):
        if dir == "up":
            self.cell = self.board[self.cell.getX() - 1][self.cell.getY()]
        if dir == "down":
            self.cell = self.board[self.cell.getX() + 1][self.cell.getY()]
        if dir == "left":
            self.cell = self.board[self.cell.getX()][self.cell.getY() - 1]
        if dir == "right":
            self.cell = self.board[self.cell.getX()][self.cell.getY() + 1]

        self.render()




class Cell:
    def __init__(self, isUp, isDown, isLeft, isRight, isVisited, isInStack, x, y, width, height):
        self.isUpWall = isUp
        self.isDownWall = isDown
        self.isLeftWall = isLeft
        self.isRightWall = isRight
        self.isVisited = isVisited
        self.isInStack = isInStack
        self.x = x
        self.y = y
        self.w = width
        self.h = height

    def setIsUpWall(self, isUp):
        self.isUpWall = isUp

    def getIsUpWall(self):
        return self.isUpWall

    def setIsDownWall(self, isDown):
        self.isDownWall = isDown

    def getIsDownWall(self):
        return self.isDownWall

    def setIsLeftWall(self, isLeft):
        self.isLeftWall = isLeft

    def getIsLeftWall(self):
        return self.isLeftWall

    def setIsRightWall(self, isRight):
        self.isRightWall = isRight

    def getIsRightWall(self):
        return self.isRightWall

    def setIsVisited(self, isVisited):
        self.isVisited = isVisited

    def getIsVisited(self):
        return self.isVisited

    def setIsInStack(self, isInStack):
        self.isInStack = isInStack

    def getIsInStack(self):
        return self.isInStack

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def fillPlayer(self):
        canvas.create_oval((self.w * self.x) + 3, (self.h * self.y) + 3, (self.w * self.x) + (self.w - 3),
                                (self.h * self.y) + (self.h - 3), fill="red", outline="black")

    def unfillPlayer(self):
        canvas.create_oval((self.w * self.x) + 2, (self.h * self.y) + 2, (self.w * self.x) + (self.w - 2),
                                (self.h * self.y) + (self.h - 2), fill="white", outline="white")


board = []

canvas = Canvas(master, height=HEIGHT, width=WIDTH, bg=BG, bd=0, highlightthickness=0, relief='ridge')
canvas.pack()

global visited
visited = []
global curx, cury
curx, cury = 0, 0
global cellStack
cellStack = Stack()


def makeBoard():
    for x in range(ROWS):
        board.append([])
        for y in range(COLS):
            isLeft, isDown = True, True
            isRight, isUp, = False, False

            if y == COLS - 1:
                isRight = True
            if x == 0:
                isUp = True

            cell = Cell(isUp, isDown, isLeft, isRight, False, False, x, y, CELLW, CELLH)
            board[x].append(cell)
    # print("Created " + str(board))


def drawBoard():

    #canvas.delete('all')
    #sleep(UPDATE_INT)


    for x in range(ROWS):
        for y in range(COLS):
            cell = board[x][y]

            # canvas.create_text((CELLW*x)+(0.5*CELLW), (CELLH*y)+(0.5*CELLH), text=str(x) + ", " + str(y))

            isUp, isDown, isLeft, isRight = cell.getIsUpWall(), cell.getIsDownWall(), cell.getIsLeftWall(), cell.getIsRightWall()

            if isUp:
                canvas.create_line(CELLW * y, CELLH * x, (CELLW * y) + CELLW, CELLH * x, fill="black",
                                   width=CELL_LINE_WIDTH)
            if isDown:
                canvas.create_line(CELLW * y, (CELLH * x) + CELLH, (CELLW * y) + CELLW, (CELLH * x) + CELLH,
                                   fill="black", width=CELL_LINE_WIDTH)
            if isLeft:
                canvas.create_line(CELLW * y, CELLH * x, CELLW * y, (CELLH * x) + CELLH, fill="black",
                                   width=CELL_LINE_WIDTH)
            if isRight:
                canvas.create_line((CELLW * y) + CELLW, CELLH * x, (CELLW * y) + CELLW, (CELLH * x) + CELLH,
                                   fill="black", width=CELL_LINE_WIDTH)

    #canvas.update()
    #canvas.update_idletasks()

makeBoard()


def findNeighbors(cors):
    global visited

    neighbors = []
    if cors == None:
        return neighbors

    x, y = cors[0], cors[1]

    tryCors = [[x - 1, y], [x + 1, y],
               [x, y - 1], [x, y + 1]]

    for x in range(len(tryCors)):
        c = tryCors[x]
        if c[0] >= 0 and c[0] < ROWS and c[1] >= 0 and c[1] < COLS and c not in visited:
            neighbors.append(c)

    # print("Neighbors " + str(cors[0]) + " , " +  str(cors[1])+ " are " + str(neighbors))
    return neighbors


def removeWall(oldcell, newcell):
    oldx, oldy = oldcell.getX(), oldcell.getY()
    newx, newy = newcell.getX(), newcell.getY()

    if newx == oldx + 1:
        oldcell.setIsDownWall(False)
    if newx == oldx - 1:
        newcell.setIsDownWall(False)
    if newy == oldy - 1:
        oldcell.setIsLeftWall(False)
    if newy == oldy + 1:
        newcell.setIsLeftWall(False)


def makeMaze():
    global board
    global visited
    global cellStack

    # start initial cell at coordinates 0, 0.
    cur_cell = board[0][0]
    cellStack.push(cur_cell)
    visited.append([cur_cell.getX(), cur_cell.getY()])
    while len(visited) != (ROWS * COLS):
        #drawBoard()
        #print(str(len(visited)) + "; " + str(cur_cell.getX()) + "," + str(cur_cell.getY()))

        # find next candidate.
        neighbors = findNeighbors([cur_cell.getX(), cur_cell.getY()])

        # Case 1: if there are no neighbors, pop the stack until you find cell with neighbor(s).

        while len(neighbors) == 0:
            lastVisited = cellStack.pop()
            #print("Popped to : " + str(lastVisited.getX()) + ", " + str(lastVisited.getY()))
            neighbors = findNeighbors([lastVisited.getX(), lastVisited.getY()])
            if len(neighbors) != 0:
                cellStack.push(lastVisited)
                cur_cell = lastVisited

        # At this point of the program, loop has exited and neighbor(s) is/are found.
        new_cell_cors = choice(neighbors)
        #print("New cell is at " + str(new_cell_cors))
        new_cell = board[new_cell_cors[0]][new_cell_cors[1]]

        # remove the wall between cur_cell and new_cell.
        removeWall(cur_cell, new_cell)

        cur_cell = new_cell

        cellStack.push(cur_cell)
        visited.append([cur_cell.getX(), cur_cell.getY()])


makeMaze()
drawBoard()

#print("here!")

player = Player(board[0][0], canvas, CELLW, CELLH, board)

def movePlayer(dir):
    #print("Moving: " + dir)
    # check whether dir is allowed (wall exists)

    x, y = player.cell.getX(), player.cell.getY()

    if dir == "up" and x > 0:
        upCell = board[x - 1][y]
        if not upCell.getIsDownWall():
            player.move("up")

    if dir == "down":
        if not player.cell.getIsDownWall():
            player.move("down")

    if dir == "left":
        if not player.cell.getIsLeftWall():
            player.move("left")

    if dir == "right" and y < COLS-1:
        rightCell = board[x][y + 1]
        if not rightCell.getIsLeftWall():
            player.move("right")



def up(event):
    movePlayer("up")

def down(event):
    movePlayer("down")

def left(event):
    movePlayer("left")

def right(event):
    movePlayer("right")

master.bind("<Up>", up)
master.bind("<Down>", down)
master.bind("<Left>", left)
master.bind("<Right>", right)


#updateBindings()

mainloop()
