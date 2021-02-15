from tkinter import *

master = Tk()
master.title("Pentago")

canvas = Canvas(master, height=800, width=800, highlightthickness=0, bd=0, bg="grey60")
canvas.pack()

ENDGAME_HEADER_FONT = ("Courier", 25, "bold")
ENDGAME_SUBHEADER_FONT = ("Courier", 15, "italic")

board = [[None, None, None, None, None, None],
         [None, None, None, None, None, None],
         [None, None, None, None, None, None],
         [None, None, None, None, None, None],
         [None, None, None, None, None, None],
         [None, None, None, None, None, None]]

global turn
turn = "black"

global step1
global step2
global step3
global step4

step1 = False
step2 = False
step3 = False
step4 = True

def drawboard():
    canvas.delete('all')
    
    for x in range(2):
        for y in range(2):
            canvas.create_rectangle(100+(300*x), 100+(300*y), 400+(300*x), 400+(300*y), fill="red", outline="black", width=3)

    for x in range(6):
        for y in range(6):
            fill_color = board[x][y]
            if fill_color == None:
                fill_color = "red"
            canvas.create_oval(120+(100*y), 120+(100*x), 180+(100*y), 180+(100*x), fill=fill_color, outline="black", width=3)

    for x in range(2):
        canvas.create_line(50+(700*x), 110, 50+(700*x), 390, fill="black", width=5, arrow="first")
        canvas.create_line(110, 50+(700*x), 390, 50+(700*x), fill="black", width=5, arrow="first")
        canvas.create_line(410, 50+(700*x), 690, 50+(700*x), fill="black", width=5, arrow="last")
        canvas.create_line(50+(700*x), 410, 50+(700*x), 690, fill="black", width=5, arrow="last")

drawboard()

def rotate_clockwise(section):
    newsection = [[section[2][0], section[1][0], section[0][0]],
                  [section[2][1], section[1][1], section[0][1]],
                  [section[2][2], section[1][2], section[0][2]]]

    return newsection

def rotate_counterclockwise(section):
    newsection = [[section[0][2], section[1][2], section[2][2]],
                  [section[0][1], section[1][1], section[2][1]],
                  [section[0][0], section[1][0], section[2][0]]]

    return newsection

def check(alist): 
    return all(i == alist[0] for i in alist)

def endgame(winner):
    master.unbind("<Button-1>")

    canvas.create_rectangle(250, 350, 550, 450, fill="white", outline="black", width=3)
    canvas.create_text(400, 370, text="GAME OVER", font=ENDGAME_HEADER_FONT)
    canvas.create_text(400, 400, text=winner.upper() + " wins", font=ENDGAME_SUBHEADER_FONT)

def checkwinner():

    winner = None
    
    for x in range(6):
        for y in range(2):
            if check(board[x][y:y+4]) == True:
                if board[x][y] == "white":
                    winner = "white"
                elif board[x][y] == "black":
                    winner = "black"

    for x in range(2):
        for y in range(6):
            if check([board[x][y], board[x+1][y], board[x+2][y], board[x+3][y], board[x+4][y]]) == True:
                if board[x][y] == "white":
                    winner = "white"
                elif board[x][y] == "black":
                    winner = "black"

    for x in range(2):
        for y in range(2):
            if check([board[x][y], board[x+1][y+1], board[x+2][y+2], board[x+3][y+3], board[x+4][y+4]]) == True:
                if board[x][y] == "white":
                    winner = "white"
                elif board[x][y] == "black":
                    winner = "black"

    for x in range(4, 6):
        for y in range(2):
            if check([board[x][y], board[x-1][y+1], board[x-2][y+2], board[x-3][y+3], board[x-4][y+4]]) == True:
                if board[x][y] == "white":
                    winner = "white"
                elif board[x][y] == "black":
                    winner = "black"

    return winner

    
            

def formulate(event):
    global turn
    global step1
    global step2
    global step3
    global step4
    
    x, y = event.x, event.y

    for i in range(6):
        for j in range(6):
            bx1, bx2 = 120+(100*i), 180+(100*i)
            by1, by2 = 120+(100*j), 180+(100*j)


            if x > bx1 and x < bx2 and y > by1 and y < by2 and board[j][i] == None and (step1 == False and step3 == False) and (step2 == True or step4 == True):
                board[j][i] = turn
                
                if turn == "black":
                    turn = "white"
                else:
                    turn = "black"

                print(board)
                print()
                print()

                drawboard()

                whowon = checkwinner()
                if whowon != None:
                    endgame(whowon)

                if step2 == True:
                    step3 = True
                    step2 = False
                elif step4 == True:
                    step1 = True
                    step4 = False

    if x > 10 and x < 90:
        if y > 105 and y < 395 and (step2 == False and step4 == False) and (step1 == True or step3 == True):
            section = [board[0][0:3], board[1][0:3], board[2][0:3]]
            section = rotate_clockwise(section)

            board[0][0:3] = section[0]
            board[1][0:3] = section[1]
            board[2][0:3] = section[2]

            drawboard()

            whowon = checkwinner()
            if whowon != None:
                endgame(whowon)

            if step1 == True:
                step1 = False
                step2 = True
            elif step3 == True:
                step3 = False
                step4 = True

        if y > 405 and y < 695 and (step2 == False and step4 == False) and (step1 == True or step3 == True):
            section = [board[3][0:3], board[4][0:3], board[5][0:3]]
            section = rotate_counterclockwise(section)

            board[3][0:3] = section[0]
            board[4][0:3] = section[1]
            board[5][0:3] = section[2]

            drawboard()

            whowon = checkwinner()
            if whowon != None:
                endgame(whowon)

            if step1 == True:
                step1 = False
                step2 = True
            elif step3 == True:
                step3 = False
                step4 = True

    if x > 710 and x < 790:
        if y > 105 and y < 395 and (step2 == False and step4 == False) and (step1 == True or step3 == True):
            section = [board[0][3:6], board[1][3:6], board[2][3:6]]
            section = rotate_counterclockwise(section)

            board[0][3:6] = section[0]
            board[1][3:6] = section[1]
            board[2][3:6] = section[2]

            drawboard()

            whowon = checkwinner()
            if whowon != None:
                endgame(whowon)

            if step1 == True:
                step1 = False
                step2 = True
            elif step3 == True:
                step3 = False
                step4 = True

        if y > 405 and y < 695 and (step2 == False and step4 == False) and (step1 == True or step3 == True):
            section = [board[3][3:6], board[4][3:6], board[5][3:6]]
            section = rotate_clockwise(section)

            board[3][3:6] = section[0]
            board[4][3:6] = section[1]
            board[5][3:6] = section[2]

            drawboard()

            whowon = checkwinner()
            if whowon != None:
                endgame(whowon)

            if step1 == True:
                step1 = False
                step2 = True
            elif step3 == True:
                step3 = False
                step4 = True

    if y > 10 and y < 90:
        if x > 105 and x < 395 and (step2 == False and step4 == False) and (step1 == True or step3 == True):
            section = [board[0][0:3], board[1][0:3], board[2][0:3]]
            section = rotate_counterclockwise(section)

            board[0][0:3] = section[0]
            board[1][0:3] = section[1]
            board[2][0:3] = section[2]

            drawboard()

            whowon = checkwinner()
            if whowon != None:
                endgame(whowon)

            if step1 == True:
                step1 = False
                step2 = True
            elif step3 == True:
                step3 = False
                step4 = True

        if x > 405 and x < 695 and (step2 == False and step4 == False) and (step1 == True or step3 == True):
            section = [board[0][3:6], board[1][3:6], board[2][3:6]]
            section = rotate_clockwise(section)

            board[0][3:6] = section[0]
            board[1][3:6] = section[1]
            board[2][3:6] = section[2]

            drawboard()

            whowon = checkwinner()
            if whowon != None:
                endgame(whowon)

            if step1 == True:
                step1 = False
                step2 = True
            elif step3 == True:
                step3 = False
                step4 = True

    if y > 710 and y < 790:
        if x > 105 and x < 395 and (step2 == False and step4 == False) and (step1 == True or step3 == True):
            section = [board[3][0:3], board[4][0:3], board[5][0:3]]
            section = rotate_clockwise(section)

            board[3][0:3] = section[0]
            board[4][0:3] = section[1]
            board[5][0:3] = section[2]

            drawboard()

            whowon = checkwinner()
            if whowon != None:
                endgame(whowon)

            if step1 == True:
                step1 = False
                step2 = True
            elif step3 == True:
                step3 = False
                step4 = True

        if x > 405 and x < 695 and (step2 == False and step4 == False) and (step1 == True or step3 == True):
            section = [board[3][3:6], board[4][3:6], board[5][3:6]]
            section = rotate_counterclockwise(section)

            board[3][3:6] = section[0]
            board[4][3:6] = section[1]
            board[5][3:6] = section[2]

            drawboard()

            whowon = checkwinner()
            if whowon != None:
                endgame(whowon)

            if step1 == True:
                step1 = False
                step2 = True
            elif step3 == True:
                step3 = False
                step4 = True

            
master.bind("<Button-1>", formulate)
