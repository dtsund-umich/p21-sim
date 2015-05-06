import os
import sys
import glob
import numpy

if len(sys.argv) < 2:
    print "Run: python pairwise.py n"
    print "n is the number of points under consideration"
    sys.exit(1)

points = []
for i in xrange(int(sys.argv[1])):
    os.chdir(str(i))
    point = []
    files = glob.glob("*")
    files.sort()
    for f in files:
        lines = open(f, 'r').readlines()
        point.append(float(lines[-1].split()[1]))
    points.append(numpy.asarray(point))
    os.chdir("..")

for i in xrange(int(sys.argv[1])):
    for j in range(int(sys.argv[1]))[i+1:]:
        print str(i) + " " + str(j) + " " + str(numpy.linalg.norm(points[i]-points[j]))
