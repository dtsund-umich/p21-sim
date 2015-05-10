#Search the outputs of p21_sim, seeing if any of them exhibit periodicity

import numpy
from glob import glob
import os

directories = glob("*/")
threshold = 0.01

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
        transformed /= (2*len(transformed))
        #Exclude the first term, because that's just the mean and we expect it to be high anyway
        if numpy.linalg.norm(transformed[1:], numpy.inf) > threshold:
            print "Periodic behavior found in trial " + d
    os.chdir("..")
