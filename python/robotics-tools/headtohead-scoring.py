from tkinter import *
from math import floor
from random import *

# fonts
TABLE_FONT = ("Ubuntu", 12, "bold")
SCORE_FONT = ("Ubuntu", 25, "bold")
AUTON_TITLE_FONT = ("Ubuntu", 18, "bold")
AUTON_REG_FONT = ("Ubuntu", 15, "bold")
DOUBLER_FONT = ("Ubuntu", 10, "normal")
TOWER_FONT = ("Ubuntu", 20, "bold")
START_ROBOT_FONT = ("Ubuntu", 17, "bold")

master = Tk()
master.title("VEX 2020-21 Change Up Head-to-Head Scoring")

canvas = Canvas(master, height=880, width=1200, bd=0, highlightthickness=0, bg="white")
canvas.grid(row=0, column=0)

# DATA
########################################################################

teams = ["Red A", "Red B", "Blue A", "Blue B"]

team_colors = ["red", "blue"]

totals_texts = [[["Red Alliance Total: 0", "Blue Alliance Total: 0"], ["Red Alliance Total: 0", "Blue Alliance Total: 0"],
                 ["Red Alliance Total: 0", "Blue Alliance Total: 0"]],
                [["Red Alliance Total: 0", "Blue Alliance Total: 0"], ["Red Alliance Total: 0", "Blue Alliance Total: 0"],
                 ["Red Alliance Total: 0", "Blue Alliance Total: 0"]],
                [["Red Alliance Total: 0", "Blue Alliance Total: 0"], ["Red Alliance Total: 0", "Blue Alliance Total: 0"],
                 ["Red Alliance Total: 0", "Blue Alliance Total: 0"]]]
totals_owners = [["No One owns this goal", "No One owns this goal", "No One owns this goal"],
                 ["No One owns this goal", "No One owns this goal", "No One owns this goal"],
                 ["No One owns this goal", "No One owns this goal", "No One owns this goal"]]

# field = [[
#         # Red A Field  Layout (Goal labels)= A B C / D E F / G H I
#           [None, "blue", "red"], ["red", "blue", "red"], [None, "red", "blue"],
#           [None, "blue", "red"], [None, None, None], [None, "red", "blue"],
#           [None, "blue", "red"], ["blue", "red", "blue"], [None, "red", "blue"]],
#
#         # Red B Field
#          [[None, "blue", "red"], ["red", "blue", "red"], [None, "red", "blue"],
#           [None, "blue", "red"], [None, None, None], [None, "red", "blue"],
#           [None, "blue", "red"], ["blue", "red", "blue"], [None, "red", "blue"]],
#
#         # Blue A Field
#          [[None, "blue", "red"], ["red", "blue", "red"], [None, "red", "blue"],
#           [None, "blue", "red"], [None, None, None], [None, "red", "blue"],
#           [None, "blue", "red"], ["blue", "red", "blue"], [None, "red", "blue"]],
#
#         # Blue B Field
#          [[None, "blue", "red"], ["red", "blue", "red"], [None, "red", "blue"],
#           [None, "blue", "red"], [None, None, None], [None, "red", "blue"],
#           [None, "blue", "red"], ["blue", "red", "blue"], [None, "red", "blue"]]]

field = [
            [[None, None, None], [None, None, None], [None, None, None],
            [None, None, None], [None, None, None], [None, None, None],
            [None, None, None], [None, None, None], [None, None, None]],

            [[None, None, None], [None, None, None], [None, None, None],
            [None, None, None], [None, None, None], [None, None, None],
            [None, None, None], [None, None, None], [None, None, None]],

            [[None, None, None], [None, None, None], [None, None, None],
            [None, None, None], [None, None, None], [None, None, None],
            [None, None, None], [None, None, None], [None, None, None]],

            [[None, None, None], [None, None, None], [None, None, None],
            [None, None, None], [None, None, None], [None, None, None],
            [None, None, None], [None, None, None], [None, None, None]],

        ]



goals = [[None, None, None, None, None, None, None, None, None],
         [None, None, None, None, None, None, None, None, None],
         [None, None, None, None, None, None, None, None, None],
         [None, None, None, None, None, None, None, None, None]]

owners = [[None, None, None],
          [None, None, None],
          [None, None, None]]

doublers = [[False, False, False, False, False, False, False, False, False],
            [False, False, False, False, False, False, False, False, False],
            [False, False, False, False, False, False, False, False, False],
            [False, False, False, False, False, False, False, False, False]]

global red_total
global blue_total

red_total = 0
blue_total = 0

global is_auton_red
global is_auton_blue
global is_auton_tie

is_auton_red = False
is_auton_blue = False
is_auton_tie = False

########################################################################

def draw_start():
    canvas.delete('all')

    canvas.create_rectangle(350, 190, 851, 691, width=4, fill="grey75")

    basex, basey = 350, 190
    for x in range(6):
        for y in range(6):
            tile_color = "grey" + str(randint(65, 95))
            canvas.create_rectangle(basex + (500/6)*x, basey + (500/6)*y, basex + (500/6)*(x+1), basey + (500/6)*(y+1),
                                    fill=tile_color, width=1)
            #canvas.create_line(basex + (500/6)*x, basey, basex + (500/6)*x, basey + 500, width=1)
            #canvas.create_line(basex, basey + (500/6)*y, basex + 500, basey + (500/6)*y, width=1)

    ball_width = 40
    spacing = 230
    for x in range(3):
        for y in range(3):
            canvas.create_oval(basex + spacing*x, basey + spacing*y, basex + spacing*x + ball_width,
                               basey + spacing*y + ball_width, width=4)

    canvas.create_rectangle(basex+4, basey + (500/6) + 10, basex + (500/6) - 16, basey + (500/3) - 10, width=2, fill="red")
    canvas.create_text(basex + (250/6) - 6, basey + (750/6), text="Red A", font=START_ROBOT_FONT, fill="white")
    canvas.create_rectangle(basex+4, basey + (1000/3) + 10, basex + (500/6) - 16, basey + (2500/6) - 10, width=2, fill="red")
    canvas.create_text(basex + (250/6) - 6, basey + (2250/6), text="Red B", font=START_ROBOT_FONT, fill="white")
    canvas.create_rectangle(basex+496, basey + (500/6) + 10, basex + (2500/6) + 16, basey + (500/3) - 10, width=2, fill="blue")
    canvas.create_text(basex + (1250/6) + 256, basey + (750/6), text="Blue A", font=START_ROBOT_FONT, fill="white")
    canvas.create_rectangle(basex+496, basey + (1000/3) + 10, basex + (2500/6) + 16, basey + (2500/6) - 10, width=2, fill="blue")
    canvas.create_text(basex + (1250/6) + 256, basey + (2250/6), text="Blue B", font=START_ROBOT_FONT, fill="white")

    for x in range(3):
        canvas.create_oval(basex+4.5, basey + 5 + spacing*x, basex+34.5, basey + 35 + spacing*x, fill="blue", width=2)
        canvas.create_oval(basex+495, basey + 5 + spacing*x, basex+465, basey + 35 + spacing*x, fill="red", width=2)

    canvas.create_oval(basex+235, basey+5, basex+265, basey+35, fill="blue", width=2)
    canvas.create_oval(basex+235, basey+495, basex+265, basey+465, fill="red", width=2)
    canvas.create_oval(basex+32, basey+32, basex+62, basey+62, fill="red", width=2)
    canvas.create_oval(basex+32, basey+468, basex+62, basey+438, fill="red", width=2)
    canvas.create_oval(basex+468, basey+32, basex+438, basey+62, fill="blue", width=2)
    canvas.create_oval(basex+468, basey+468, basex+438, basey+438, fill="blue", width=2)
    canvas.create_oval(basex+235, basey+197, basex+265, basey+227, fill="red", width=2)
    canvas.create_oval(basex+197, basey+235, basex+227, basey+265, fill="blue", width=2)
    canvas.create_oval(basex+235, basey+273, basex+265, basey+303, fill="blue", width=2)
    canvas.create_oval(basex+273, basey+235, basex+303, basey+265, fill="red", width=2)
    canvas.create_oval(basex+235, basey+(750/6)-15, basex+265, basey+(750/6)+15, fill="red", width=2)
    canvas.create_oval(basex+235, basey+(2250/6)-15, basex+265, basey+(2250/6)+15, fill="blue", width=2)

    canvas.create_polygon(875, 190, 1190, 190, 1190, 435, 875, 435, 875, 330, 860, basey+(750/6), 875, 300, fill="blue", width=2, outline="black")
    canvas.create_polygon(875, 445, 1190, 445, 1190, 691, 875, 691, 875, 585, 860, basey+(2250/6), 875, 555, fill="blue", width=2, outline="black")

#draw_start()

def draw_main():

    global red_total
    global blue_total

    global is_auton_red
    global is_auton_blue
    global is_auton_tie

    canvas.delete('all')
    for x in range(3):
        for y in range(3):
            basey, basex = 400 * x, 280 * y
            for r in range(4):
                for c in range(4):
                    addx, addy = (140 / 3) * r, 100 * c

                    if r == 0:
                        boxcolor = team_colors[floor(c / 2)]
                        boxtext = teams[c]

                        canvas.create_rectangle(basey + addy, basex + addx, basey + addy + 100,
                                                       basex + addx + (140 / 3),
                                                       fill=boxcolor)
                        canvas.create_text(basey + addy + 60, basex + addx + (70 / 3),
                                                  text=boxtext, fill="white", font=TABLE_FONT, anchor=E)

                        doubler_box_color = boxcolor
                        if doublers[c][(3 * y) + x] == True:
                            doubler_box_color = "yellow"
                        canvas.create_rectangle(basey+addy+70, basex+addx+15, basey+addy+86.667, basex+addx+31.667, width=2, fill=doubler_box_color)
                        canvas.create_text(basey+addy+78.333, basex+addx+23.333, text="D", font=DOUBLER_FONT)
                    else:
                        canvas.create_rectangle(basey + addy, basex + addx, basey + addy + 100,
                                                       basex + addx + (140 / 3))

                        ball_color = field[c][(3 * y) + x][r - 1]
                        if ball_color == None:
                            ball_color = "white"
                        canvas.create_oval(basey + addy + 30, basex + addx + (10 / 3), basey + addy + 70,
                                                  basex + addx + (130 / 3),
                                                  width=2, fill=ball_color)

            for r in range(4, 5):
                for c in range(2):
                    addx, addy = (140 / 3) * r, 200 * c

                    canvas.create_rectangle(basey + addy, basex + addx, basey + addy + 200,
                                                   basex + addx + (140 / 3))

                    if c == 0:
                        text_color = "red"
                    else:
                        text_color = "blue"
                    canvas.create_text(basey + addy + 100, basex + addx + (70 / 3), text=totals_texts[y][x][c],
                                              fill=text_color, font=TABLE_FONT)

            for r in range(5, 6):
                if totals_owners[y][x] == "RED owns this goal":
                    text_color = "red"
                elif totals_owners[y][x] == "BLUE owns this goal":
                    text_color = "blue"
                else:
                    text_color = "black"

                canvas.create_rectangle(basey, basex + (700 / 3), basey + 400, basex + 280)
                canvas.create_text(basey + 200, basex + (770 / 3), text=totals_owners[y][x],
                                          fill=text_color, font=TABLE_FONT)

                canvas.create_rectangle(basey + 5, basex + (700 / 3) + 5, basey + 5 + (140 / 3), basex + 280 - 5, width=2, fill="grey90")
                canvas.create_text(basey + 5 + (70 / 3), basex + (770/3), text=chr(65 + (3 * y + x)), font=TOWER_FONT)

    for x in range(3):
        canvas.create_line(0, 280 * (x + 1), 1200, 280 * (x + 1), width=3)
        canvas.create_line(400 * (x + 1), 0, 400 * (x + 1), 840, width=3)

    canvas.create_line(1200, 0, 1200, 880, width=3)
    canvas.create_line(0, 0, 0, 880, width=3)

    canvas.create_text(20, 860, text="Autonomous Winner:", font=AUTON_TITLE_FONT, anchor=W)

    canvas.create_rectangle(210, 845, 725, 875, width=2, fill="grey90")

    if is_auton_red:
        canvas.create_rectangle(215, 848, 370, 872, width=2, fill="yellow")
    else:
        canvas.create_rectangle(215, 848, 370, 872, width=2, fill="white")

    if is_auton_blue:
        canvas.create_rectangle(390, 848, 545, 872, width=2, fill="yellow")
    else:
        canvas.create_rectangle(390, 848, 545, 872, width=2, fill="white")

    if is_auton_tie:
        canvas.create_rectangle(565, 848, 720, 872, width=2, fill="yellow")
    else:
        canvas.create_rectangle(565, 848, 720, 872, width=2, fill="white")

    canvas.create_rectangle(730, 845, 1190, 875, width=2, fill="grey90")
    canvas.create_text(875, 860, text="RED       " + str(red_total), font=SCORE_FONT, fill="red", anchor=E)
    canvas.create_text(950, 860, text="-", font=SCORE_FONT, fill="black")
    canvas.create_text(1025, 860, text=str(blue_total) + "       BLUE", font=SCORE_FONT, fill="blue", anchor=W)

    canvas.create_text(292.5, 860, text="RED", font=AUTON_REG_FONT)
    canvas.create_text(292.5+175, 860, text="BLUE", font=AUTON_REG_FONT)
    canvas.create_text(292.5+350, 860, text="TIE", font=AUTON_REG_FONT)


global red_scoring_map
red_scoring_map = {"red": 2, "blue": 1, None: 0}

global blue_scoring_map
blue_scoring_map = {"blue": 2, "red": 1, None: 0}


class Goal:
    global red_scoring_map
    global blue_scoring_map

    def __init__(self, side, ball1, ball2, ball3, doubler):
        self.ball1 = ball1
        self.ball2 = ball2
        self.ball3 = ball3
        self.doubler = doubler  # if the robot is contacting the goal
        self.total = 0

        if side == "red":
            self.scoring_map = red_scoring_map
        else:
            self.scoring_map = blue_scoring_map

    def get_doubler(self):
        return self.doubler

    def get_total(self):
        ball1pts = self.scoring_map[self.ball1]
        ball2pts = self.scoring_map[self.ball2]
        ball3pts = self.scoring_map[self.ball3]

        self.total = ball1pts + ball2pts + ball3pts

        if self.doubler:
            self.total *= 2

        return self.total


def ownership(redAgoal, redBgoal, blueAgoal, blueBgoal):
    redtotal = redAgoal.get_total() + redBgoal.get_total()
    bluetotal = blueAgoal.get_total() + blueBgoal.get_total()

    if redtotal > bluetotal:
        owner = "red"
    elif bluetotal > redtotal:
        owner = "blue"
    else:
        owner = None

    return owner


def update_goals():
    for x in range(4):
        for y in range(9):
            tower = field[x][y]
            if x < 2:
                side = "red"
            else:
                side = "blue"

            doubler = doublers[x][y]
            goal = Goal(side, tower[0], tower[1], tower[2], doubler)


            goals[x][y] = goal



def update_ownerships():
    for x in range(3):
        for y in range(3):
            owner = ownership(goals[0][(3 * x) + y], goals[1][(3 * x) + y], goals[2][(3 * x) + y],
                              goals[3][(3 * x) + y])
            owners[x][y] = owner

            if owners[x][y] == None:
                totals_owners[x][y] = "No One owns this goal"
            else:
                totals_owners[x][y] = str(owner.upper()) + " owns this goal"

def check_valid_row(side_index, top_index1, top_index2, top_index3):
    global red_total
    global blue_total

    top_index1 -= 1
    top_index2 -= 1
    top_index3 -= 1

    toprow1, topcol1 = floor(top_index1 / 3), top_index1 % 3
    toprow2, topcol2 = floor(top_index2 / 3), top_index2 % 3
    toprow3, topcol3 = floor(top_index3 / 3), top_index3 % 3



    if owners[toprow1][topcol1] == owners[toprow2][topcol2] and owners[toprow2][topcol2] == owners[toprow3][topcol3]:

        if owners[toprow1][topcol1] == "red" and side_index == 0:
            red_total += 13
            #print("Valid row found at side index %d, top_index1 %d, top_index2 %d, and top_index3 %d"
                  #% (side_index, top_index1, top_index2, top_index3))
        elif owners[toprow1][topcol1] == "blue" and  side_index == 1:
            blue_total += 13
            #print("Valid row found at side index %d, top_index1 %d, top_index2 %d, and top_index3 %d"
                  #% (side_index, top_index1, top_index2, top_index3))

def update_score():
    global red_total
    global blue_total

    for x in range(2):

        check_valid_row(x, 1, 2, 3)
        check_valid_row(x, 4, 5, 6)
        check_valid_row(x, 7, 8, 9)
        check_valid_row(x, 1, 4, 7)
        check_valid_row(x, 2, 5, 8)
        check_valid_row(x, 3, 6, 9)
        check_valid_row(x, 1, 5, 9)
        check_valid_row(x, 3, 5, 7)


    for x in range(2):
        for y in range(3):
            for z in range(3):

                alliance_total = 0

                goalA = goals[2*x][(3 * y) + z]
                goalB = goals[(2*x)+1][(3 * y) + z]

                goalAtotal = goalA.get_total()
                goalBtotal = goalB.get_total()

                if goalA.get_doubler() is True and goalB.get_doubler() is False:
                    goalBtotal *= 2
                elif goalB.get_doubler() is True and goalA.get_doubler() is False:
                    goalAtotal *= 2
                elif goalB.get_doubler() is True and goalA.get_doubler() is True:
                    goalAtotal *= 2
                    goalBtotal *= 2

                alliance_total = goalAtotal + goalBtotal

                if x == 0:
                    red_total += alliance_total
                    totals_texts[y][z][x] = "Red Alliance Total: " + str(alliance_total)
                else:
                    blue_total += alliance_total
                    totals_texts[y][z][x] = "Blue Alliance Total: " + str(alliance_total)





def update():
    update_goals()
    update_ownerships()
    update_score()

def auton_red():
    global red_total
    global is_auton_red
    global is_auton_blue
    global is_auton_tie
    is_auton_blue = False
    is_auton_tie = False
    is_auton_red = True

def auton_blue():
    global blue_total
    global is_auton_red
    global is_auton_blue
    global is_auton_tie
    is_auton_red = False
    is_auton_tie = False
    is_auton_blue = True

def auton_tie():
    global red_total
    global blue_total
    global is_auton_red
    global is_auton_blue
    global is_auton_tie
    is_auton_red = False
    is_auton_blue = False
    is_auton_tie = True


def mouse_click_event(x, y):
    global red_total
    global blue_total

    red_total = 0
    blue_total = 0

    ball_vals_red = [None, "red", "blue"]
    ball_vals_blue = [None, "blue", "red"]
    for i in range(3):
        for j in range(3):
            for k in range(0, 1):
                for l in range(4):
                    basei, basej = 280 * j, 400 * i
                    addi, addj = (140/3) * k, 100 * l

                    x1 = basej + addj + 70
                    y1 = basei + addi + 15
                    x2 = basej + addj + (260/3)
                    y2 = basei + addi + (95/3)

                    if x > x1 and x < x2 and y > y1 and y < y2:
                        #print("here")
                        doubler = doublers[l][(3 * j) + i]
                        if doubler == True:
                            doublers[l][(3 * j) + i] = False
                        elif doubler == False:
                            doublers[l][(3 * j) + i] = True

            for k in range(1, 4):
                for l in range(4):
                    basei, basej = 280 * j, 400 * i
                    addi, addj = (140 / 3) * k, 100 * l

                    x1 = basej + addj + 30
                    y1 = basei + addi + (10 / 3)
                    x2 = basej + addj + 70
                    y2 = basei + addi + (130 / 3)

                    if x > x1 and x < x2 and y > y1 and y < y2:
                        ball_val = field[l][(3 * j) + i][k - 1]
                        if (x > 200 and x < 400) or (x > 600 and x < 800) or (x > 1000 and x < 1200):
                            ball_vals = ball_vals_blue
                        else:
                            ball_vals = ball_vals_red

                        ball_val_cur_index = ball_vals.index(ball_val)
                        ball_val_cur_index += 1
                        field[l][(3 * j) + i][k - 1] = ball_vals[ball_val_cur_index % 3]

    for i in range(3):

        x1 = 175*i + 215
        x2 = 175*i + 370

        if x > x1 and x < x2 and y > 848 and y < 872:
            if i == 0:
                auton_red()
            elif i == 1:
                auton_blue()
            elif i == 2:
                auton_tie()

    if is_auton_red:
        red_total += 6
    elif is_auton_blue:
        blue_total += 6
    elif is_auton_tie:
        red_total += 3
        blue_total += 3


    update()
    draw_main()


def reset_field(event):
    global field
    field = [[

         # Red A Field  Layout (Goal labels)= A B C / D E F / G H I
           [None, "blue", "red"], ["red", "blue", "red"], [None, "red", "blue"],
           [None, "blue", "red"], [None, None, None], [None, "red", "blue"],
           [None, "blue", "red"], ["blue", "red", "blue"], [None, "red", "blue"]],

         # Red B Field
          [[None, "blue", "red"], ["red", "blue", "red"], [None, "red", "blue"],
           [None, "blue", "red"], [None, None, None], [None, "red", "blue"],
           [None, "blue", "red"], ["blue", "red", "blue"], [None, "red", "blue"]],

         # Blue A Field
          [[None, "blue", "red"], ["red", "blue", "red"], [None, "red", "blue"],
           [None, "blue", "red"], [None, None, None], [None, "red", "blue"],
           [None, "blue", "red"], ["blue", "red", "blue"], [None, "red", "blue"]],

         # Blue B Field
          [[None, "blue", "red"], ["red", "blue", "red"], [None, "red", "blue"],
           [None, "blue", "red"], [None, None, None], [None, "red", "blue"],
           [None, "blue", "red"], ["blue", "red", "blue"], [None, "red", "blue"]]]

def clear_field(event):
    global field
    field = [
        [[None, None, None], [None, None, None], [None, None, None],
         [None, None, None], [None, None, None], [None, None, None],
         [None, None, None], [None, None, None], [None, None, None]],

        [[None, None, None], [None, None, None], [None, None, None],
         [None, None, None], [None, None, None], [None, None, None],
         [None, None, None], [None, None, None], [None, None, None]],

        [[None, None, None], [None, None, None], [None, None, None],
         [None, None, None], [None, None, None], [None, None, None],
         [None, None, None], [None, None, None], [None, None, None]],

        [[None, None, None], [None, None, None], [None, None, None],
         [None, None, None], [None, None, None], [None, None, None],
         [None, None, None], [None, None, None], [None, None, None]],

    ]



def formulate(event):
    x, y = event.x, event.y
    mouse_click_event(x, y)

master.bind("<Button-1>", formulate)
master.bind("<r>", reset_field)
master.bind("<c>", clear_field)

update()
draw_main()

mainloop()
