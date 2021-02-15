#!/usr/bin/env python

from tkinter import *
from random import randint

master = Tk()
master.title("Codebreaker")

canvas = Canvas(master, height=400, width=800, bg="grey")
canvas.grid(row=0, column=0)


    
def main(max_tries):
    
    canvas.delete('all')
    TITLE_FONT = ("Courier", 40, "bold")
    SUBTITLE_FONT = ("Courier", 20, "normal")
    FOOTNOTE_FONT = ("Courier", 10, "italic")
    BUTTON_FONT = ("Courier", 20, "bold")
    END_MAIN_FONT = ("Courier", 25, "bold")
    END_SUB_FONT = ("Courier", 10, "italic")
    END_BUTTON_FONT = ("Courier", 10, "normal")
    OPTIONS_BUTTON_FONT = ("Courier", 12, "bold")

    global try_count
    try_count = 0

    circles = []
    circles_colors_keys = []
    checks = [None, None, None, None]
    global options_widgets
    options_widgets = []

    canvas.create_text(400, 40, text="CODEBREAKER", font=TITLE_FONT)
    try_count_text = canvas.create_text(400, 80, text="Number of tries left: " + str(max_tries-try_count), font=SUBTITLE_FONT)
    canvas.create_rectangle(10, 340, 372, 390, width=2)
    canvas.create_text(20, 350, text="White mark - correct color, wrong placement", font=FOOTNOTE_FONT, anchor=W)
    canvas.create_text(20, 365, text="Red mark - correct color, right placement", font=FOOTNOTE_FONT, anchor=W)
    canvas.create_text(20, 380, text="Grey mark - wrong color, wrong placement", font=FOOTNOTE_FONT, anchor=W)
    canvas.create_rectangle(400, 340, 650, 390, width=2)

    button = canvas.create_rectangle(678, 340, 790, 390, width=2, fill="#5e6269")
    button_text = canvas.create_text(734, 365, text="CHECK", font=BUTTON_FONT)

    options = canvas.create_rectangle(670, 25, 790, 75, width=2, fill="#5e6269")
    options_text = canvas.create_text(730, 50, text="OPTIONS", font=BUTTON_FONT)

    colors = {0:"red", 1:"orange", 2:"yellow", 3:"green", 4:"blue", 5:"purple", 6:"pink"}
    check_colors = {"red":False, "orange":False, "yellow":False, "green":False, "blue":False, "purple":False, "pink":False}
    cur_colors = [0, 0, 0, 0]
    for x in range(4):
        circle = canvas.create_oval((200*x)+25, 125, (200*x)+175, 275, width=3, fill=colors[cur_colors[x]])
        circles.append(circle)

    for x in range(4):
        circles_colors_keys.append(randint(0, 6))

    def restart():
        main(max_tries)

    def system_decision(event):
        x, y = event.x, event.y

        if y>215 and y<235:
            if x>230 and x<320:
                restart()
            elif x>350 and x<440:
                exit()
            elif x>470 and x<560:
                home()

    def formulate_fwd(event):
        x, y = event.x, event.y
        circle_index = check_click(x, y)
        if circle_index != None and circle_index != "BUTTON" and circle_index != "OPTIONS":
            cur_colors[circle_index] += 1
            canvas.itemconfig(circles[circle_index], fill=colors[cur_colors[circle_index]%7])

        if circle_index == "BUTTON":
            check_code()

        if circle_index == "OPTIONS":
            show_options()
        
    def formulate_rev(event):
        x, y = event.x, event.y
        circle_index = check_click(x, y)
        if circle_index != None:
            cur_colors[circle_index] -= 1
            canvas.itemconfig(circles[circle_index], fill=colors[cur_colors[circle_index]%7])

    def options_cancel():
        global options_widgets
        for x in range(len(options_widgets)):
            canvas.delete(options_widgets[x])
        canvas.unbind("<Button-1>")
        canvas.bind("<Button-1>", formulate_fwd)
    
    def options_detect(event):
        x, y = event.x, event.y

        if x>260 and x<395:
            if y>155 and y<197.5:
                restart()
            elif y>202.5 and y<245:
                home()
        elif x>405 and x<540:
            if y>155 and y<197.5:
                exit()
            elif y>202.5 and y<245:
                options_cancel()
    
    def show_options():
        canvas.unbind("<Button-1>")
        global options_widgets
        options_panel = canvas.create_rectangle(250, 150, 550, 250, fill="white", width=3)
        
        restart = canvas.create_rectangle(260, 155, 395, 197.5, fill="#5e6269", width=3)
        exit_ = canvas.create_rectangle(405, 155, 540, 197.5, fill="#5e6269", width=3)
        back_home = canvas.create_rectangle(260, 202.5, 395, 245, fill="#5e6269", width=3)
        cancel = canvas.create_rectangle(405, 202.5, 540, 245, fill="#5e6269", width=3)

        restart_text = canvas.create_text(327.5, 175.75, text="RESTART", font=OPTIONS_BUTTON_FONT)
        exit_text = canvas.create_text(472.5, 175.75, text="EXIT", font=OPTIONS_BUTTON_FONT)
        home_text = canvas.create_text(327.5, 223.75, text="HOME", font=OPTIONS_BUTTON_FONT)
        cancel_text = canvas.create_text(472.5, 223.75, text="CANCEL", font=OPTIONS_BUTTON_FONT)
        
        options_widgets = [options_panel, restart, exit_, back_home, cancel,
                           restart_text, exit_text, home_text, cancel_text]

        canvas.bind("<Button-1>", options_detect)
        

    def check_click(x, y):
        index = None
        if y>125 and y<275:
            if x>25 and x<175:
                index = 0
            elif x>225 and x<375:
                index = 1
            elif x>425 and x<575:
                index = 2
            elif x>625 and x<775:
                index = 3

        if (x>678 and x<790) and (y>340 and y<390):
            index = "BUTTON"

        if (x>670 and x<790) and (y>25 and y<75):
            index = "OPTIONS"
        
        
        return index

    def end_game(main, sub):
        canvas.unbind("<Button-1>")
        canvas.unbind("<Button-3>")
        canvas.create_rectangle(200, 150, 600, 250, fill="white", width=3)
        canvas.create_text(400, 175, text=main, font=END_MAIN_FONT)
        canvas.create_text(400, 200, text=sub, font=END_SUB_FONT)

        canvas.create_rectangle(230, 215, 320, 235, fill="grey", width=2)
        canvas.create_text(275, 225, text="RESTART", font=END_BUTTON_FONT)
        canvas.create_rectangle(350, 215, 440, 235, fill="grey", width=2)
        canvas.create_text(395, 225, text="EXIT", font=END_BUTTON_FONT)
        canvas.create_rectangle(470, 215, 560, 235, fill="grey", width=2)
        canvas.create_text(515, 225, text="HOME", font=END_BUTTON_FONT)

        canvas.bind("<Button-1>", system_decision)

    def color_matches(color, users, key):
        check = False
        for x in range(4):
            if users[x] == color and users[x] != color:
                check = False
                break
            if users[x] == key[x] and users[x] == color:
                check = True
        return check

    def check_code():
        global try_count
        for x in range(4):
            user_color = cur_colors[x]%7
            key_color = circles_colors_keys[x]

            #print(user_color, key_color)

            if user_color == key_color:
                checks[x] = "red"
                check_colors[colors[user_color]] = True
            elif user_color != key_color and user_color in circles_colors_keys and check_colors[colors[user_color]] == False and color_matches(user_color, cur_colors, circles_colors_keys) == False:
                checks[x] = "white"
                check_colors[colors[user_color]] = True
            else:
                checks[x] = "grey"

            canvas.create_oval((60*x)+420, 345, (60*x)+460, 385, fill=checks[x], width=3)

        for x in range(7):
            check_colors[colors[x]] = False

        for x in range(4):
            cur_colors[x]%=7
        if cur_colors == circles_colors_keys:
            try_count+=1
            if try_count == 1:
                ntext = " try"
            else:
                ntext = " tries"
            end_game("YOU WIN", "You broke the code in " + str(try_count) + ntext)
        else:
            try_count+=1
            if try_count>max_tries:
                raw_colors = []
                for x in range(4):
                    raw_colors.append(colors[circles_colors_keys[x]])
                end_game("YOU LOSE", "Colors were " + raw_colors[0] + ", " + raw_colors[1] + ", " + raw_colors[2] + ", and " + raw_colors[3])
            add = ""
            if max_tries-try_count == -1:
                add = "?!"
            canvas.itemconfig(try_count_text, text="Number of tries left: " + str(max_tries-try_count) + add)

        print()


    canvas.bind("<Button-1>", formulate_fwd)
    canvas.bind("<Button-3>", formulate_rev)

def home():

    canvas.delete('all')
    TITLE_FONT = ("Courier", 40, "bold")
    AUTHOR_FONT = ("Courier", 10, "italic")
    SUBTITLE_FONT = ("Courier", 20, "underline")
    BUTTON_FONT = ("Courier", 18, "bold")
    BUTTON_SUB_FONT = ("Courier", 10, "italic")
    RULES_FONT = ("Courier", 15, "bold")
    canvas.create_text(400, 40, text="CODEBREAKER", font=TITLE_FONT)
    canvas.create_text(400, 62, text="-- Rohan Kosalge --", font=AUTHOR_FONT)
    canvas.create_text(400, 150, text="Select game difficulty:", font=SUBTITLE_FONT)
    global rules_widgets
    rules_widgets = []

    canvas.create_rectangle(25, 350, 175, 390, width=2, fill="white")
    canvas.create_text(100, 370, text="RULES", font=RULES_FONT)
    canvas.create_rectangle(625, 350, 775, 390, width=2, fill="white")
    canvas.create_text(700, 370, text="EXIT", font=RULES_FONT)

    gamemodes = ["EASY", "NORMAL", "HARD", "IMPOSSIBLE"]
    gamemode_tries = [15, 10, 5, 2]
    for x in range(4):
        canvas.create_rectangle((200*x)+25, 200, (200*x)+175, 300, width=2, fill="#5e6269")
        canvas.create_text((200*x)+100, 250, text=gamemodes[x], font=BUTTON_FONT)
        canvas.create_text((200*x)+100, 315, text="("+str(gamemode_tries[x])+" tries)", font=BUTTON_SUB_FONT)

    def hide_rules(event):
        x, y = event.x, event.y

        if (x>650 and x<775) and (y>325 and y<375):
            #print(rules_widgets)
            for x in range(len(rules_widgets)):
                canvas.delete(rules_widgets[x])
            canvas.unbind("<Button-1>")
            canvas.bind("<Button-1>", choose_gamemode)
    
    def show_rules():
        canvas.unbind("<Button-1>")
        RULES_TITLE_FONT = ("Courier", 30, "bold")
        RULES_TEXT_FONT = ("Courier", 9, "normal")
        RULES_BUTTON_FONT = ("Courier", 20, "bold")
        rules_panel = canvas.create_rectangle(0, 0, 800, 400, fill="white", outline="white")
        rules_title = canvas.create_text(400, 30, text="-- RULES --", font=RULES_TITLE_FONT)

        rules = "Welcome to Codebreaker, where your job is to 'break' the code!\nA random code of four colors is secretly chosen, and it is your mission to find out what the colors are!\nDon't be worried, because you have certain clues to guide you. Each time you 'check' your code, four 'keys'\nare projected (one for each colored circle).\n\nA key can have one of three colors:\n\nred: the color is correct and in the right position\nwhite: the color is correct but in the wrong position\ngrey: the color is wrong and in the wrong position\n\nOnce all keys have turned red, you will have broken the code! You only have a certain number of attempts\nto guess the code. Choose from four gamemodes that specify the given number of attempts: easy, normal, hard, \nor impossible.\n\nControls:\n\nleft-click: change color to the right (red, orange, etc.)\nright-click: change color to the left (orange, red, etc.)\n\nGood-luck and have fun playing Codebreaker!"
        rules_text = canvas.create_text(400, 220, text=rules.upper(), font=RULES_TEXT_FONT)

        ok = canvas.create_rectangle(650, 325, 775, 375, fill="grey", width=2)
        ok_text = canvas.create_text(712.5, 350, text="OK", font=RULES_BUTTON_FONT)

        rules_widgets.append(rules_panel)
        rules_widgets.append(rules_title)
        rules_widgets.append(rules_text)
        rules_widgets.append(ok)
        rules_widgets.append(ok_text)
        print(rules_widgets)

        canvas.bind("<Button-1>", hide_rules)
    
    
    def choose_gamemode(event):
        x, y = event.x, event.y
        main_run_tries = None
        
        if y>200 and y<300:
            if x>25 and x<175:
                main_run_tries = 15
            elif x>225 and x<375:
                main_run_tries = 10
            elif x>425 and x<575:
                main_run_tries = 5
            elif x>625 and x<775:
                main_run_tries = 2

            if main_run_tries != None:
                main(main_run_tries)

        if y>350 and y<390:
            if x>25 and x<175:
                show_rules()
            elif x>625 and x<775:
                exit()


    canvas.bind("<Button-1>", choose_gamemode)
    
home()
