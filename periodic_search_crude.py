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
    all_zeroes = True
    periodicity = False
    periodic_file = ""
    period = 0
    one_diverges = False
    if d == "./.git":
        continue
    os.chdir(d)
    bad = False
    for f in glob("*"):
        try:
            reader = open(f, 'r')
            lines = reader.readlines()
            halfway  = len(lines) / 2
            stepsize = float(lines[0].split()[0].strip()) - float(lines[1].split()[0].strip())
            data = []
            if lines[-1].split()[1].strip() == "nan":
                if checking_one:
                    sys.exit(0)
                print "Failure to converge found in trial " + d
                bad = True
                break
            if lines[-1].split()[1].strip() != "0.0":
                all_zeroes = False
            for line in lines[halfway:]:
                data.append(float(line.split()[1].strip()))
            maxima = []
            divergent = True
            for i in xrange(len(data)):
                if i > 0 and i < len(data) - 1:
                    if data[i] < data[i+1]:
                        divergent = False
                    if data[i] > data[i-1] and data[i] > data[i+1]:
                        maxima.append(i)
            if divergent:
                one_diverges = True
            if max(data) > 0.00000001 and max(data)/min(data) > 1.002 and len(maxima) > 2:
                if checking_one:
                    sys.exit(1)
                periodicity = True
                periodic_file = f
                period = str((maxima[0] - maxima[1]) * stepsize)
                bad = True
                break
        except IndexError:
            bad = True
            if checking_one:
                sys.exit(0)
            print "ERROR found in trial " + d
    if periodicity:
        if one_diverges:
            print "Periodivergence in trial " + d + ", periodic file " + periodic_file + ", period = " + period
        else:
            print "Periodic behavior found in trial " + d + ", file " + periodic_file + ", period = " + period
    elif not bad:
        if checking_one:
            sys.exit(0)
        if all_zeroes:
            print "Error or zero-convergence in trial " + d
        if one_diverges:
            print "Divergence in trial " + d
        else:
            print "Steady-state behavior found in trial " + d
    os.chdir("..")
