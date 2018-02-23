#!/usr/bin/env python3

from random import randint,seed
from threading import Timer # to debug (sloweR+prints error on callback function call)

try:
    # for Python2
    import Tkinter as tkinter  ## notice capitalized T in Tkinter
except ImportError:
    # for Python3
    import tkinter  ## notice lowercase 't' in tkinter here

##seed(42)  ## From debugging/reproducible experiments

# Set useful constants
PIXEL_SIZE=4 # multiply all the drawings by this value
CANVAS_WIDTH=100
CANVAS_HEIGHT=100
TRACK_SIZE=CANVAS_WIDTH/4
MOBILITY_RANGE=TRACK_SIZE/6
TERRAIN_FG_COLOR="black"
TERRAIN_BG_COLOR="white"
PLAYER_COLOR="red"
SCORE_COLOR="green"
SPEED=1.        # starting with slow speed of 1 sec between new line creation
SPEED_DEC=8./10. # the amount of speed increase (in fact timeout decrease)
SCORE_MOD=15     # every X score points, the speed increases
MIN_PLAYER_POS=1
MAX_PLAYER_POS=CANVAS_WIDTH-1

# Create the GUI
# - create window
root_window = tkinter.Tk()
root_window.configure(background=TERRAIN_BG_COLOR)
# - add canvas
canvas = tkinter.Canvas(root_window, width=CANVAS_WIDTH*PIXEL_SIZE, height=CANVAS_HEIGHT*PIXEL_SIZE)
canvas.pack()

txt = canvas.create_text(CANVAS_WIDTH*PIXEL_SIZE/2, 4*PIXEL_SIZE, anchor='center', fill=SCORE_COLOR, state="disabled")
canvas.itemconfig(txt, text="Score: 0\nSpeed: "+str(1./SPEED))
canvas.itemconfig(txt, tags=("score"))
canvas.pack()

terrain = None
last_center = None
player_pos = None
timer = None
dead = False
# TODO: make game go faster with time!

# Resets the game parameters (called on click on "Reset" button)
def start_game():
    global terrain, last_center, player_pos, dead
    dead = False
    terrain, last_center = init_terrain()
    player_pos = last_center
    score = 0
    #sleep(20);
    update_terrain(terrain, last_center, score)

# Quits the game (called on click on "Quit" button)
def quitf():
    global dead
    dead = True
    root_window.destroy()

# - add quit button to the GUI
quit_button = tkinter.Button(root_window, text="Exit",
                             command=quitf)
quit_button.pack()

# - add start_game button to the GUI
reset_button = tkinter.Button(root_window, text="Start/Reset",
                              command=start_game)
reset_button.pack()

# Moves player to the left/right according to keypress
def move_player(event):
    #print(event.keysym)
    global player_pos, dead
    if (dead):
        return
    if event.keysym == "Right":
        player_pos = player_pos+1
        if (player_pos > MAX_PLAYER_POS):
            player_pos = MAX_PLAYER_POS
    elif event.keysym == "Left":
        player_pos = player_pos-1
        if (player_pos < MIN_PLAYER_POS):
            player_pos = MIN_PLAYER_POS
    if check_player_dead(terrain, player_pos):
        dead = True
#    else:
#        draw_player(player_pos)

# - add callback for left&right keypresses
canvas.bind_all("<KeyPress-Left>", move_player)
canvas.bind_all("<KeyPress-Right>", move_player)

# Create a new line for the terrain
def compute_line(last_center):
    new_center = last_center+randint(-MOBILITY_RANGE, MOBILITY_RANGE) # TODO: optimize
    if (new_center<MOBILITY_RANGE): new_center=MOBILITY_RANGE
    if (new_center>(CANVAS_WIDTH-MOBILITY_RANGE)): new_center=CANVAS_WIDTH-MOBILITY_RANGE
    new_track_width = randint(TRACK_SIZE-4, TRACK_SIZE)
    return(new_center, new_track_width)

# Initializes the terrain
## Optimization: we store only the "centers" and "track_width" for each line
def init_terrain():
    global player_pos
    terrain = []
    last_center = CANVAS_WIDTH/2
    for l in range(0, CANVAS_HEIGHT):
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
        l1 = canvas.create_line(0, l*PIXEL_SIZE, (curr_center-curr_width/2)*PIXEL_SIZE, l*PIXEL_SIZE, width=PIXEL_SIZE, fill=TERRAIN_FG_COLOR)
        l2 = canvas.create_line((curr_center+curr_width/2)*PIXEL_SIZE, l*PIXEL_SIZE, canvas.winfo_width()*PIXEL_SIZE, l*PIXEL_SIZE, width=PIXEL_SIZE, fill=TERRAIN_FG_COLOR)
        canvas.itemconfig(l1, tags=("terrain"))
        canvas.itemconfig(l2, tags=("terrain"))

# Draws the player
def draw_player(player_pos):
    canvas.delete(canvas.find_withtag("player"))
    pl = canvas.create_line((player_pos-1)*PIXEL_SIZE, (len(terrain)-1)*PIXEL_SIZE, (player_pos+1)*PIXEL_SIZE, (len(terrain)-1)*PIXEL_SIZE, width=PIXEL_SIZE, fill=PLAYER_COLOR)
    canvas.itemconfig(pl, tags=("player"))

# Draws the score
def draw_score(score):
    sc = canvas.find_withtag("score")
    canvas.itemconfig(sc, text="Score: "+str(score)+"\nSpeed: "+str(1./SPEED))
    canvas.tag_raise("score")

# Draws the whole game set
def draw_game(terrain, score):
    canvas.delete("terrain")
    canvas.delete("player")
    draw_terrain(terrain)
    draw_player(player_pos)
    draw_score(score)

# Moves terrain upwards + create a new line at bottom
# - in fact delete most upwards line + create new line at bottom & redraws the whole terrain
# TODO: optimize using canvas.move on all gfx objects tagged as "terrain"?
def update_terrain(curr_terrain, lst_center, score):
    global terrain, last_center, dead, SPEED
    if (dead):
        return
    del(curr_terrain[-1])
    new_center, new_track_width = compute_line(lst_center)
    curr_terrain = [(new_center, new_track_width)] + curr_terrain
    terrain = curr_terrain
    last_center=new_center
#    if check_player_dead(terrain, player_pos):
#        dead = True
#    else:
    if (score%SCORE_MOD==1):
       SPEED=SPEED*SPEED_DEC
    draw_game(curr_terrain, score);
    t = Timer(SPEED, update_terrain, kwargs={ 'curr_terrain':curr_terrain, 'lst_center': new_center, 'score': score+1 })
    t.start()

# Check if player is dead?
def check_player_dead(terrain, player_pos):
    (curr_center, curr_width) = terrain[-1] # get last line
    left_wall = curr_center-curr_width/2
    right_wall= curr_center+curr_width/2
    #print("****** "+str(left_wall)+" < "+str(player_pos)+" < "+str(right_wall)+"****** ")
    #print(str(SPEED))
    is_alive=(player_pos>left_wall and player_pos<right_wall) # TODO: use <= / >= ?
    #print(str(is_alive))
    return(not is_alive)


# Start GUI
root_window.mainloop()
