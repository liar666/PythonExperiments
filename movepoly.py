#!/usr/bin/env python

try:
    # for Python2
    import Tkinter as tkinter  ## notice capitalized T in Tkinter
except ImportError:
    # for Python3
    import tkinter  ## notice lowercase 't' in tkinter here


racine = tkinter.Tk()
canvas = tkinter.Canvas(racine, width=800, height=500)
canvas.pack()

numéro_figure=canvas.create_polygon(110, 110, 110, 160, 150, 135)

def déplaceobjet(event):
    if event.keysym == 'Up':
        canvas.move(numéro_figure, 0, -3)
    elif event.keysym == 'Down':
        canvas.move(numéro_figure, 0, 3)
    elif event.keysym == 'Left':
        canvas.move(numéro_figure, -3, 0)
    elif event.keysym == 'Right':
        canvas.move(numéro_figure, 3, 0)
    elif event.keysym == 'q':
        racine.destroy()
    else: print("Unknown key pressed")

canvas.bind_all('<KeyPress>', déplaceobjet)
racine.mainloop()
