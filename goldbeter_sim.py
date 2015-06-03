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
#All of these constants come directly from the Goldbeter paper.
cdc20tot = 5
e2ftot = 3
gf = 0.1 #XXX This one is adjustable
k_da = 0.1
k_db = 0.005
k_dd = 0.1
k_de = 0.1
k_gf = 0.1
k_1cdc20 = 1
k_2cdc20 = 1
k_1e2f = 0.01
k_2e2f = 0.01
v_da = 0.245
v_db = 0.28
v_dd = 0.245
v_de = 0.35
v_sa = 0.175
v_sb = 0.21
v_sd = 0.175
v_se = 0.21
v_1cdc20 = 0.21
v_2cdc20 = 0.35
v_1e2f = 0.805
v_2e2f = 0.7

md = k_dd * v_sd * gf / (k_gf + gf) / (v_dd - (v_sd * gf / (k_gf + gf)))


#Dummy initial conditions
y0 = [0.01,0.01,0.01,1.1,0.01]

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
names = []
names.append("E2F")
names.append("Me")
names.append("Ma")
names.append("Mb")
names.append("Cdc20")


#The derivative function for the differential equation system.
def func(y,t):
    return [
            v_1e2f * (e2ftot - y[0])/(k_1e2f + e2ftot - y[0]) * (md + y[1]) - v_2e2f * y[0]/(k_2e2f + y[0]) * y[2],
            v_se * y[0] - v_de * y[2] * y[1]/(k_de + y[1]),
            v_sa * y[0] - v_da * y[4] * y[2]/(k_da + y[2]),
            v_sb * y[2] - v_db * y[4] * y[3]/(k_db + y[3]),
            v_1cdc20 * y[3] * (cdc20tot - y[4])/(k_1cdc20 + cdc20tot - y[4]) - v_2cdc20 * y[4]/(k_2cdc20 + y[4])
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

