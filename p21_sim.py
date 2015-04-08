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
beta_vp = 1 #DUMMY with no physical basis XXX
alpha_mpa = 1.4 #Kim-Jackson
alpha_epa = 0.14 #DUMMY; Kim-Jackson alpha_ipa, which is obviously different
beta_mm = 9.425 #Kim-Jackson
beta_mi = 0.08 #Kim-Jackson
kappa_rb = 1 #DUMMY with no physical basis XXX
alpha_m = 0.583 #Kim-Jackson
beta_m = 0.9 #Kim-Jackson
alpha_M = 1 #Kim-Jackson
alpha_mm = 0.5 #DUMMY; Kim-Jackson alpha_sm, which isn't the same
beta_p21 = 3 #DUMMY with no physical basis XXX
beta_pp = 1 #DUMMY with no physical basis XXX
kappa_p = 1 #DUMMY with no physical basis XXX
alpha_p21 = 1 #DUMMY with no physical basis XXX
alpha_ep21 = 1 #DUMMY with no physical basis XXX
beta_rb = 0.7 #DUMMY with no physical basis XXX
alpha_rb = 1 #DUMMY with no physical basis XXX
alpha_crb = 1 #DUMMY with no physical basis XXX
k_a = 1 #DUMMY with no physical basis XXX
k_d = 1 #DUMMY with no physical basis XXX
k_6 = 0.1 #Tyson, adjustable 0.1-10
k_3 = 200 #Tyson, maybe misinterpreted
k_5 = 0 #Tyson
k_7 = 1 #DUMMY with no physical basis XXX
beta_cyc = 0.015 #Tyson, maybe misinterpreted
k_2 = 0 #Tyson
b_cyc = 1 #DUMMY (unused) with no physical basis XXX
b_kin = 1 #DUMMY (unused) with no physical basis XXX
b_e7 = 1 #DUMMY with no physical basis XXX

#Dummy initial conditions
y0 = [0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1]

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
    if y[7] == 0:
        return 0.018
    return 0.018+10*y[7]**2/(y[5]+y[6]+y[7])**2 #Tyson, adjustable

#Variable key
#y[0] = p53_active
#y[1] = mdm2
#y[2] = MDM2
#y[3] = p21
#y[4] = Rb
#y[5] = CDK1
#y[6] = pMPF
#y[7] = MPF
#y[8] = Cyclin
names = []
names.append("p53")
names.append("mdm2")
names.append("MDM2")
names.append("p21")
names.append("Rb")
names.append("CDK1")
names.append("pMPF")
names.append("MPF")
names.append("Cyclin")


#The derivative function for the differential equation system.
def func(y,t):
    return [
            #p53: synth - MDM2 degradation - E6 degradation
            beta_vp - alpha_mpa * y[2] * y[0] - alpha_epa * E6(t) * y[0],
            #mdm2: p53 transcription + Rb transcription - degradation
            beta_mm * y[0] + beta_mi * kappa_rb / (kappa_rb + y[4]) - alpha_m * y[1],
            #MDM2: translation - degradation - MPF degradation
            beta_m * y[1] - alpha_M * y[2] - alpha_mm * y[7] * y[2],
            #p21: Um, lots of things.
            beta_p21 + beta_pp*y[3]*y[0]/(y[0]+kappa_p) - alpha_p21*y[3] - alpha_ep21*E7(t)*y[3],
            #Rb: synth - degrad - cyclin
            beta_rb - alpha_rb*y[4] - alpha_crb*y[8]*y[4]**2/(y[4]+b_e7*E7(t)),
            #CDK1: MPF-driven synth - complexing with cyclin
            k_6*y[7] - k_3*y[5]*y[8],
            #pMPF: complex formation - phosphorylation + hydrolysis - degradation
            k_3*y[5]*y[8] - y[6]*fM(y) + k_5*y[7] - k_7*y[3]*y[6],
            #MPF: phosphorylation - dissociation - hydrolysis
            y[6]*fM(y) - k_6*y[7] - k_5*y[7],
            #Cyclin: synth - breakdown - complexing with CDK
            beta_cyc - k_2*y[8] - k_3*y[5]*y[8],
           ]

t = arange(0, 10.0, 0.01)

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

