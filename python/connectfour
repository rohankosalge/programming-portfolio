from tkinter import *

d = Tk()
d.title("Connect Four Multiplayer")

c = Canvas(d, height=900, width=1050, bg='#037ffc')
c.pack()

global board
board = [[None, None, None, None, None, None],
         [None, None, None, None, None, None],
         [None, None, None, None, None, None],
         [None, None, None, None, None, None],
         [None, None, None, None, None, None],
         [None, None, None, None, None, None],
         [None, None, None, None, None, None]]

def drawBoard(board):
    for x in range(len(board)):
        for y in range(len(board[x])):
            if board[x][y] == None:
                color = 'white'
            elif board[x][y] == 1:
                color = 'red'
            elif board[x][y] == 2:
                color = 'yellow'
            c.create_oval(150*x, 900-(150*y), (150*x)+150, 900-((150*y)+150), fill=color, width=2)

drawBoard(board)

global indicator
indicator = 0

def switchSig(indicator):
    if indicator == 0:
        new_indic = 1
    elif indicator == 1:
        new_indic = 0

    return new_indic

def checkWin(board):
    winner = None
    
    # check columns first. Easiest to check lol.
    for x in range(7):
        for y in range(3):
            if (board[x][y] == board[x][y+1]) and (board[x][y+1] == board[x][y+2]) and (board[x][y+2] == board[x][y+3]):
                if board[x][y] == 1:
                    winner = 'red'
                elif board[x][y] == 2:
                    winner = 'yellow'

    # argh gotta check rows
    for x in range(4):
        for y in range(6):
            # actually it isn't that bad lol
            if (board[x][y] == board[x+1][y]) and (board[x+1][y] == board[x+2][y]) and (board[x+2][y] == board[x+3][y]):
                if board[x][y] == 1:
                    winner = 'red'
                elif board[x][y] == 2:
                    winner = 'yellow'

    # lol i forgot diagonals
    for x in range(3):
        for y in range(4):
            if (board[x][y] == board[x+1][y+1]) and (board[x+1][y+1] == board[x+2][y+2]) and (board[x+2][y+2] == board[x+3][x+3]):
                if board[x][y] == 1:
                    winner = 'red'
                elif board[x][y] == 2:
                    winner = 'yellow'

    for x in range(4, 7):
        for y in range(4):
            if (board[x][y] == board[x-1][y-1]) and (board[x-1][y-1] == board[x-2][y-2]) and (board[x-2][y-2] == board[x-3][y-3]):
                if board[x][y] == 1:
                    winner = 'red'
                elif board[x][y] == 2:
                    winner = 'yellow'

    return winner

def formulate(event):
    global board
    global indicator
    
    position = event.x

    if position >=0 and position <= 149:
        column = 0
    elif position >= 150 and position <= 299:
        column = 1
    elif position >= 300 and position <= 449:
        column = 2
    elif position >= 450 and position <= 599:
        column = 3
    elif position >= 600 and position <= 749:
        column = 4
    elif position >= 750 and position <= 899:
        column = 5
    else:
        column = 6

    for x in range(len(board[column])):
        if None not in board[column]:
            print(board[column])
            break
        
        if board[column][x] == None:
            if indicator == 0:
                board[column][x] = 1
            elif indicator == 1:
                board[column][x] = 2

            indicator = switchSig(indicator)
            break

    drawBoard(board)

    winner = checkWin(board)

    if winner != None:
        c.unbind("<Button-1>")

        c.create_rectangle(325, 350, 725, 550, fill='white', width=3)
        c.create_text(525, 450, text=winner.upper() + " WINS!", font=("Ubuntu", 30, "bold"))

    

c.bind("<Button-1>", formulate)
