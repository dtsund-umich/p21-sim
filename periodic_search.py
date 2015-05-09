#Search the outputs of p21_sim, seeing if any of them exhibit periodicity

import numpy
from glob import glob
import os

directories = glob("*/")
threshold = 0.5

for d in directories:
    if d == "./.git":
        continue
    os.chdir(d)
    for f in glob("*"):
        print f
        reader = open(f, 'r')
        lines = reader.readlines()
        halfway  = len(lines) / 2
        data = []
        for line in lines[halfway:]:
            data.append(float(line.split()[1].strip()))
        transformed = numpy.fft.rfft(data)
        #Exclude the first few terms to cut down on noise
        if numpy.linalg.norm(transformed[4:], numpy.inf) > threshold:
            print "Periodic behavior found in trial " + d
    os.chdir("..")
