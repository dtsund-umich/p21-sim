#Search the outputs of p21_sim, seeing if any of them exhibit periodicity
#Cruder than periodic_search; no Fourier transforms here, just local max search

import numpy
from glob import glob
import os

directories = glob("*/")
threshold = 0.1

for d in directories:
    if d == "./.git":
        continue
    os.chdir(d)
    bad = False
    for f in glob("*"):
        try:
            reader = open(f, 'r')
            lines = reader.readlines()
            halfway  = len(lines) / 2
            data = []
            if lines[-1].split()[1].strip() == "nan":
                print "Failure to converge found in trial " + d
                bad = True
                break
            for line in lines[halfway:]:
                data.append(float(line.split()[1].strip()))
            maxima = []
            for i in xrange(len(data)):
                if i > 0 and i < len(data) - 1:
                    if data[i] > data[i-1] and data[i] > data[i+1]:
                        maxima.append(i)
            if max(data) > 0.00000001 and max(data)/min(data) > 1.2 and len(maxima) > 2:
                print "Periodic/bad behavior found in trial " + d + ", file " + f + ", period = " + str((maxima[1] - maxima[0]) * 0.01)
                bad = True
                break
        except IndexError:
            bad = True
            print "ERROR found in trial " + d
    if not bad:
        print "Good behavior found in trial " + d
    os.chdir("..")
