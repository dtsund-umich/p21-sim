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
alpha_p53 = 2 #Kim-Jackson alpha_pi, inactive p53 degradation rate
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
kappa_a = 1 #DUMMY with no physical basis XXX
kappa_d = 1 #DUMMY with no physical basis XXX
b_e7 = 1 #DUMMY with no physical basis XXX
k_e = 0.01 #DUMMY with no physical basis XXX
k_a = 0.01 #DUMMY with no physical basis XXX
k_b = 0.01 #DUMMY with no physical basis XXX


#All of the following constants come directly from the Goldbeter paper.
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
#p53_active: Kim-Jackson
#mdm2: Kim-Jackson
#MDM2: Kim-Jackson
#p21: XXX
#Rb: XXX
#Rb-E7: XXX, but starting at 0 makes a lot of sense
#E2F: Goldbeter
#Me: Goldbeter
#Ma: Goldbeter
#Mb: Goldbeter
#Cdc20: Goldbeter
y0 = [0.077,1.065,2.336,0.1,0.1,0,0.01,0.01,0.01,1.1,0.01]

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


#Variable key
#y[0] = p53_active
#y[1] = mdm2
#y[2] = MDM2
#y[3] = p21
#y[4] = Rb
#y[6] = CDK1
#y[7] = pMPF
#y[8] = MPF
#y[9] = Cyclin
#y[10] = CDK1-P
#y[10] = Cyclin-P
names = []
names.append("p53")
names.append("mdm2")
names.append("MDM2")
names.append("p21")
names.append("Rb")
names.append("Rb-E7")
names.append("E2F")
names.append("Me")
names.append("Ma")
names.append("Mb")
names.append("Cdc20")



#The derivative function for the differential equation system.
def func(y,t):
    return [
            #p53: synth - MDM2 degradation - E6 degradation - regular degradation
            beta_vp - alpha_mpa * y[2] * y[0] - alpha_epa * E6(t) * y[0] - alpha_p53 * y[0],
            #mdm2: p53 transcription + Rb transcription - degradation
            beta_mm * y[0] + beta_mi * kappa_rb / (kappa_rb + y[4]) - alpha_m * y[1],
            #MDM2: translation - degradation - MPF degradation
            beta_m * y[1] - alpha_M * y[2] - alpha_mm * y[8] * y[2],
            #p21: Um, lots of things.
            beta_p21 + beta_pp*y[0]/(y[0]+kappa_p) - alpha_p21*y[3] - alpha_ep21*(E7(t) - y[5])*y[3],
            #Rb: synth - degrad - cyclin - E7 association + E7 dissociation
            beta_rb - alpha_rb*y[4] - alpha_crb*y[7]*y[4] - kappa_a * y[4] * (E7(t) - y[5]) + kappa_d * y[5],
            #Rb-E7: association - dissociation
            kappa_a * y[4] * (E7(t) - y[5]) - kappa_d * y[5],
            #Active E2F: activation - deactivation
            v_1e2f * (e2ftot - y[6])/(k_1e2f + e2ftot - y[6]) * (md + y[7]) - v_2e2f * y[6]/(k_2e2f + y[6]) * y[8],
            #Cyclin E/CDK2 complex: synth - degrad (CycA/CDK2) - degrad (p21)
            v_se * y[6] - v_de * y[8] * y[7]/(k_de + y[7]) - k_e * y[3] * y[7],
            #Cyclin A/CDK2 complex: synth - degrad (Cdc20) - degrad (p21)
            v_sa * y[6] - v_da * y[10] * y[8]/(k_da + y[8]) - k_a * y[3] * y[8],
            #Cyclin B/CDK1 complex: synth - degrad (Cdc20) - degrad (p21)
            v_sb * y[8] - v_db * y[10] * y[9]/(k_db + y[9]) - k_b * y[3] * y[9],
            #Active Cdc20: activation - deactivation
            v_1cdc20 * y[9] * (cdc20tot - y[10])/(k_1cdc20 + cdc20tot - y[10]) - v_2cdc20 * y[10]/(k_2cdc20 + y[10])
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

