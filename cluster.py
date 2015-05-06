import os
import sys

if len(sys.argv) < 3:
    print "Run: python cluster.py infile threshold"
    sys.exit(1)

threshold = float(sys.argv[2])
lines = open(sys.argv[1], 'r').readlines()
for line in lines:
    tokens = line.strip().split()
    #Should be three tokens in each line.
    if float(tokens[2]) < threshold:
        print tokens[0] + " " + tokens[1]
