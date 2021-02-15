from tkinter import *
from random import *

master = Tk()
master.title('Kruskal\'s Maze!')

CD = 800
SIZE = 50
CELL = CD/SIZE
WIDTH = 1
CELL_COLOR = "blue"
BORDER_OUTLINE = "black"
BORDER_FILL = "white"
BORDER_WIDTH = 5

canvas = Canvas(master, height=CD+(2*CELL), width=CD+(2*CELL))
canvas.pack()

hlines = []
vlines = []
#nums = {}

global coords
coords = {}

global find_num_from_coords
find_num_from_coords = {}

def drawGrid():

   canvas.create_rectangle(CELL, CELL, CD+CELL, CD+CELL, width=BORDER_WIDTH, outline=BORDER_OUTLINE, fill=BORDER_FILL)
   
   for x in range(SIZE-1):
       vlines.append([])
       for y in range(SIZE):

           vline = canvas.create_line((CELL*x)+(2*CELL), (CELL*y)+CELL, (CELL*x)+(2*CELL), (CELL*y)+(2*CELL), fill=CELL_COLOR, width=WIDTH)
           vlines[x].append(vline)

   for x in range(SIZE):
       hlines.append([])
       for y in range(SIZE-1):

           hline = canvas.create_line((CELL*x)+CELL, (CELL*y)+(2*CELL), (CELL*x)+(2*CELL), (CELL*y)+(2*CELL), fill=CELL_COLOR, width=WIDTH)
           hlines[x].append(hline)

   for x in range(SIZE):
       for y in range(SIZE):
           num = (SIZE*x)+y
           cors = (y, x)
           coords.update({num: [cors]})
           find_num_from_coords.update({cors: num})

           #num_text = canvas.create_text((40*x)+60, (40*y)+60, text=num, font=("Ubuntu", 10, "bold"))
           #nums.update({cors: num_text})

   #print("HLINES: " + str(hlines))
   #print("VLINES: " + str(vlines))

def moveItems(root, passer):
   global coords
   global find_num_from_coords

   passer_cors_list = coords[passer]

   #print("root = %d, passer = %d" %(root, passer))
   #print("Length of passer_cors_list: " + str(len(passer_cors_list)))
   #print("Root: " + str(root))
   #print("Length of coords[root]: " + str(len(coords[root])))
   for cors in passer_cors_list:
       coords[root].append(cors)
       find_num_from_coords[cors] = root

   

   del coords[passer]


def removeLines():
   while len(coords) != 1:

       lines = choice([hlines, vlines])

       if lines == hlines:
          line_x = randint(0, SIZE-2)
          line_y = randint(0, SIZE-1)

          while lines[line_y][line_x] == None:
              line_x = randint(0, SIZE-2)
              line_y = randint(0, SIZE-1)

       else:
          line_x = randint(0, SIZE-1)
          line_y = randint(0, SIZE-2)

          while lines[line_y][line_x] == None:
              line_x = randint(0, SIZE-1)
              line_y = randint(0, SIZE-2)
      

       line = lines[line_y][line_x]

       if lines == hlines:
           num1, num2 = find_num_from_coords[(line_x, line_y)], find_num_from_coords[(line_x+1, line_y)]
       else:
           num1, num2 = find_num_from_coords[(line_x, line_y)], find_num_from_coords[(line_x, line_y+1)]

       if num1 == num2:
          continue
       

       moveItems(min([num1, num2]), max([num1, num2]))

       canvas.delete(line)
       canvas.update()
       canvas.update_idletasks()

       #print(coords)
       lines[line_y][line_x] = None


       #print("LENGTH OF COORDS: " + str(len(coords)))



drawGrid()
#print(coords)

removeLines()

mainloop()
