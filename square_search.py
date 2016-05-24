from numpy import arange
import math
import os
import sys
import random

if len(sys.argv) < 3:
    print "use: python square_search.py parameters points outfile [-e]"
    print "parameters: file with parameter names, lower bounds, upper bounds"
    print "points: how many points are wanted"
    print "-e: add this flag for an exponential distribution (don't use 0 as a bound here)"
    sys.exit(1)

infile = sys.argv[1]
#This could crash with bad input, but I don't care
numpoints = int(sys.argv[2])
outfile  = sys.argv[3]

exponential = False
if len(sys.argv) >= 5:
    if sys.argv[4] == "-e":
        exponential = True

reader = open(infile)
names = []
nums = []
for line in reader.readlines():
    words = line.split()
    names.append(words[0])
    lower = 0
    upper = 0
    if exponential:
        lower = math.log(float(words[1]))
        upper = math.log(float(words[2]))
    else:
        lower = float(words[1])
        upper = float(words[2])
    numlist = arange(lower, upper + (upper - lower)/numpoints, (upper - lower)/(numpoints-1))
    #random.shuffle(numlist)
    nums.append(numlist.tolist())


i = 0
metawriter = open("run_" + outfile + ".sh", 'w')
listwriter = open(outfile + "_list.txt", 'w')
while len(nums[0]) > 0:
    outname = outfile + str(i) + ".txt"
    writer = open(outname, "w")
    writer.write("dirname=\""+str(i)+"\"\n")
    #for j in xrange(len(names)):
    #    towrite = ""
    #    if exponential:
    #        towrite = str(math.exp(nums[j].pop()))
    #    else:
    #        towrite = str(nums[j].pop())
    #    writer.write(names[j] + "=" + towrite + "\n")
    if exponential:
        writer.write(names[0] + "=" + str(math.exp(nums[0][i/numpoints])) + "\n")
        writer.write(names[1] + "=" + str(math.exp(nums[1][i%numpoints])) + "\n")
    else:
        writer.write(names[0] + "=" + str(nums[0][i/numpoints]) + "\n")
        writer.write(names[1] + "=" + str(nums[1][i%numpoints]) + "\n")
    writer.close()
    i += 1
    metawriter.write("python p21_sim.py " + outname + "\n")
    listwriter.write(outname + "\n")
metawriter.close()
