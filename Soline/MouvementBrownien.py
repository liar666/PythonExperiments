#!/usr/bin/env python

import random   # pour les nombres aléatoires
import math     # pour les arrondis
import time     # pour ralentir la simu

try:
    # for Python2
    import Tkinter as tkinter
except ImportError:
    # for Python3
    import tkinter


### A few constants
GRID_WIDTH      = 20;      # Taille de la grille
GRID_HEIGHT     = 20;      # Taille de la grille
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
NB_PARTICLES   = 10;           # Nombre de particles a simuler
PARTICLE_SIZE  = GRID_STEP/2;  # Taille des cercles pour representer chq particule
PARTICLE_COLOR = "red";        # Couleur des particules
#
NB_SIMU_STEPS   = 100;  # Nombre de pas de temps dans la simulation
SIMU_ANTISPEED  = 1;    # Nombre de secondes entre chaque pas de temps


#### Fonction des particules

# Initialise les positions des particules
def initParticles(N):
    particles = [];
    for p in xrange(0, N):
        initialPos = { 'x': 0, 'y': 0 };
        particles.append(initialPos);
    return particles;

# Deplace aleatoirement une unique particule, en respectant la "condition de bordure"
def moveSingleParticule(oldPos):
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
    if (newPos['x']<GRID_X_MIN):
        newPos['x'] = GRID_X_MIN;
    elif (newPos['x']>GRID_X_MAX):
        newPos['x'] = GRID_X_MAX;
    elif (newPos['y']<GRID_Y_MIN):
        newPos['y'] = GRID_Y_MIN;
    elif (newPos['y']>GRID_Y_MAX):
        newPos['y'] = GRID_Y_MAX;
    return newPos;

# Deplace toutes les particules d'un pas aleatoire
def moveParticles(particles):
    newParticles = [];
    for p in xrange(0, len(particles)):
        newParticles.append(moveSingleParticule(particles[p]));
    return(newParticles);


#### Fonctions graphiques

# Creation & Placement des elements graphiques
def initGUI(racine):
    global canvas;  ## for debugging purpose
    canvas = tkinter.Canvas(racine, width=CANVAS_WIDTH, height=CANVAS_HEIGHT);
    canvas.config(background=CANVAS_BG_COLOR);
    canvas.pack();
    bouton_sortir = tkinter.Button(racine, text="Sortir",
                                   command=racine.destroy);
    bouton_sortir.pack();
    bouton_demarrer = tkinter.Button(racine, text="Démarrer",
                                     command= lambda:startSimu(canvas));
    bouton_demarrer.pack();

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


def drawParticles(canvas, particles):
    for p in xrange(0, len(particles)):
        currentParticle = particles[p];
        tx = currentParticle['x']-GRID_X_MIN;
        ty = currentParticle['y']-GRID_Y_MIN;
        c = canvas.create_oval(tx*GRID_STEP-PARTICLE_SIZE, ty*GRID_STEP-PARTICLE_SIZE,
                               tx*GRID_STEP+PARTICLE_SIZE, ty*GRID_STEP+PARTICLE_SIZE,
                               outline=PARTICLE_COLOR, fill=PARTICLE_COLOR);
        canvas.itemconfig(c, tags=("part"+str(p))); ## Useless

# Lance la simulation
## TODO: looping inside the GUI event loop is dirty. Looping should be done with:
## Problem1: we do no give a change to the GUI elements to update => we need to force them
## Problem2: since the event loop is broken, the "Sortir" button does not work.
## t = Timer(<delay>, <cbfunc>, kwargs={ <args hmap> });
## t.start();
def startSimu(canvas):
    particles = initParticles(NB_PARTICLES);
    for step in xrange(0, NB_SIMU_STEPS):
        print("*** DRAWING STEP#"+str(step));
        # for the fun of seeing things move
        canvas.delete("all");  # optimization:
        drawGrid(canvas);      # remove only particles
        drawParticles(canvas, particles);
        canvas.update_idletasks(); # THIS IS A DIRTY HACK!!!
        # actions reelles du pas de temsp de la simu
        print("*** MOVING PARTICLES");
        particles = moveParticles(particles);
        time.sleep(SIMU_ANTISPEED);


##### Lancement automatique du programme
def main():
    # Les elements graphiques
    racine = tkinter.Tk(); # une fenetre graphique TK
    initGUI(racine);

main();


def test():
    particles = initParticles(NB_PARTICLES);
    canvas.delete("all");
    drawGrid(canvas);
    drawParticles(canvas, particles);
    time.sleep(3);
    particles = moveParticles(particles);
    particles = moveParticles(particles);
    particles = moveParticles(particles);
    canvas.delete("all");
    drawGrid(canvas);
    drawParticles(canvas, particles);
