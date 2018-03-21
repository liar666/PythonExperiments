#!/usr/bin/env python

import random as rd
import math as m
from threading import Timer

try:
    # for Python2
    import Tkinter as tkinter  ## notice capitalized T in Tkinter
except ImportError:
    # for Python3
    import tkinter  ## notice lowercase 't' in tkinter here

racine = tkinter.Tk()
canvas = tkinter.Canvas(racine, width=500, height=500)
canvas.pack()
bouton_sortir = tkinter.Button(racine, text="Sortir",
                               command=racine.destroy)
bouton_sortir.pack()

def rectangle_aleatoire(largeur, hauteur, remplissage=None):
    x1 = rd.randrange(largeur)
    y1 = rd.randrange(hauteur)
    x2 = rd.randrange(largeur)
    y2 = rd.randrange(hauteur)
    if remplissage==None:
        canvas.create_rectangle(x1, y1, x2, y2)
    else :
        canvas.create_rectangle(x1, y1, x2, y2, fill=remplissage)

def couleurshex(rouge, vert, bleu):
    rouge = m.floor(255*(rouge/100.0))
    vert  = m.floor(255*(vert/100.0))
    bleu  = m.floor(255*(bleu/100.0))
    return '#%02x%02x%02x' % (rouge, vert, bleu)

def couleur_surprise():
    return couleurshex(rd.randrange(100),rd.randrange(100),rd.randrange(100))

for x in range(0, 100):
    rectangle_aleatoire(500,500, couleur_surprise())

racine.mainloop()

## >>> from drawrect import *
