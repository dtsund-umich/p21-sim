import boolean2
import sys
import string

import pygame
from pygame.locals import *
#TODO: Add E6, E7 effects

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
names = []
initials = []
for line in netstrings:
    names.append(line.split("*")[0])
    initials.append(True)
text = generate(netstrings, names, initials)

from boolean2 import Model

pygame.init()


space_needed = len(netstrings) * 70 + 10
screen = pygame.display.set_mode((space_needed,850), DOUBLEBUF)

model = boolean2.Model(text, mode='sync')
model.initialize()
model.iterate(steps=10)

screen.fill((255,255,255))
font = pygame.font.Font(None, 30)
for i in xrange(len(names)):
    #Stagger the names, because some of them might be long
    screen.blit(font.render(names[i], True, (0,0,0)), (10 + 70*i, 30 if i % 2 == 0 else 50))

step = 0
for state in model.states:
    cur_var = 0
    for name in names:
        pygame.draw.rect(screen, (0,255,0) if getattr(state,name) else (255,0,0),(10+70*cur_var,70+step*70,70,70))
        cur_var += 1
    step += 1
pygame.display.flip()
raw_input()

