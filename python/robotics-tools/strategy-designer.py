from tkinter import *
from tkinter.colorchooser import *
from time import sleep
from PIL import ImageTk, Image

master = Tk()
master.title("VEX Strategy Designer: 2020-21 Season (\"Change Up!\")")

canvas = Canvas(height=800, width=800, bd=0, highlightthickness=0, bg="dark grey")
canvas.grid(row=0, column=0)

controls = Canvas(height=800, width=400, bd=0, highlightthickness=0, bg="black")
controls.grid(row=0, column=1)

handle = open("/Users/rohankosalge/Downloads/Skills Designs.txt", "w+")
data = handle.read().splitlines()


TITLE_FONT = ("Ubuntu", 25, "bold")
HEADER_FONT = ("Ubuntu", 20, "bold underline")
SUB_HEADER_FONT = ("Ubuntu", 18, "bold italic")
WIDGET_FONT = ("Ubuntu", 15, "bold")
BIG_BUTTON_FONT = ("Ubuntu", 25, "bold")

global balls
balls = []

deleted_balls = []

global balls_cors
balls_cors = []

global deleted_balls_cors
deleted_balls_cors = []

global arrows
arrows = []

global arrow_cors
arrow_cors = []

global deleted_arrows
deleted_arrows = []

global deleted_arrows_cors
deleted_arrows_cors = []

global ball_insert_state
ball_insert_state = "enabled"

global draw_state
draw_state = "arrow"

global prev_draw_state
prev_draw_state = draw_state

global oldx
global oldy
global freeline


class Pen:
    # simple pen class with width and color attributes.

    def __init__(self, width, color):
        self.width = width
        self.color = color

    def set_width(self, width):
        self.width = width

    def get_width(self):
        return self.width

    def set_color(self, color):
        self.color = color

    def get_color(self):
        return self.color


p = Pen(width=5, color="black")


class FieldElement:

    def __init__(self, basecors, baseposs):
        self.y, self.x = basecors[0] - 20, basecors[1] - 20
        self.fieldx, self.fieldy = baseposs[0], baseposs[1]

    def draw_ball_topleft(self, color):
        if self.fieldx == 0 and self.fieldy == 0:
            balls.append(
                canvas.create_oval(self.y + 20, self.x + 20, self.y + 60, self.x + 60, width=3, outline="black",
                                   fill=color))
        elif self.fieldx == 0 and self.fieldy != 0:
            balls.append(
                canvas.create_oval(self.y, self.x + 20, self.y + 40, self.x + 60, width=3, outline="black", fill=color))
        elif self.fieldx != 0 and self.fieldy == 0:
            balls.append(
                canvas.create_oval(self.y + 20, self.x, self.y + 60, self.x + 40, width=3, outline="black", fill=color))
        else:
            balls.append(
                canvas.create_oval(self.y, self.x, self.y + 40, self.x + 40, width=3, outline="black", fill=color))

    def draw_ball_topright(self, color):
        if self.fieldx == 0 and self.fieldy == 5:
            balls.append(
                canvas.create_oval(self.y + (800 / 6) - 20, self.x + 20, self.y + (800 / 6) + 20, self.x + 60, width=3,
                                   outline="black", fill=color))
        elif self.fieldx != 0 and self.fieldy == 5:
            balls.append(
                canvas.create_oval(self.y + (800 / 6) - 20, self.x, self.y + (800 / 6) + 20, self.x + 40, width=3,
                                   outline="black", fill=color))
        elif self.fieldx == 0 and self.fieldy != 5:
            balls.append(canvas.create_oval(self.y + (800 / 6), self.x + 20, self.y + (800 / 6) + 40, self.x + 60, width=3,
                                   outline="black", fill=color))
        else:
            balls.append(canvas.create_oval(self.y + (800 / 6), self.x, self.y + (800 / 6) + 40, self.x + 40, width=3,
                                            outline="black", fill=color))

    def draw_ball_bottomleft(self, color):
        if self.fieldx == 5 and self.fieldy == 0:
            balls.append(
                canvas.create_oval(self.y + 20, self.x + (800 / 6) - 20, self.y + 60, self.x + (800 / 6) + 20, width=3,
                                   outline="black", fill=color))
        elif self.fieldx != 5 and self.fieldy == 0:
            balls.append(
                canvas.create_oval(self.y + 20, self.x + (800 / 6), self.y + 60, self.x + (800 / 6) + 40, width=3,
                                   outline="black", fill=color))
        elif self.fieldx == 5 and self.fieldy != 0:
            balls.append(
                canvas.create_oval(self.y, self.x + (800 / 6) - 20, self.y + 40, self.x + (800 / 6) + 20, width=3,
                                   outline="black", fill=color))
        else:
            balls.append(canvas.create_oval(self.y, self.x + (800 / 6), self.y + 40, self.x + (800 / 6) + 40, width=3,
                                            outline="black", fill=color))

    def draw_ball_bottomright(self, color):
        if self.fieldx == 5 and self.fieldy == 5:
            balls.append(canvas.create_oval(self.y + (800 / 6) - 20, self.x + (800 / 6) - 20, self.y + 20 + (800 / 6),
                                            self.x + (800 / 6) + 20, width=3, outline="black", fill=color))
        elif self.fieldx != 5 and self.fieldy == 5:
            balls.append(canvas.create_oval(self.y + (800 / 6) - 20, self.x + (800 / 6), self.y + 20 + (800 / 6),
                                            self.x + (800 / 6) + 40, width=3, outline="black", fill=color))
        elif self.fieldx == 5 and self.fieldy != 5:
            balls.append(canvas.create_oval(self.y + (800 / 6), self.x + (800 / 6) - 20, self.y + 40 + (800 / 6),
                                            self.x + (800 / 6) + 20, width=3, outline="black", fill=color))
        else:
            balls.append(canvas.create_oval(self.y + (800 / 6), self.x + (800 / 6), self.y + 40 + (800 / 6),
                                            self.x + (800 / 6) + 40, width=3, outline="black", fill=color))

    def draw_ball_left(self, color):
        if self.fieldy == 0:
            balls.append(
                canvas.create_oval(self.y + 20, self.x + (400 / 6), self.y + 60, self.x + 40 + (400 / 6), width=3,
                                   outline="black", fill=color))
        else:
            balls.append(canvas.create_oval(self.y, self.x + (400 / 6), self.y + 40, self.x + 40 + (400 / 6), width=3,
                                            outline="black", fill=color))

    def draw_ball_up(self, color):
        if self.fieldx == 0:
            balls.append(canvas.create_oval(self.y + (400 / 6), self.x + 20, self.y + 40 + (400 / 6), self.x + 60, width=3,
                                   outline="black", fill=color))
        else:
            balls.append(canvas.create_oval(self.y + (400 / 6), self.x, self.y + 40 + (400 / 6), self.x + 40, width=3,
                                            outline="black", fill=color))

    def draw_ball_right(self, color):
        if self.fieldy == 5:
            balls.append(canvas.create_oval(self.y + (800 / 6) - 20, self.x + (400 / 6), self.y + (800 / 6) + 20,
                                            self.x + 40 + (400 / 6), width=3, outline="black", fill=color))
        else:
            balls.append(canvas.create_oval(self.y + (800 / 6), self.x + (400 / 6), self.y + 40 + (800 / 6),
                                            self.x + 40 + (400 / 6), width=3, outline="black", fill=color))

    def draw_ball_down(self, color):
        if self.fieldx == 5:
            balls.append(canvas.create_oval(self.y + (400 / 6), self.x + (800 / 6) - 20, self.y + 40 + (400 / 6),
                                            self.x + 20 + (800 / 6), width=3, outline="black", fill=color))
        else:
            balls.append(canvas.create_oval(self.y + (400 / 6), self.x + (800 / 6), self.y + 40 + (400 / 6),
                                            self.x + 40 + (800 / 6), width=3, outline="black", fill=color))

    def draw_ball_center(self, color):
        balls.append(canvas.create_oval(self.y + (400 / 6), self.x + (400 / 6), self.y + (400 / 6) + 40,
                                        self.x + (400 / 6) + 40, width=3, outline="black", fill=color))




field_elements = []

for x in range(6):
    field_elements.append([])
    for y in range(6):
        canvas.create_rectangle((800 / 6) * y, (800 / 6) * x, (800 / 6) * y + (800 / 6), (800 / 6) * x + (800 / 6),
                                width=2, outline="black", fill="dark grey")
        field_element = FieldElement(((800 / 6) * y, (800 / 6) * x), (x, y))
        field_elements[x].append(field_element)

for x in range(3):
    for y in range(3):
        canvas.create_oval(380 * y, 380 * x, (380 * y) + 40, (380 * x) + 40, width=3, outline="black", fill="grey")


def round_rectangle(x1, y1, x2, y2, w, r, **kwargs):
    x1+=w
    y1+=w
    x2-=w
    y2-=w
    points = (x1+r, y1, x1+r, y1, x2-r, y1, x2-r, y1, x2, y1, x2, y1+r, x2, y1+r, x2, y2-r, x2, y2-r, x2, y2, x2-r, y2, x2-r, y2, x1+r, y2, x1+r, y2, x1, y2, x1, y2-r, x1, y2-r, x1, y1+r, x1, y1+r, x1, y1)
    return controls.create_polygon(points, **kwargs, smooth=True)


controls.create_text(200, 20, text="VEX STRAT DESIGN", font=TITLE_FONT, fill="white")

round_rectangle(15, 40, 385, 410, 0, 15, outline="white", width=5)
#controls.create_rectangle(15, 40, 385, 410, fill="black", outline="white", width=3)
round_rectangle(15, 420, 385, 790, 0, 15, outline="white", width=5)
#controls.create_rectangle(15, 420, 385, 790, fill="black", outline="white", width=3)
#round_rectangle(395, 40, 635, 410, 0, 15, outline="white", width=5)
#round_rectangle(395, 420, 635, 790, 0, 15, outline="white", width=5)


controls.create_text(25, 55, text="Add Ball", font=HEADER_FONT, fill="white", anchor=W)



ball_color = StringVar(master)
ball_color.set("red")
choose_red = Radiobutton(master, text="RED", variable=ball_color, value="red", bg="black", fg="red", font=WIDGET_FONT)
choose_blue = Radiobutton(master, text="BLUE", variable=ball_color, value="blue", bg="black", fg="blue",
                          font=WIDGET_FONT)

controls.create_text(25, 90, text="Choose Color:", font=SUB_HEADER_FONT, fill="white", anchor=W)
controls.create_window(60, 120, window=choose_red)
controls.create_window(145, 120, window=choose_blue)

row, col = IntVar(master), IntVar(master)
row.set(1)
col.set(1)
rows = OptionMenu(master, row, 1, 2, 3, 4, 5, 6)
rows.config(bg="black", font=WIDGET_FONT)
cols = OptionMenu(master, col, 1, 2, 3, 4, 5, 6)
cols.config(bg="black", font=WIDGET_FONT)

controls.create_text(25, 160, text="Field Element:", font=SUB_HEADER_FONT, fill="white", anchor=W)
controls.create_text(25, 195, text="Row:", font=WIDGET_FONT, anchor=W, fill="white")
controls.create_window(75, 195, window=rows, anchor=W)
controls.create_text(25, 220, text="Column:", font=WIDGET_FONT, anchor=W, fill="white")
controls.create_window(100, 220, window=cols, anchor=W)

pos = StringVar(master)
pos.set("Top Left")
positions = OptionMenu(master, pos, "Left", "Up", "Right", "Down", "Top Left", "Top Right", "Bottom Left",
                       "Bottom Right", "Center")
positions.config(bg="black", font=WIDGET_FONT)

controls.create_text(25, 260, text="Choose Position:", font=SUB_HEADER_FONT, fill="white", anchor=W)
controls.create_window(25, 290, window=positions, anchor=W)

round_rectangle(200, 245, 370, 320, 5, 10, outline="white", width=5)
controls.create_text(285, 282.5, text="INSERT BALL", font=WIDGET_FONT, fill="white")

round_rectangle(200, 325, 370, 400, 5, 10, outline="white", width=5)
controls.create_text(285, 362.5, text="INSERT LAYOUT", font=WIDGET_FONT, fill="white")

enablebox1 = round_rectangle(200, 50, 282.5, 100, 5, 10, outline="grey", width=5)
enabletext1 = controls.create_text(241.25, 75, text="ENABLE", font=WIDGET_FONT, fill="grey")

disablebox1 = round_rectangle(287.5, 50, 370, 100, 5, 10, outline="white", width=5)
disabletext1 = controls.create_text(328.75, 75, text="DISABLE", font=WIDGET_FONT, fill="white")

round_rectangle(200, 105, 370, 152.5, 5, 10, outline="yellow", width=5)
controls.create_text(285, 128.75, text="UNDO", font=WIDGET_FONT, fill="yellow")

round_rectangle(200, 157.5, 370, 205, 5, 10, outline="yellow", width=5)
controls.create_text(285, 181.25, text="REDO", font=WIDGET_FONT, fill="yellow")

round_rectangle(200, 210, 370, 240, 5, 10, outline="red", width=5)
controls.create_text(285, 225, text="DELETE ALL", font=WIDGET_FONT, fill="red")

controls.create_text(25, 330, text="Add Ball Layout:", font=SUB_HEADER_FONT, fill="white", anchor=W)
layout_text = Text(master, font=WIDGET_FONT, width=14, height=2)
controls.create_window(25, 350, window=layout_text, anchor=NW)

global width_var
width_var = IntVar()
width_var.set(5)


def change_width():
    global width_var
    p.set_width(width_var.get())


def change_color():
    color = askcolor()[1]
    p.set_color(color)


controls.create_text(25, 435, text="Draw Stuff", font=HEADER_FONT, fill="white", anchor=W)

typebox1 = round_rectangle(25, 460, 105, 505, 5, 10, outline="grey", width=5)
typetext1 = controls.create_line(35, 482.5, 95, 482.5, width=3, arrow="last", fill="grey")
typebox2 = round_rectangle(110, 460, 190, 505, 5, 10, outline="white", width=5)
typetext2 = controls.create_text(150, 482.5, text="FREE", font=WIDGET_FONT, fill="white")

enablebox2 = round_rectangle(200, 430, 282.5, 480, 5, 10, outline="grey", width=5)
disablebox2 = round_rectangle(287.5, 430, 370, 480, 5, 10, outline="white", width=5)
enabletext2 = controls.create_text(241.25, 455, text="ENABLE", font=WIDGET_FONT, fill="grey")
disabletext2 =controls.create_text(328.75, 455, text="DISABLE", font=WIDGET_FONT, fill="white")

controls.create_text(25, 525, text="Change Width:", font=SUB_HEADER_FONT, fill="white", anchor=W)

change_width_box = Spinbox(master, textvariable=width_var, from_=1, to=25, command=change_width, font=WIDGET_FONT,
                           bg="black", fg="white", width=13)
controls.create_window(112, 570, window=change_width_box)

controls.create_text(25, 620, text="Change Color:", fill="white", font=SUB_HEADER_FONT, anchor=W)
change_color_box = Button(master, text="Open Color UI", command=change_color, font=WIDGET_FONT)
controls.create_window(30, 650, window=change_color_box, anchor=W)

round_rectangle(25, 680, 190, 780, 5, 10, outline="red", width=5)
controls.create_text(110, 730, text="ERASE ALL", font=BIG_BUTTON_FONT, fill="red")

round_rectangle(200, 490, 370, 630, 5, 10, outline="yellow", width=5)
controls.create_text(285, 560, text="UNDO", font=BIG_BUTTON_FONT, fill="yellow")

round_rectangle(200, 640, 370, 780, 5, 10, outline="yellow", width=5)
controls.create_text(285, 710, text="REDO", font=BIG_BUTTON_FONT, fill="yellow")


controls.create_text(405, 55, text="Open/Save Design", font=HEADER_FONT, anchor=W, fill="white")
controls.create_text(405, 435, text="Robot/Pointers", font=HEADER_FONT, anchor=W, fill="white")


#   round_rectangle()

def place_ball(color, x, y, p):
    tile = field_elements[x][y]

    if p == "Left":
        tile.draw_ball_left(color)
    elif p == "Up":
        tile.draw_ball_up(color)
    elif p == "Right":
        tile.draw_ball_right(color)
    elif p == "Down":
        tile.draw_ball_down(color)
    elif p == "Top Left":
        tile.draw_ball_topleft(color)
    elif p == "Top Right":
        tile.draw_ball_topright(color)
    elif p == "Bottom Left":
        tile.draw_ball_bottomleft(color)
    elif p == "Bottom Right":
        tile.draw_ball_bottomright(color)
    else:
        tile.draw_ball_center(color)

    global balls_cors
    balls_cors.append((tile, p, color))


def check_button_press(event):
    global ball_insert_state
    global draw_state
    global prev_draw_state
    x, y = event.x, event.y

    if x >= 200 and x <= 282.5 and y >= 50 and y <= 100:
        ball_insert_state = "enabled"
        controls.itemconfig(enablebox1, outline="grey")
        controls.itemconfig(disablebox1, outline="white")
        controls.itemconfig(enabletext1, fill="grey")
        controls.itemconfig(disabletext1, fill="white")

    elif x >= 287.5 and x <= 370 and y >= 50 and y <= 100:
        ball_insert_state = "disabled"
        controls.itemconfig(enablebox1, outline="white")
        controls.itemconfig(disablebox1, outline="grey")
        controls.itemconfig(enabletext1, fill="white")
        controls.itemconfig(disabletext1, fill="grey")

    elif x >= 200 and x <= 370 and y >= 245 and y <= 320:
        if ball_insert_state == "enabled":
            color = ball_color.get()
            r, c = row.get() - 1, col.get() - 1
            tile = field_elements[r][c]
            p = pos.get()

            if p == "Left":
                tile.draw_ball_left(color)
            elif p == "Up":
                tile.draw_ball_up(color)
            elif p == "Right":
                tile.draw_ball_right(color)
            elif p == "Down":
                tile.draw_ball_down(color)
            elif p == "Top Left":
                tile.draw_ball_topleft(color)
            elif p == "Top Right":
                tile.draw_ball_topright(color)
            elif p == "Bottom Left":
                tile.draw_ball_bottomleft(color)
            elif p == "Bottom Right":
                tile.draw_ball_bottomright(color)
            else:
                tile.draw_ball_center(color)

            global balls_cors
            balls_cors.append((tile, p, color))

    elif x >= 200 and x <= 370 and y >= 105 and y <= 152.5:
        if len(balls) != 0 and ball_insert_state == "enabled":
            deleted_ball = balls.pop(-1)
            canvas.delete(deleted_ball)
            deleted_balls.append(deleted_ball)
            deleted_ball_cors = balls_cors.pop(-1)
            deleted_balls_cors.append(deleted_ball_cors)
            # print(deleted_balls)

    elif x >= 200 and x <= 370 and y >= 157.5 and y <= 205:
        if len(deleted_balls) != 0 and ball_insert_state == "enabled":
            deleted_balls.pop(-1)
            retained_ball_cors = deleted_balls_cors.pop(-1)
            tile, p, color = retained_ball_cors[0], retained_ball_cors[1], retained_ball_cors[2]

            if p == "Left":
                tile.draw_ball_left(color)
            elif p == "Up":
                tile.draw_ball_up(color)
            elif p == "Right":
                tile.draw_ball_right(color)
            elif p == "Down":
                tile.draw_ball_down(color)
            elif p == "Top Left":
                tile.draw_ball_topleft(color)
            elif p == "Top Right":
                tile.draw_ball_topright(color)
            elif p == "Bottom Left":
                tile.draw_ball_bottomleft(color)
            elif p == "Bottom Right":
                tile.draw_ball_bottomright(color)
            else:
                tile.draw_ball_center(color)

            balls_cors.append(retained_ball_cors)

    elif x >= 200 and x <= 370 and y >= 325 and y <= 400:
        if ball_insert_state == "enabled":
            layout = layout_text.get("1.0", "1.end")

            layout_balls = layout.split(", ")
            sym_to_color = {'b': 'blue', 'r': 'red'}
            sym_to_pos = {'l': 'Left', 'u': 'Up', 'r': 'Right', 'd': 'Down', 'tl': 'Top Left', 'tr': 'Top Right',
                          'bl': 'Bottom Left', 'br': 'Bottom Right', 'c': 'Center'}

            print(layout_balls)

            for ball in layout_balls:
                color = sym_to_color[ball[0]]
                x, y = int(ball[1])-1, int(ball[2])-1
                position = sym_to_pos[ball[3:]]
                place_ball(color, x, y, position)



    elif x >= 200 and x <= 370 and y >= 210 and y <= 240:
        if len(balls) != 0 and ball_insert_state == "enabled":
            for x in range(len(balls)):
                deleted_ball = balls.pop(-1)
                canvas.delete(deleted_ball)
                deleted_balls.append(deleted_ball)
                print("here-io like a cheerio")

    elif x >= 30 and x <= 240 and y >= 680 and y <= 780:
        # print("here")

        # print(len(arrows))
        # print(arrows)

        for i in range(len(arrows)):
            print(i)
            arrow = arrows[i]
            if len(arrow) == 1:
                canvas.delete(arrow[0])
            else:
                for freeline in arrow:
                    canvas.delete(freeline)
            deleted_arrows.append(arrow)

        arrows.clear()

        for ac in arrow_cors:
            deleted_arrows_cors.append(ac)

        arrow_cors.clear()

        # for arrow, ac in arrows, arrow_cors:
        #    canvas.delete(arrow)
        #    arrows.remove(arrow)
        #    deleted_arrows.append(arrow)
        #    arrow_cors.remove(ac)
        #    deleted_arrows_cors.append(ac)
        print(len(deleted_arrows_cors))

    elif x >= 25 and x <= 105 and y >= 460 and y <= 505:
        if draw_state != None:
            controls.itemconfig(typebox1, outline="gray")
            controls.itemconfig(typebox2, outline="white")
            controls.itemconfig(typetext1, fill="gray")
            controls.itemconfig(typetext2, fill="white")
            draw_state = "arrow"

            canvas.unbind("<ButtonPress-1>")
            canvas.unbind("<B1-Motion>")
            canvas.unbind("<ButtonRelease-1>")

            canvas.bind("<ButtonPress-1>", setstartcors)
            canvas.bind("<B1-Motion>", setmidcors)
            canvas.bind("<ButtonRelease-1>", setendcors)


    elif x >= 110 and x <= 190 and y >= 460 and y <= 505:
        if draw_state != None:
            controls.itemconfig(typebox1, outline="white")
            controls.itemconfig(typebox2, outline="gray")
            controls.itemconfig(typetext1, fill="white")
            controls.itemconfig(typetext2, fill="gray")
            draw_state = "free"

            canvas.unbind("<ButtonPress-1>")
            canvas.unbind("<B1-Motion>")
            canvas.unbind("<ButtonRelease-1>")

            canvas.bind("<ButtonPress-1>", start)
            canvas.bind("<B1-Motion>", update)
            canvas.bind("<ButtonRelease-1>", finish)

    elif x >= 200 and x <= 282.5 and y >= 430 and y <= 480:
        if prev_draw_state == "arrow":
            draw_state = "arrow"
            canvas.bind("<ButtonPress-1>", setstartcors)
            canvas.bind("<B1-Motion>", setmidcors)
            canvas.bind("<ButtonRelease-1>", setendcors)
        elif prev_draw_state == "free":
            draw_state = "free"
            canvas.bind("<ButtonPress-1>", start)
            canvas.bind("<B1-Motion>", update)
            canvas.bind("<ButtonRelease-1>", finish)

        controls.itemconfig(enablebox2, outline="grey")
        controls.itemconfig(disablebox2, outline="white")
        controls.itemconfig(enabletext2, fill="grey")
        controls.itemconfig(disabletext2, fill="white")

    elif x >= 287.5 and x <= 370 and y >= 430 and y <= 480:
        canvas.unbind("<ButtonPress-1>")
        canvas.unbind("<B1-Motion>")
        canvas.unbind("<ButtonRelease-1>")
        prev_draw_state = draw_state
        draw_state = None

        controls.itemconfig(enablebox2, outline="white")
        controls.itemconfig(disablebox2, outline="grey")
        controls.itemconfig(enabletext2, fill="white")
        controls.itemconfig(disabletext2, fill="grey")

    elif x >= 200 and x <= 370 and y >= 490 and y <= 630:
        if len(arrows) != 0:
            deleted_arrow = arrows.pop(-1)
            deleted_arrow_cors = arrow_cors.pop(-1)

            if len(deleted_arrow) == 1:
                canvas.delete(deleted_arrow[0])
            else:
                for line in deleted_arrow:
                    canvas.delete(line)


            deleted_arrows.append(deleted_arrow)
            deleted_arrows_cors.append(deleted_arrow_cors)


    elif x >= 200 and x <= 370 and y >= 640 and y <= 780:
        # print(len(deleted_arrows))
        # print(deleted_arrows)
        if len(deleted_arrows) != 0:
            retained_arrow = deleted_arrows.pop(-1)
            retained_arrow_cors = deleted_arrows_cors.pop(-1)
            arrow_cors.append(retained_arrow_cors)

            if len(retained_arrow) == 1:
                sc, ec, w, c, a = retained_arrow_cors[0], retained_arrow_cors[1], retained_arrow_cors[2], \
                                  retained_arrow_cors[3], retained_arrow_cors[4]
                retained_arrow[0] = canvas.create_line(sc, ec, width=w, fill=c, arrow=a)

            else:
                retained_arrow.clear()
                flc, w, c = retained_arrow_cors[0], retained_arrow_cors[1], retained_arrow_cors[2]

                for cors in flc:
                    freeline = canvas.create_line(cors, width=w, fill=c)
                    retained_arrow.append(freeline)

            arrows.append(retained_arrow)

global startcors
startcors = []

global endcors
endcors = []

global line


def setstartcors(event):
    global startcors
    global line
    startcors.clear()
    startcors.append(event.x)
    startcors.append(event.y)

    arrows.append([])

    line = canvas.create_line(startcors, startcors, width=p.get_width(), fill=p.get_color(), arrow="last")


def setmidcors(event):
    global endcors
    endcors.clear()
    endcors.append(event.x)
    endcors.append(event.y)

    global line
    canvas.delete(line)
    line = canvas.create_line(startcors, endcors, width=p.get_width(), fill=p.get_color(), arrow="last")


def setendcors(event):
    global endcors
    endcors.clear()
    endcors.append(event.x)
    endcors.append(event.y)

    global line
    canvas.delete(line)

    line = canvas.create_line(startcors, endcors, width=p.get_width(), fill=p.get_color(), arrow="last")
    global arrow_cors
    arrow_cors.append((startcors, endcors, p.get_width(), p.get_color(), "last", 0, "round", "false"))

    global arrows
    arrows[-1].append(line)

    print(arrows)
    print(arrow_cors)


global freelinecors
freelinecors = []


def create_freeline(c1, c2, c3, c4, condition):
    global freeline
    global freelinecors

    freelinecors.append((c1, c2, c3, c4))

    freeline = canvas.create_line(c1, c2, c3, c4, splinesteps=360, capstyle="round", smooth="true", width=p.get_width(),
                                  fill=p.get_color())

    arrows[-1].append(freeline)

    if condition == "finish":
        #print(arrows)
        # print("i'm here lmao")
        arrow_cors.append((freelinecors, p.get_width(), p.get_color()))
        print(arrow_cors)


def start(event):
    global freelinecors
    freelinecors.clear()
    global oldx
    global oldy
    oldx, oldy = event.x, event.y

    arrows.append([])


def update(event):
    global oldx
    global oldy
    create_freeline(oldx, oldy, event.x, event.y, "update")
    oldx, oldy = event.x, event.y


def finish(event):
    global oldx
    global oldy
    create_freeline(oldx, oldy, event.x, event.y, "finish")
    oldx, oldy = None, None



controls.bind("<Button-1>", check_button_press)

canvas.bind("<ButtonPress-1>", setstartcors)
canvas.bind("<B1-Motion>", setmidcors)
canvas.bind("<ButtonRelease-1>", setendcors)

mainloop()
