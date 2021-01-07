# NOTE: Code author- Alberto Alvarez

from tkinter import *
from tkinter.colorchooser import askcolor
from tkinter.filedialog import *
from pyautogui import *
from PIL import ImageGrab, Image, ImageTk
from random import randrange


# NOTE: Code with overall GUI Containers

# Main window

root = Tk()
root.title('PyPaint')
root.iconphoto(False, PhotoImage(file='icon.png'))
w = root.winfo_screenwidth()-9  # TODO: fix weird width
h = root.winfo_screenheight()
root.geometry('%dx%d+%d+%d' % (w, h, 0, 0))
MAINBG = 'gray84'
root.configure(background=MAINBG)

# Toolbox frame containing all of the tools

toolbox = Frame(root)
toolbox.grid(padx=10, pady=10, sticky=E+W)

root.grid_rowconfigure(0, weight=1)

# Canvas for drawing

canvas = Canvas(root)
canvas.grid(row=1, padx=10, pady=10, sticky=N+E+S+W)

root.grid_rowconfigure(1, weight=10)
root.grid_columnconfigure(0, weight=1)

# NOTE: Global values holding information about the type of tool the user is using

# Tools:
# -1: None selected
# 0: Eraser
# 1: Color Dropper
# 2: Line Tool
# 3: Ellipse Tool

tool = -1

# x and y coordinates for line tool
initx = 0
inity = 0

# Brushes:
# 0 - Brush
# 1 - Calligraphy Brush 1
# 2 - Calligraphy Brush 2
# 3 - Spray

brush = 0

# Brush Color and Size
color = '#000000'
size = 5

# NOTE: Program Methods


# Method for changing tool
def changetool(n):
    global tool
    global brush
    tool = n
    brush = 0


# Method for changing brush
def changebrush(n):
    global brush
    global tool
    brush = n
    tool = -1


# Method for choosing color
def choosecolor():
    global color
    color = askcolor()[1]


# Method for saving files
def filesave():
    direc = asksaveasfilename(defaultextension='.png', filetypes=(('PNG Image', '*.png'), ('JPG Image', '.jpg')))

    if direc is None:
        return

    topleftx = root.winfo_rootx()+canvas.winfo_x()
    toplefty = root.winfo_rooty()+canvas.winfo_y()
    bottomrightx = topleftx + canvas.winfo_width()
    bottomrighty = toplefty+canvas.winfo_height()
    ImageGrab.grab().crop((topleftx, toplefty, bottomrightx, bottomrighty)).save(direc)


# Method for drawing that is called whenever the mouse is clicked on the canvas
# clickevent is for listening to mouse release (-1 is release, 1 is press)
def draw(event):
    clickevent = None
    if 'ButtonRelease' in str(event):
        clickevent = -1
    if 'ButtonPress' in str(event):
        clickevent = 1

    xpos, ypos = event.x, event.y
    global brush
    global tool
    global size

    size = slider.get()

    c = None
    if tool == 0:
        c = '#f0f0f0'
    else:
        global color
        c = color

    if tool < 1:
        if brush == 0:
            canvas.create_oval(xpos-size, ypos-size, xpos+size, ypos+size, outline=c, fill=c)
        elif brush == 1:
            canvas.create_line(xpos-size, ypos-size, xpos+size, ypos+size, fill=c)
        elif brush == 2:
            canvas.create_line(xpos-size, ypos+size, xpos+size, ypos-size, fill=c)
        elif brush == 3:
            var = size
            for i in range(10):
                xrand = randrange(xpos-var, xpos+var, 1)
                yrand = randrange(ypos-var, ypos+var, 1)
                canvas.create_rectangle(xrand-1, yrand-1, xrand+1, yrand+1, outline=c, fill=c)
    else:
        if tool == 1:
            xpos, ypos = position()  # Have to reassign pos for use with pyautogui
            RGB = screenshot().getpixel((xpos, ypos))
            color = "#%02x%02x%02x" % RGB  # Convert from RGB to hex
        elif tool == 2 or tool == 3:
            global initx
            global inity
            if clickevent == 1:
                initx = xpos
                inity = ypos
            elif clickevent == -1:
                if tool == 2:
                    canvas.create_line(initx, inity, xpos, ypos, width=size, fill=c)
                elif tool == 3:
                    canvas.create_oval(initx, inity, xpos, ypos, width=size, outline=c)


# NOTE: GUI interfaces for toolbox

brushes = Frame(toolbox)
brushes.grid(row=0, column=0, padx=5, pady=5, sticky=E+W)
Label(brushes, text='Brushes').grid(row=0, column=1, columnspan=2, padx=5, pady=5, sticky=E+W)
Button(brushes, text='Brush', command=lambda: changebrush(0)).grid(row=1, column=0)
Button(brushes, text='Calligraphy Brush 1', command=lambda: changebrush(1)).grid(row=1, column=1)
Button(brushes, text='Calligraphy Brush 2', command=lambda: changebrush(2)).grid(row=1, column=2)
Button(brushes, text='Spray', command=lambda: changebrush(3)).grid(row=1, column=3)

tools = Frame(toolbox)
tools.grid(row=0, column=1, padx=100, pady=5, sticky=E+W)
Label(tools, text='Tools').grid(row=0, column=1, columnspan=2, padx=5, pady=5, sticky=E+W)
Button(tools, text='Eraser', command=lambda: changetool(0)).grid(row=1, column=0)
Button(tools, text='Color Dropper', command=lambda: changetool(1)).grid(row=1, column=1)
Button(tools, text='Line Tool', command=lambda: changetool(2)).grid(row=1, column=2)
Button(tools, text='Ellipse Tool', command=lambda: changetool(3)).grid(row=1, column=3)

sliderframe = Frame(toolbox)
sliderframe.grid(row=0, column=2, padx=100, pady=5, sticky=E+W)
Label(sliderframe, text='Brush Size').grid(padx=5, pady=5, sticky=E+W)
slider = Scale(sliderframe, from_=1, to=100, orient=HORIZONTAL)
slider.grid(row=1, sticky=E+W)

colorframe = Frame(toolbox)
colorframe.grid(row=0, column=3, padx=100, pady=5, sticky=E+W)
Label(colorframe, text='Choose Color').grid(row=0, column=0, padx=5, pady=5, sticky=E+W)
colorwheel = PhotoImage(file='colorwheel.png')
Button(colorframe, image=colorwheel, command=choosecolor, width=1, height=25).grid(row=1, column=0, padx=5, pady=5, sticky=E+W)

filebuttons = Frame(toolbox)
filebuttons.grid(row=0, column=4, padx=100, pady=5, sticky=E+W)
Button(filebuttons, text='Save File', command=filesave).grid(row=0, column=0, padx=5, pady=5, sticky=E+W)

canvas.bind(sequence='<Button-1>', func=draw)
canvas.bind(sequence='<ButtonRelease-1>', func=draw)
canvas.bind(sequence='<B1-Motion>', func=draw)
root.mainloop()
