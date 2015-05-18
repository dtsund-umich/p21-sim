#Remove all lines from the output files, except for every thousandth line, for efficiency of plotting

from glob import glob
import os

directories = glob("*/")

for d in directories:
    if d == "./.git":
        continue
    os.chdir(d)
    for f in glob("*"):
        reader = open(f, 'r')
        writer = open("chopped_" + f, 'w')
        lines = reader.readlines()
        i = 0
        for line in lines:
            i += 1
            if i % 1000 == 0:
                writer.write(line)
                i = 0
    os.chdir("..")
