# Programmer: Rohan Kosalge
# Creation Date: October 11, 2020
# Purpose: Program to easily understand and visualize
# the scoring for this year's VRC competition (Change Up).

from tkinter import *   # graphics library

master = Tk()
master.title("VEX 2020-21 Change Up Scoring")

# fonts
TOWER_NUMBER_FONT = ("Ubuntu", 30, "bold")
BUTTON_SYMBOL_FONT = ("Ubuntu", 25, "normal")
SCORING_EQUATION_FONT = ("Ubuntu", 25, "bold")

# scoring variables
global red_ball_count
global red_row_count
global blue_ball_count
global blue_row_count
global final_score

red_ball_count = 0
red_row_count = 0
blue_ball_count = 15
blue_row_count = 8
final_score = 0

# three canvases: grid canvas, scoreboard canvas and information canvas
# grid will have the towers, balls, controls
# scoreboard will have the score above in the formula format
# the formula is red balls (1x) + red rows (6x) - blue balls (1x) - blue rows (6x) + 63
# comparison canvas will show how each change affects the score
# will be listed in a cause and effect t-chart

grid = Canvas(master, height=810, width=600, bd=0, highlightthickness=0, bg="black")
grid.grid(row=1, column=0)

scoreboard = Canvas(master, height=40, width=600, bd=0, highlightthickness=0, bg="black")
scoreboard.grid(row=0, column=0)

information = Canvas(master, height=850, width=300, bd=0, highlightthickness=0, bg="black")
#information.grid(rowspan=2, column=1, row=0)

# border lines for information canvas
information.create_line(0, 0, 0, 850, fill="white")
information.create_line(0, 0, 300, 0, fill="white")
information.create_line(0, 850, 300, 850, fill="white")
information.create_line(300, 0, 300, 850, fill="white")

# this array will keep track of the whole layout
tower_layout = [[None, "blue", "blue"], [None, None, "blue"], [None, "blue", "blue"],
                [None, None, "blue"], ["blue", "blue", "blue"], [None, None, "blue"],
                [None, "blue", "blue"], [None, None, "blue"], [None, "blue", "blue"]]

def draw_grid():
    # used to create the grid+numbers, towers and buttons
    # because some values will change based on user-oriented mouse-click bindings
    # this function will most likely be called more than once.

    grid.delete("all")

    # make outer lines for A E S T H E T I C S
    grid.create_line(600, 0, 600, 810, fill="white")
    grid.create_line(0, 810, 600, 810, fill="white")
    
    for x in range(3):
        # use this outer loop to draw the grid lines
        
        grid.create_line(200*x, 0, 200*x, 900, fill="white")
        grid.create_line(0, 270*x, 600, 270*x, fill="white")

        for y in range(3):
            # use the x, y nested loops to make the tower numbers, towers and buttons
            
            tower_num = chr(65 + 3*x + y)
            grid.create_text(200*y + 20, 270*x + 20, text=tower_num, font=TOWER_NUMBER_FONT, fill="white")

            for z in range(3):
                # since there are three tower rings and nine towers in 3x3 grid,
                # it's necessary to have an x, y, z loop!

                ball_value = tower_layout[(3*x)+y][z]
                if ball_value == None:
                    ball_value = "black"

                grid.create_oval(200*y + 105, 270*x + 22.5 + 75*z, 200*y + 180, 270*x + 97.5 + 75*z, fill=ball_value, outline="white", width=2)

                # three buttons: one for launching/appending a red ball, another for a blue ball,
                # and one for pooping/popping the bottom-most ball

                button_colors = ["blue", "red", "grey"]
                button_symbols = ["+", "+", "-"]
                
                grid.create_oval(200*y + 40, 270*x + 80 + 45*z, 200*y + 70, 270*x + 110 + 45*z,
                                 fill=button_colors[z], outline=button_colors[z], width=1)
                grid.create_text(200*y + 56, 270*x + 93 + 45*z, text=button_symbols[z],
                                 font=BUTTON_SYMBOL_FONT, fill="white")

scoring_equation = scoreboard.create_text(300, 20, text="Score = (%s + (6 × %s)) - (%s + (6 × %s)) + 63 = %s" % (red_ball_count, red_row_count, blue_ball_count, blue_row_count, final_score), font=SCORING_EQUATION_FONT, fill="white") 

# also a function needed to change the scoring equation
# reset whenever the grid is reset
def change_scoring():
    scoreboard.itemconfig(scoring_equation, text="Score = (%s + (6 × %s)) - (%s + (6 × %s)) + 63 = %s" % (red_ball_count, red_row_count, blue_ball_count, blue_row_count, final_score))

draw_grid()

# (based on the tower_layout array)
# right now every tower is just a list of Nones (no balls in towers)
# a value can either be blue, red or None value

# based on user-oriented mouse-click bindings these values change through small functions,
# and then run back to the main draw function and scoring function.

def insert_ball(num, color):
    # find tower list based on num index
    # if there is space then it will take the lowest space possible
    # and replace with the specified color ball
    
    tower = tower_layout[num]
    
    for x in range(1, 4):
        if tower[-x] == None:
            tower[-x] = color
            break;

def remove_ball(num):
    # find tower list based on num index
    # unless there are no balls take out the bottom ball
    # and shift the other balls (if any) down

    tower = tower_layout[num]

    for x in range(1, len(tower)):
        tower[-x] = tower[-x-1]
        
    tower[0] = None                 # there will never be a topmost ball after pooping

def change_ball(num, pos):
    tower = tower_layout[num]
    if tower[pos] != None:
        if tower[pos] == "red":
            tower[pos] = "blue"
        else:
            tower[pos] = "red"

def scoring():
    global red_ball_count
    global red_row_count
    global blue_ball_count
    global blue_row_count
    global final_score                      
                                          

    # reset variables
    red_ball_count = 0
    red_row_count = 0
    blue_ball_count = 0
    blue_row_count = 0
    final_score = 0

    # check for individual balls, they are somewhat easier
    
    for tower in tower_layout:
        for ball in tower:
            if ball == "red":
                red_ball_count += 1
            elif ball == "blue":
                blue_ball_count += 1

    # to check for rows, make a separate array for only the top balls
    top_ball_array = [[None, None, None],
                      [None, None, None],
                      [None, None, None]]

    for x in range(3):
        for y in range(3):
            for z in range(3):
                if tower_layout[3*x + y][z] != None:
                    top_ball_array[x][y] = tower_layout[3*x + y][z]
                    break

    for x in range(3):
        if top_ball_array[x][0] == top_ball_array[x][1] and top_ball_array[x][1] == top_ball_array[x][2]:
            if top_ball_array[x][0] == "red":
                red_row_count += 1
            elif top_ball_array[x][0] == "blue":
                blue_row_count += 1
        if top_ball_array[0][x] == top_ball_array[1][x] and top_ball_array[1][x] == top_ball_array[2][x]:
            if top_ball_array[0][x] == "red":
                red_row_count += 1
            elif top_ball_array[0][x] == "blue":
                blue_row_count += 1

    if top_ball_array[0][0] == top_ball_array[1][1] and top_ball_array[1][1] == top_ball_array[2][2]:
        if top_ball_array[0][0] == "red":
            red_row_count += 1
        elif top_ball_array[0][0] == "blue":
            blue_row_count += 1

    if top_ball_array[0][2] == top_ball_array[1][1] and top_ball_array[1][1] == top_ball_array[2][0]:
        if top_ball_array[0][2] == "red":
            red_row_count += 1
        elif top_ball_array[0][2] == "blue":
            blue_row_count += 1

    final_score = (red_ball_count + 6*red_row_count) - (blue_ball_count + 6*blue_row_count) + 63

    change_scoring()

def check_mouse_click(event):
    x, y = event.x, event.y

    # whenever user clicks on grid this function is called and grid is actually reset
    # everything might stay the same but in some cases (if you clicked a button)
    # the change is shown in the next frame

    # there will be a lot of conditional statements to check the coordinates
    # and eventually pass to other functions

    for i in range(3):
        for j in range(3):
            if (x > 200*i + 40 and x < 200*i + 70):
                if (y > 270*j + 80 and y < 270*j + 110):
                    insert_ball(3*j + i, "blue")
                if (y > 270*j + 125 and y < 270*j + 155):
                    insert_ball(3*j + i, "red")
                if (y > 270*j + 170 and y < 270*j + 200):
                    remove_ball(3*j + i)

            for k in range(3):
                if (x > 200*i + 105  and x < 200*i + 180):
                    if (y > 270*j + 22.5 + 75*k and y < 270*j + 97.5 + 75*k):           
                        change_ball(3*j + i, k)

    # refresh in the end
    draw_grid()
    scoring()

def reset_skills(event):

    global tower_layout
    tower_layout = [[None, "blue", "blue"], [None, None, "blue"], [None, "blue", "blue"],
                    [None, None, "blue"], ["blue", "blue", "blue"], [None, None, "blue"],
                    [None, "blue", "blue"], [None, None, "blue"], [None, "blue", "blue"]]

    draw_grid()
    scoring()


# bind the mouse to the grid so it can detect mouse input
grid.bind("<Button-1>", check_mouse_click)

# bind the key "r" to reset the skills tower layout
master.bind("r", reset_skills)

mainloop()
