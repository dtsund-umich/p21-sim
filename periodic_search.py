#Search the outputs of p21_sim, seeing if any of them exhibit periodicity

import numpy
from matplotlib import pyplot as plt
from glob import glob
import os
import sys

directories = glob("*/")
threshold = 0.1

for d in directories:
    if d == "./.git":
        continue
    os.chdir(d)
    bad = False
    periods = []
    for f in glob("*"):
        if "scaled" in f:
            continue
        reader = open(f, 'r')
        lines = reader.readlines()
        halfway  = len(lines) / 2
        data = []
        if lines[-1].split()[1].strip() == "nan":
            print "Failure to converge found in trial " + d
            bad = True
            break
        for line in lines:
            data.append(float(line.split()[1].strip()))
        stepsize = 0.1 #FIXME
        transformed = numpy.fft.rfft(data)
        freq = numpy.fft.rfftfreq(len(data), d=stepsize)
        #Skip the first element of the Fourier transform, it corresponds to the high constant portion
        maxarg = numpy.argmax(numpy.absolute(transformed[1:])) + 1
        if transformed[maxarg] > threshold:
            #print "Periodic behavior found in trial " + d + ", periodic file " + f + ", period = " + str(1/freq[maxarg])
            periods.append(1/freq[maxarg])
            bad = True
            #break
    if not bad:
        print "Steady-state behavior found in trial " + d
    else:
        print "Periodic behavior found in trial " + d + ", periods " + str(periods)
    os.chdir("..")
