#!/usr/bin/env python3

from random import randint
from threading import Timer
from time import sleep

try:
    # for Python2
    import Tkinter as tkinter  ## notice capitalized T in Tkinter
except ImportError:
    # for Python3
    import tkinter  ## notice lowercase 't' in tkinter here

# Set useful constants
PIXEL_SIZE=4 # multiply all the drawings by this value
WINDOW_WIDTH=100
WINDOW_HEIGHT=100
TRACK_SIZE=WINDOW_WIDTH/4
MOBILITY=TRACK_SIZE/6
TERRAIN_FG_COLOR="black"
TERRAIN_BG_COLOR="white"
SPEED=60

# Create the GUI
# - create window
root_window = tkinter.Tk()
root_window.configure(background=TERRAIN_BG_COLOR)
# - add canvas
canvas = tkinter.Canvas(root_window, width=500, height=500)
canvas.pack()

terrain = None
last_center = None
player_pos = None
timer = None
# TODO: make game go faster with time!

# Quits the game (called on click on "Quit" button)
def quitf():
    timer.stop()
    root_window.destroy()

# - add quit button to the GUI
quit_button = tkinter.Button(root_window, text="Exit",
                             command=quitf)
quit_button.pack()

# Resets the game parameters (called on click on "Reset" button)
def start_game():
    global terrain, last_center
    terrain, last_center = init_terrain()
    player_pos = last_center
    score = 0
    sleep(20);
    update_terrain(terrain, last_center, player_pos, score)

# - add start_game button to the GUI
reset_button = tkinter.Button(root_window, text="Start/Reset",
                              command=start_game)
reset_button.pack()

# Moves player to the left
## TODO: optimize: make a single function that tests key pressed and acts accordingly
def move_left(event):
    print(event)
    global player_pos
    player_pos = player_pos-1
    if check_player_dead(terrain, player_pos):
        timer.stop()
    else:
        canvas.delete(canvas.find_withtag("player"))
        draw_player(player_pos)

# - add event callback for left keypress
canvas.bind_all("<KeyPress-Left>", move_left)

# Moves player to the right
## TODO: optimize: make a single function that tests key pressed and acts accordingly
def move_right(event):
    print(event)
    global player_pos
    player_pos = player_pos+1
    if check_player_dead(terrain, player_pos):
        timer.stop()
    else:
        canvas.delete(canvas.find_withtag("player"))
        draw_player(player_pos)

# - add callback for right keypress
canvas.bind_all("<KeyPress-Right>", move_right)

# Create a new line for the terrain
def compute_line(last_center):
    new_center = last_center+randint(-MOBILITY, MOBILITY) # TODO: optimize
    if (new_center<1): new_center=1
    if (new_center>(WINDOW_WIDTH-1)): new_center=WINDOW_WIDTH-1
    new_track_width = randint(TRACK_SIZE/2, TRACK_SIZE)
    return(new_center, new_track_width)

# Initializes the terrain
## Optimization: we store only the "centers" and "track_width" for each line
def init_terrain():
    global player_pos
    terrain = []
    last_center = WINDOW_WIDTH/2
    for l in range(0, WINDOW_HEIGHT):
        new_center, new_track_width = compute_line(last_center)
        terrain += [ (new_center, new_track_width) ]
        last_center = new_center
    player_pos = last_center
    return(terrain, last_center)

# Draws the terrain on the window canvas
## Here use PIXEL_SIZE to zoom in
def draw_terrain(terrain):
    for l in range(0,len(terrain)):
        curr_center, curr_width = terrain[l]
        l1 = canvas.create_line(0, l, curr_center-curr_width/2, l)
        l2 = canvas.create_line(curr_center+curr_width/2, l, canvas.winfo_width(), l)
        canvas.itemconfig(l1, tags=("terrain"))
        canvas.itemconfig(l2, tags=("terrain"))

# Draws the player
def draw_player(player_pos):
    pl = canvas.create_line(player_pos-1, len(terrain)-1, player_pos+1, len(terrain)-1)
    canvas.itemconfig(pl, tags=("player"))

# Draws the whole game set
def draw_game(terrain, player_pos, score):
    canvas.delete("all")
    draw_terrain(terrain)
    draw_player(player_pos)
    print(score)

# Moves terrain upwards + create a new line at bottom
# - in fact delete most upwards line + create new line at bottom & redraws the whole terrain
# TODO: optimize using canvas.move on all gfx objects tagged as  "terrain"?
def update_terrain(curr_terrain, last_center, player_pos, score):
    global terrain, last_center
    del(curr_terrain[0])
    new_center, new_track_width = compute_line(last_center)
    curr_terrain = curr_terrain + [(new_center, new_track_width)]
    terrain = curr_terrain
    last_center=new_center
    if check_player_dead():
        timer.stop()
    else:
        draw_game(curr_terrain, player_pos, score);
        t = Timer(SPEED, update_terrain, kwargs={ 'curr_terrain':curr_terrain, 'last_center': new_center, 'player_pos': player_pos, 'score': score+1 })
        t.start()

# Check if player is dead?
def check_player_dead(terrain, player_pos):
    last_line=terrain[len(terrain)-1]
    if (last_line[player_pos-1]==1 and last_line[player_pos+1]==1):
        return true
    else:
        return false


# Start GUI
root_window.mainloop()
