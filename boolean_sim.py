import boolean2
import sys
import string
import time

import pygame
import pygame.event
from pygame.locals import *
#TODO: Add E6, E7 effects

#Generate the string input for the booleannet library call, based on update
#rules (net_lines), variable names (name_lines), and initial conditions.
def generate(net_lines, name_lines, initial_values):
    to_return = ""
    for i in xrange(len(name_lines)):
        to_return += name_lines[i] + " = " + str(initial_values[i]) + "\n"
    to_return += "\n"
    to_return += string.join(net_lines, "\n")
    return to_return
        

if len(sys.argv) < 2:
    print "Use: python boolean_sim.py networkfile.txt"
    print "networkfile.txt will be a list of update rules in plain text form."
    print "Example:"
    print "p53* = not MDM2"
    print "mdm2rna* = p53 or not Rb"
    print "etc."
    print "Be advised that variable names cannot differ in only casing!"
    print ""
    sys.exit()

netstrings = open(sys.argv[1]).readlines()
for i in xrange(len(netstrings)):
    netstrings[i] = netstrings[i].strip()
names = []
initials = []
for line in netstrings:
    names.append(line.split("*")[0])
    initials.append(True)
text = generate(netstrings, names, initials)

from boolean2 import Model

pygame.init()
font = pygame.font.Font(None, 30)

#Determine how big the window should be.
space_needed = len(netstrings) * 70 + 30
update_objs = []
longest = 0
for line in netstrings:
    length = font.size(line)[0]
    longest = length if length > longest else longest
space_needed += longest
screen = pygame.display.set_mode((space_needed,850), DOUBLEBUF)
pygame.display.set_caption("BooleanNet basic graphical frontend")

while True:
    model = boolean2.Model(text, mode='sync')
    model.initialize()
    model.iterate(steps=10)
    
    #Display the variable names along the top
    screen.fill((255,255,255))
    for i in xrange(len(names)):
        #Stagger the names, because some of them might be long
        screen.blit(font.render(names[i], True, (0,0,0)), (10 + 70*i, 20 if i % 2 == 0 else 45))
    
    #Display the update rules on the side
    for i in xrange(len(netstrings)):
        screen.blit(font.render(netstrings[i], True, (0,0,0)), (20 + 70 * len(netstrings), 70 + 25 * i))

    step = 0
    for state in model.states:
        cur_var = 0
        for name in names:
            pygame.draw.rect(screen, (0,255,0) if getattr(state,name) else (255,0,0),(10+70*cur_var,70+step*70,70,70))
            cur_var += 1
        step += 1
    pygame.display.flip()
    #See if the user clicked somewhere to update an initial condition
    update = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                if event.pos[0] > 10 and event.pos[0] < 10 + 70 * len(names):
                    index = (event.pos[0] - 10) / 70
                    initials[index] = not initials[index]
                    update = True
    if update:
        text = generate(netstrings, names, initials)
    time.sleep(0.1)

