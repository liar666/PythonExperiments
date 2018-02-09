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
WINDOW_WIDTH=200
WINDOW_HEIGHT=100
TRACK_SIZE=50
TERRAIN_FG_COLOR="black"
TERRAIN_BG_COLOR="white"
SPEED=60

# Create the GUI
# - create window
root_window = tkinter.Tk()
root.configure(background=BG_COLOR)
# - add canvas
canvas = tkinter.Canvas(root_window, width=500, height=500)
# - add events for left/right keypress
canvas.bind_all("<KeyPress-Left>", move_left)
canvas.bind_all("<KeyPress-Right>", move_right)
canvas.pack()

# terrain = None
# last_center = None
player_pos = None
timer = None
# TODO: make game go faster with time!

# Quits the game (called on click on "Quit" button)
def quitf:
    timer.stop()
    root_window.destroy()

# - add quit button to the GUI
quit_button = tkinter.Button(root_window, text="Exit",
                             command=quitf)
quit_button.pack()

# Resets the game parameters (called on click on "Reset" button)
def start_game():
    time.sleep(20);
    terrain, last_center = init_terrain()
    player_pos = last_center
    score = 0
    update_terrain(terrain, last_center, player_pos, score)

# - add start_game button to the GUI
reset_button = tkinter.Button(root_window, text="Start/Reset",
                              command=start_game)
reset_button.pack()

# Moves player to the left
def move_left():
    player_pos--
    if check_player_dead():
        timer.stop()
    else:
        canvas.delete(canvas.find_withtag("player"))
        draw_player(player_pos)

# Moves player to the right
def move_right():
    player_pos++
    if check_player_dead():
        timer.stop()
    else:
        canvas.delete(canvas.find_withtag("player"))
        draw_player(player_pos)

# Create a new line for the terrain
def compute_line(last_center):
    new_center = last_center+randint(-TRACK_SIZE/4, TRACK_SIZE/4) # TODO: optimize
    new_track_width = randint(TRACK_SIZE/2, TRACK_SIZE)
    return(new_center, new_track_width)

# Initializes the terrain
## Optimization: we store only the "centers" and "track_width" for each line
def init_terrain():
    terrain = []
    last_center = WINDOW_WIDTH/2
    for l in range(WINDOW_HEIGHT):
        new_center, new_track_width = compute_line(last_center)
        terrain += [ (new_center, new_track_width) ]
        last_center = current_center
    return(terrain, last_center)

# Draws the terrain on the window canvas
def draw_terrain(terrain):
    for l in range(0,len(terrain)):
        curr_center, curr_width = terrain[l]
        l1 = canvas.create_line(0, l, curr_center-curr_width/2, l)
        l2 = canvas.create_line(curr_center+curr_width/2, l, canvas.winfo_width(), l)
        itemconfig(l1, tags=("terrain"))
        itemconfig(l2, tags=("terrain"))

# Draws the player
def draw_player(player_pos):
    pl = canvas.create_line(player_pos-1, len(terrain)-1, player_pos+1, len(terrain)-1)
    itemconfig(pl, tags=("player"))

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
    del(curr_terrain[0])
    new_center, new_track_width = compute_line(last_center)
    curr_terrain = curr_terrain + [(new_center, new_track_width)]
    if check_player_dead():
        timer.stop()
    else:
        draw_game(curr_terrain, player_pos, score);
        t = Timer(SPEED, update_terrain, kwargs={ 'curr_terrain':curr_terrain, 'last_center': new_center, 'player_pos': player_pos, 'score': score+1 })
        t.start()

# Check if player is dead?
def check_player_dead(terrain, player_pos):
    last_line=terrain[len(terrain)-1]
    if (last_line[player_pos-1]==1 || last_line[player_pos+1]==1):
        return true
    else:
        return false


# Start GUI
root_window.mainloop()
