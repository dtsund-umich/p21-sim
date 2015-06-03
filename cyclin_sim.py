# Copyright (c) 2015 Derrick Sund
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.


from scipy.integrate import odeint
from numpy import arange
import time
import datetime
import os
import sys

infile = ""
dirname = ""

if len(sys.argv) > 1:
    infile = sys.argv[1]
    if not os.path.isfile(infile):
        sys.stderr.write(infile + ": No such file found.\n")
        sys.exit(1)

#Constants.  Do not add constants directly to the derivative function; violators
#will have rabid weasels set upon them.
k_6 = 0.5 #Tyson, adjustable 0.1-10
k_3 = 200 #Tyson, maybe misinterpreted
k_5 = 0 #Tyson
k_7 = 0.6 #Tyson
k_9 = k_6 * 10000 #Tyson
k_8 = k_9 * 10000 #Tyson
beta_cyc = 0.015 #Tyson, maybe misinterpreted
k_2 = 0 #Tyson

#Dummy initial conditions
y0 = [k_9/k_8,0.1,0.1,0.1,0.1,0.1]

#Potentially override parameters
if infile != "":
    reader = open(infile)
    for line in reader.readlines():
        exec(line)

#Functions to be called from the derivative functions.
def E6(t):
    return 0 #dummy

def E7(t):
    return 0 #dummy

def fM(y):
    if y[2] == 0:
        return 0.018
    return 0.018+100*y[2]**2/(y[0]+y[1]+y[2]+y[4])**2 #Tyson, adjustable

#Variable key
#y[5] = CDK1
#y[6] = pMPF
#y[7] = MPF
#y[8] = Cyclin
#y[9] = CDK1-P
#y[10] = Cyclin-P
names = []
names.append("CDK1")
names.append("pMPF")
names.append("MPF")
names.append("Cyclin")
names.append("CDK1-P")
names.append("Cyclin-P")


#The derivative function for the differential equation system.
def func(y,t):
    return [
            #CDK1: MPF breakdown - phosphorylation + dephosphorylation
            0,#k_6*y[2] - k_8*y[0] + k_9*y[4],
            #pMPF: complex formation - phosphorylation + hydrolysis
            k_3*y[4]*y[3] - y[1]*fM(y) + k_5*y[2],
            #MPF: phosphorylation - hydrolysis - dissociation
            y[1]*fM(y) - k_5*y[2] - k_6*y[2],
            #Cyclin: synth - breakdown - complexing with CDK
            beta_cyc - k_2*y[3] - k_3*y[4]*y[3],
            #CDK1-P: phosphorylation - dephosphorylation - complexing with cyclin
            k_8*y[0] - k_9*y[4] - k_3*y[4]*y[3],
            #Cyclin-P: dissociation - breakdown
            k_6*y[2] - k_7*y[5]
           ]

t = arange(0, 500.0, 0.01)

y = odeint(func, y0, t, ixpr=True)

if dirname == "":
    dirname = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d-%H:%M:%S')
os.makedirs(dirname)
os.chdir(dirname)

for i in range(len(y0)):
    writer = open(names[i]+".txt", 'w')
    for j in xrange(len(t)):
        writer.write(str(t[j]) + " " + str(y[j][i]) + "\n")
    writer.close()

