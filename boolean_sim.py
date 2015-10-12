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

model = boolean2.Model(text, mode='sync')
model.initialize()
model.iterate(steps=10)
for state in model.states:
    print state.Mb

pygame.init()
screen = pygame.display.set_mode((1024,850), DOUBLEBUF)
screen.fill((255,255,255))
font = pygame.font.Font(None, 30)
screen.blit(font.render("p53", True, (0,0,0)), (10, 50))
screen.blit(font.render("mdm2", True, (0,0,0)), (80, 50))
screen.blit(font.render("MDM2", True, (0,0,0)), (150, 50))
screen.blit(font.render("p21", True, (0,0,0)), (220, 50))
screen.blit(font.render("Rb", True, (0,0,0)), (290, 50))
screen.blit(font.render("E2F", True, (0,0,0)), (360, 50))
screen.blit(font.render("p16", True, (0,0,0)), (430, 50))
screen.blit(font.render("Md", True, (0,0,0)), (500, 50))
screen.blit(font.render("Me", True, (0,0,0)), (570, 50))
screen.blit(font.render("Ma", True, (0,0,0)), (640, 50))
screen.blit(font.render("Mb", True, (0,0,0)), (710, 50))
screen.blit(font.render("Cdc20", True, (0,0,0)), (780, 50))
cur = 0
for state in model.states:
    pygame.draw.rect(screen, (0,255,0) if state.p53 else (255,0,0),(10,70+cur*70,70,70))
    pygame.draw.rect(screen, (0,255,0) if state.mdm2rna else (255,0,0),(80,70+cur*70,70,70))
    pygame.draw.rect(screen, (0,255,0) if state.MDM2 else (255,0,0),(150,70+cur*70,70,70))
    pygame.draw.rect(screen, (0,255,0) if state.p21 else (255,0,0),(220,70+cur*70,70,70))
    pygame.draw.rect(screen, (0,255,0) if state.Rb else (255,0,0),(290,70+cur*70,70,70))
    pygame.draw.rect(screen, (0,255,0) if state.E2F else (255,0,0),(360,70+cur*70,70,70))
    pygame.draw.rect(screen, (0,255,0) if state.p16 else (255,0,0),(430,70+cur*70,70,70))
    pygame.draw.rect(screen, (0,255,0) if state.Md else (255,0,0),(500,70+cur*70,70,70))
    pygame.draw.rect(screen, (0,255,0) if state.Me else (255,0,0),(570,70+cur*70,70,70))
    pygame.draw.rect(screen, (0,255,0) if state.Ma else (255,0,0),(640,70+cur*70,70,70))
    pygame.draw.rect(screen, (0,255,0) if state.Mb else (255,0,0),(710,70+cur*70,70,70))
    pygame.draw.rect(screen, (0,255,0) if state.Cdc20 else (255,0,0),(780,70+cur*70,70,70))
    cur += 1
pygame.display.flip()
raw_input()

