#Search the outputs of p21_sim, seeing if any of them exhibit periodicity
#Cruder than periodic_search; no Fourier transforms here, just local max search

import numpy
from glob import glob
import os
import sys

directories = glob("*/")
threshold = 0.1

#New feature: Pass in an argument to check only one directory!
#Return code 1 for periodicity, 0 otherwise.
checking_one = False
if len(sys.argv) > 1:
    directories = [sys.argv[1]]
    checking_one = True

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
                if checking_one:
                    sys.exit(0)
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
            if max(data) > 0.00000001 and max(data)/min(data) > 1.002 and len(maxima) > 2:
                if checking_one:
                    sys.exit(1)
                print "Periodic behavior found in trial " + d + ", file " + f + ", period = " + str((maxima[1] - maxima[0]) * 0.01)
                bad = True
                break
        except IndexError:
            bad = True
            if checking_one:
                sys.exit(0)
            print "ERROR found in trial " + d
    if not bad:
        if checking_one:
            sys.exit(0)
        print "Steady-state behavior found in trial " + d
    os.chdir("..")
