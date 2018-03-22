#!/usr/bin/env python
# coding: utf-8

import random     # pour les nombres aleatoires
import math       # pour les arrondis
import time       # pour ralentir la simu avec sleep ou avec after
import Tkinter as tkinter # for GUI (version for Python2)

random.seed(42);  # For debugging/reproducible experiments

### A few constants
GUI_ELT_WIDTH=10;
GUI_ELT_HEIGHT=1;
FONT=('Times', '8', 'bold italic');
#
GRID_WIDTH      = 50;      # Taille de la grille
GRID_HEIGHT     = 50;      # Taille de la grille
GRID_STEP       = 10;       # Espace entre les points de la grille
GRID_COLOR      = "grey";   # Couleur des traits de la grille
GRID_X_MIN      = -math.floor(GRID_WIDTH/2);  # Coordonnees dans referentiel enonce
GRID_X_MAX      = math.floor(GRID_WIDTH/2);   # Coordonnees dans referentiel enonce
GRID_Y_MIN      = -math.floor(GRID_HEIGHT/2); # Coordonnees dans referentiel enonce
GRID_Y_MAX      = math.floor(GRID_HEIGHT/2);  # Coordonnees dans referentiel enonce
#
CANVAS_WIDTH    = GRID_WIDTH*GRID_STEP;       # Taille resultante du canvas (zone dessin)
CANVAS_HEIGHT   = GRID_HEIGHT*GRID_STEP;      # Taille resultante du canvas (zone dessin)
CANVAS_BG_COLOR = "white";                    # Couleur de fond du canvas (zone dessin)
#
NB_PARTICLES   = 500;            # Nombre de particles a simuler
PARTICLE_SIZE  = GRID_STEP*2/3;  # Taille des cercles pour representer chq particule
PARTICLE_COLOR = "red";          # Couleur des particules
#
NB_SIMU_STEPS   = 100;  # Nombre de pas de temps dans la simulation
SIMU_INVSPEED   = 100;  # Nombre de millisecondes entre chaque pas de temps

## The only shared var
paused=False;

#### Fonction des particules

# Initialise les positions des particules
def initParticles(N):
    particles = [];
    for p in xrange(N):
        initialPos = { 'x': 0, 'y': 0 };
        particles.append(initialPos);
    return particles;

# Deplace aleatoirement une unique particule, en respectant la "condition de bordure"
def moveSingleParticle(oldPos):
    aleat = random.randint(0, 3);
    if (aleat==0):
        newPos = { 'x':oldPos['x']+1, 'y': oldPos['y']};
    elif (aleat==1):
        newPos = { 'x': oldPos['x']-1, 'y': oldPos['y']};
    elif (aleat==2):
        newPos = { 'x': oldPos['x'], 'y': oldPos['y']+1};
    elif (aleat==3):
        newPos = { 'x': oldPos['x'], 'y': oldPos['y']-1};
    else:
        print("Should not have reached here! "+str(aleat)+" is not an accepted output");
    ## "Lorsqu'une particule rencontre une paroi, elle ne bouge pas si le mouvement
    ## determine aleatoirement la fait traverser cette paroi."
    if (newPos['x']<GRID_X_MIN+1):
        newPos['x'] = GRID_X_MIN+1;
    elif (newPos['x']>GRID_X_MAX-1):
        newPos['x'] = GRID_X_MAX-1;
    elif (newPos['y']<GRID_Y_MIN+1):
        newPos['y'] = GRID_Y_MIN+1;
    elif (newPos['y']>GRID_Y_MAX-1):
        newPos['y'] = GRID_Y_MAX-1;
    return newPos;

# Deplace toutes les particules d'un pas aleatoire
def moveParticles(particles):
    newParticles = [];
    for p in xrange(len(particles)):
        newParticles.append(moveSingleParticle(particles[p]));
    return(newParticles);

def applyGravity(particles):
    newParticles = [];
    for p in xrange(len(particles)):
        part = particles[p];
        if (part['y']<GRID_Y_MAX-1): # Only change value if it particle does not exit screen
            part['y'] += 1;  # Make particle go down
        newParticles.append(part);
    return(newParticles);

#### Problem/Model to GUI/View functions

# Convertit la liste des positions des particules en un tableau
# (proche de la "grille graphique")
def convertToMatrix(particles):
    matrix = [[0 for x in range(GRID_WIDTH)] for y in range(GRID_WIDTH)];
    for p in xrange(len(particles)):
        currentParticle = particles[p];
        tx = int(math.floor(currentParticle['x']-GRID_X_MIN));
        ty = int(math.floor(currentParticle['y']-GRID_Y_MIN));
        ##print("----------- Particle position: ("+str(x)+","+str(y)+")->("+str(tx)+","+str(ty)+")");  ## Debug
        ##print("----------- Grid: ["+str(GRID_X_MIN)+"->"+str(GRID_X_MAX)+" ; "+str(GRID_Y_MIN)+"->"+str(GRID_Y_MAX)+"] / ("+str(GRID_WIDTH)+", "+str(GRID_HEIGHT)+")");
        matrix[tx][ty] += 1;
    ##print(matrix);   # for debugging
    return matrix;

#### Fonctions graphiques

# Un/Pauses the simulation
def pause(pauseButton):
    global paused;  ## required to set global var
    paused = not paused;
    if (paused):
        pauseButton.config(text="Unpause");
    else:
        pauseButton.config(text="Pause");

# Creation & Placement des elements graphiques
def initGUI(rootWindow):
    ##global canvas;  ## for debugging purpose
    canvas = tkinter.Canvas(rootWindow, width=CANVAS_WIDTH, height=CANVAS_HEIGHT);
    canvas.config(background=CANVAS_BG_COLOR);
    canvas.pack();
    slider = tkinter.Scale(rootWindow, from_=0, to=10, orient=tkinter.HORIZONTAL);
    slider.set(0);
    #slider.config(height=GUI_ELT_HEIGHT, width=GUI_ELT_WIDTH);
    slider.pack();
    label = tkinter.Label(rootWindow, text='t=0');
    labelfont = ('times', 20, 'bold');
    label.config(bg='black', fg='yellow');
    label.config(font=labelfont);
    label.config(height=GUI_ELT_HEIGHT, width=GUI_ELT_WIDTH);
    label.pack();  # expand=YES, fill=BOTH
    startButton = tkinter.Button(rootWindow, text="Démarrer",
                                 command= lambda: startSimulationLoop(canvas,label,slider));
    startButton.config(height=GUI_ELT_HEIGHT, width=GUI_ELT_WIDTH);
    startButton.pack();
    pauseButton = tkinter.Button(rootWindow, text="Pause",
                                 command=lambda: pause(pauseButton));
    pauseButton.config(height=GUI_ELT_HEIGHT, width=GUI_ELT_WIDTH);
    pauseButton.pack();
    exitButton = tkinter.Button(rootWindow, text="Sortir",
                                command=rootWindow.destroy);
    exitButton.config(height=GUI_ELT_HEIGHT, width=GUI_ELT_WIDTH);
    exitButton.pack();

def drawGrid(canvas):
    for x in xrange(0, CANVAS_WIDTH, GRID_STEP):
      l1 = canvas.create_line(x, 0, x, CANVAS_HEIGHT, fill=GRID_COLOR);
      canvas.itemconfig(l1, tags=("vl")); ## Useless
    for y in xrange(0, CANVAS_HEIGHT, GRID_STEP):
      l2 = canvas.create_line(0, y, CANVAS_WIDTH, y, fill=GRID_COLOR);
      canvas.itemconfig(l2, tags=("hl")); ## Useless
    ctr = canvas.create_oval(-GRID_X_MIN*GRID_STEP-PARTICLE_SIZE/2,
                             -GRID_Y_MIN*GRID_STEP-PARTICLE_SIZE/2,
                             -GRID_X_MIN*GRID_STEP+PARTICLE_SIZE/2,
                             -GRID_Y_MIN*GRID_STEP+PARTICLE_SIZE/2,
                             outline="grey", fill="grey");

# def drawParticlesFromPositions(canvas, particles):
#     for p in xrange(len(particles)):
#         currentParticle = particles[p];
#         tx = currentParticle['x']-GRID_X_MIN;
#         ty = currentParticle['y']-GRID_Y_MIN;
#         txg = tx*GRID_STEP;
#         tyg = ty*GRID_STEP;
#         o = canvas.create_oval(txg-PARTICLE_SIZE, tyg-PARTICLE_SIZE,
#                                txg+PARTICLE_SIZE, tyg+PARTICLE_SIZE,
#                                outline=PARTICLE_COLOR, fill=PARTICLE_COLOR);
#         canvas.itemconfig(o, tags=("part"+str(p))); ## Useless
#         canvas.update_idletasks(); # THIS IS A DIRTY HACK!!!

def drawParticlesFromGrid(canvas, matrix):
     for x in xrange(GRID_WIDTH):
         for y in xrange(GRID_HEIGHT):
             if (matrix[x][y]>0):
                 xg = x*GRID_STEP;
                 yg = y*GRID_STEP;
                 o = canvas.create_oval(xg-PARTICLE_SIZE, yg-PARTICLE_SIZE,
                                        xg+PARTICLE_SIZE, yg+PARTICLE_SIZE,
                                        outline=PARTICLE_COLOR, fill=PARTICLE_COLOR);
                 canvas.itemconfig(o, tags=("part("+str(x)+"/"+str(y)+")")); ## Useless
                 ##print("----------- Particle position: "+str(xg)+"/"+str(yg));  ## Debug
                 t = canvas.create_text((xg, yg), text=str(matrix[x][y]), font=FONT);
                 canvas.itemconfig(t, tags=("partCount("+str(x)+"/"+str(y)+")")); ## Useless
                 canvas.update_idletasks(); # THIS IS A DIRTY HACK!!!

def drawTime(label, t):
    label.configure(text="t="+str(t));
    label.update_idletasks();  # THIS IS A DIRTY HACK!!!

# Lance la simulation with loop
## Problem1: we do no give a chance to the GUI elements to update => we need to force them
## Problem2: since the event loop is broken, the "Sortir" button does not work.
# def startSimulationLoop(canvas, label):
#     particles = initParticles(NB_PARTICLES);
#     for step in xrange(NB_SIMU_STEPS):
#         ## print("*** DRAWING STEP#"+str(step)); ## Debug
#         # for the fun of seeing things move
#         canvas.delete("all");  # optimization:
#         drawGrid(canvas);      # remove only particles
# ###        drawParticlesFromPositions(canvas, particles);
#         drawParticlesFromGrid(canvas, convertToMatrix(particles));
#         drawTime(label, step);
#         # actions reelles du pas de temps de la simu
#         ## print("*** MOVING PARTICLES"); ## Debug
#         particles = moveParticles(particles);
#         time.sleep(SIMU_INVSPEED);

# Execute un pas de simulation (si on n'est pas en pause) et se
# rappelle elle-même au bout un certain delai
def oneSimulationStep(step, canvas, label, particles, gravity):
    global paused;  ## required to get global var
    if (not paused):
        ## print("*** DRAWING STEP#"+str(step)); ## Debug
        # for the fun of seeing things move
        canvas.delete("all");  # optimization:
        drawGrid(canvas);      # remove only particles
        ###    drawParticlesFromPositions(canvas, particles);
        matrix = convertToMatrix(particles);
        drawParticlesFromGrid(canvas, matrix);
        drawTime(label, step);
        # actions reelles du pas de temps de la simu
        ## print("*** MOVING PARTICLES"); ## Debug
        ## print(particles); ## Debug
        ## print(matrix);    ## Debug
        particles = moveParticles(particles);
        if (gravity!=0 and step%gravity==0):
            ## print("*** Applying gravity: step="+str(step)); ## Debug
            particles = applyGravity(particles);
        step=step+1;
    # Whatever the status of pause, we recall ourselves
    canvas.after(SIMU_INVSPEED, oneSimulationStep, step, canvas, label, particles, gravity);

# Lance la simulation (via un timer)
def startSimulationLoop(canvas, label, slider):
    particles = initParticles(NB_PARTICLES);
    gravity = slider.get();
    ##print("*** Starting simulation with gravity="+str(gravity));
    oneSimulationStep(1, canvas, label, particles, gravity);

##### Lancement automatique du programme
def main():
    # Les elements graphiques
    rootWindow = tkinter.Tk(); # une fenetre graphique TK
    rootWindow.title("Ma Super Simulation du Mouvement Brownien");
    initGUI(rootWindow);
    rootWindow.mainloop();

main();
