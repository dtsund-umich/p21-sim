# Copyright (c) 2015-2016 Derrick Sund
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

infiles = []
dirname = ""

if len(sys.argv) > 1:
    infiles = sys.argv[1:]
    for infile in infiles:
        if not os.path.isfile(infile):
            sys.stderr.write(infile + ": No such file found.\n")
            sys.exit(1)

#Constants.  Do not add constants directly to the derivative function; violators
#will have rabid weasels set upon them.
alpha_p14 = 1 #DUMMY
alpha_Ink4 = 5 #DUMMY
alpha_p21 = 4 #DUMMY
alpha_p53 = 0.9 #DUMMY
alpha_mdm2r = 9.425 #DUMMY
alpha_MDM2 = 1 #DUMMY
alpha_CD = 1 #DUMMY
alpha_CE = 1 #DUMMY
alpha_CB = 1 #DUMMY

omega_p14 = 0.116 #DUMMY
omega_Ink4 = 0.139 #DUMMY
omega_p21 = 1 #DUMMY
omega_p21CE = 1 #DUMMY
omega_p53 = 2.079 #DUMMY
omega_p53MDM2 = 1 #DUMMY
omega_p53E6 = 1 #DUMMY
omega_mdm2r = 0.693 #DUMMY
omega_MDM2 = 8.318 #DUMMY
omega_CD = 0.023 #DUMMY
omega_CDInk4 = 1 #DUMMY
omega_CE = 1 #DUMMY
omega_CA = 1 #DUMMY
omega_CACDC20 = 1 #DUMMY
omega_CB = 1 #DUMMY
omega_CBCDC20 = 1 #DUMMY

beta_E2FRb = 2 #DUMMY
beta_E2FRbMP = beta_E2FRb * 0.3 #DUMMY, but should be smaller than beta_E2FRb
beta_mdm2p14 = 1 #DUMMY
beta_cp21 = 1 #DUMMY
beta_E7p21 = 1 #DUMMY
beta_E7pRB = 1 #DUMMY
beta_E7pRBP = 1 #DUMMY
beta_E7pRBPP = 1 #DUMMY

delta_E7p21 = 1 #DUMMY
delta_E7pRB = 1 #DUMMY

epsilon_RbCD = 0.4 #DUMMY
epsilon_RbCE = 0.7 #DUMMY
epsilon_E2F = 20 #DUMMY
epsilon_CDC20 = 1 #DUMMY

sigma_Rb = 0.3 #DUMMY
sigma_RbMP = 0.1 #DUMMY
sigma_E2F = 0.7 #DUMMY
sigma_CDC20 = 1 #DUMMY

kappa_CECA = 1 #DUMMY
kappa_CBCA = 1 #DUMMY

#Knockdown terms.  These should all be equal to 1 unless we're testing the
#effects of a knockdown.
theta_E2F = 1
theta_p53 = 1
theta_CE = 1
theta_MDM2 = 1
theta_CD = 1
theta_CA = 1
theta_Ink4 = 1
theta_CB = 1
theta_CDC20 = 1


k_p21 = 1
k_p53 = 1
k_RbMP = 1
k_RbPP = 1
k_RbCD = 1
k_RbCE = 1
k_E2FCA = 1
k_E2F = 1
k_CD = 1
k_CA = 1
k_CB = 1
k_CDC20CB = 1
k_CDC20 = 1

E2F_tot = 10 #DUMMY
CDC20_tot = 0.285
Rb_tot = 10 #DUMMY

#Potentially override parameters
for infile in infiles:
    reader = open(infile)
    for line in reader.readlines():
        exec(line)


#Dummy initial conditions
y0 = [0.1,0.1,0.1,0.1,Rb_tot,0.0,0.0,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0,0]


#Abort early if the output directory already exists.
if dirname != "":
    if os.path.exists(dirname):
        sys.stderr.write("Output dir " + dirname + " already exists.  Aborting.\n")
        sys.exit(2)


#Functions to be called from the derivative functions.
def E6(t):
    return 0 #dummy

def E7(t):
    return 0 #dummy

#Fractions for inhibition/inactive complex formation.
#Each has a sanity check in case chief input is near zero.
sanity_threshold = 0.00001
def f(e2f, rb, rbmp):
    if e2f < sanity_threshold:
        return 0
    return e2f**2 / (e2f + beta_E2FRb * rb + beta_E2FRbMP * rbmp)

def g(mdm2, p14):
    if mdm2 < sanity_threshold:
        return 0
    return mdm2**2 / (mdm2 + beta_mdm2p14 * p14)

def h(c, p21, cd, ce, ca, cb):
    if c < sanity_threshold:
        return 0
    if ca+cb+cd+ce < sanity_threshold:
        return 0
    return c**2 / (c + beta_cp21 * p21 * c / (ca+cb+cd+ce))

def j(e7, e7prb, e7p21):
    return e7 - e7prb - e7p21

#Variable key
#y[0] = p14
#y[1] = Ink4
#y[2] = p21
#y[3] = p53
#y[4] = Rb
#y[5] = pRb-P
#y[6] = pRb-PP
#y[7] = E2F
#y[8] = mdm2
#y[9] = pMDM2
#y[10] = CD (Cyclin D/CDK4-6 complex)
#y[11] = CE (Cyclin E/CDK2 complex)
#y[12] = CA (Cyclin A/CDK2 complex)
#y[13] = CB (Cyclin B/CDK1 complex)
#y[14] = CDC20
#y[15] = E7-pRB
#y[16] = E7-p21
names = []
names.append("p14")
names.append("Ink4")
names.append("p21")
names.append("p53")
names.append("pRb")
names.append("pRb-P")
names.append("pRb-PP")
names.append("E2F")
names.append("mdm2")
names.append("pMDM2")
names.append("CD")
names.append("CE")
names.append("CA")
names.append("CB")
names.append("CDC20")
names.append("E7-pRB")
names.append("E7-p21")




#The derivative function for the differential equation system.
def func(y,t):
    return [
            #We have p14 being produced by E2F after inhibition from Rb
            #is accounted for, and degraded at a constant rate.
            alpha_p14 * theta_E2F * f(y[7], y[4], y[5]) - omega_p14 * y[0],
            #It's just like the p14 equation, but with Ink4 instead!
            alpha_Ink4 * theta_E2F * f(y[7], y[4], y[5]) - omega_Ink4 * y[1],
            #Form p21 at a rate proportional to p53 presence; degrade it
            #"naturally" or with help from Cyclin E/CDK2.    E7 sequesters p21.
            alpha_p21 * theta_p53 * y[3] - omega_p21 * y[2] - omega_p21CE * theta_CE * y[11] * y[2]/(y[2]+k_p21) - beta_E7p21 * j(E7(t),y[15],y[16]) * y[2] + delta_E7p21 * y[16],
            #P53 is generated naturally at a constant rate, and degrades
            #both on its own and with help from MDM2.
            alpha_p53 - omega_p53 * y[3] - (omega_p53MDM2 * theta_MDM2 * g(y[9], y[0]) + omega_p53E6 * E6(t)) * y[3]/(y[3]+k_p53),
            #Rb gets monophosphorylated by Cyclin D/CDK4-6.  Rb-monophosphate
            #gets its phosphate cleaved at a constant rate.  Rb of all sorts
            #gets sequestered by E7.
            -epsilon_RbCD * theta_CD * y[4]/(y[4]+k_RbCD) * y[10] + sigma_Rb * y[5]/(y[5]+k_RbMP) - beta_E7pRB * j(E7(t),y[15],y[16]) * y[4] + delta_E7pRB * y[15] * y[4]/Rb_tot,
            #Rb-monophosphate can be formed by phosphorylation of Rb or cleavage
            #of Rb-polyphosphate.  It can be lost by Cyclin E/CDK2 or
            #phosphatase activity.  Rb of all sorts gets sequestered by E7.
            epsilon_RbCD * theta_CD * y[4]/(y[4]+k_RbCD) * y[10] - sigma_Rb * y[5]/(y[5]+k_RbMP) - epsilon_RbCE * theta_CE * y[5]/(y[5]+k_RbCE) * y[11] + sigma_RbMP * y[6]/(y[6]+k_RbPP) - beta_E7pRBP * j(E7(t),y[15],y[16]) * y[5] + delta_E7pRB * y[15] * y[5]/Rb_tot,
            #Rb-polyphosphate arises from Cyclin E/CDK2 activity on
            #Rb-monophosphate, and is lost by phosphatase activity.  Rb of all
            #sorts gets sequestered by E7.
            epsilon_RbCE * theta_CE * y[5]/(y[5]+k_RbCE) * y[11] - sigma_RbMP * y[6]/(y[6]+k_RbPP) - beta_E7pRBPP * j(E7(t),y[15],y[16]) * y[6] + delta_E7pRB * y[15] * y[6]/Rb_tot,
            #E2F is inactivated by Cyclin A/CDK2.  It is reactivated at a
            #constant rate, or so this equation proposes.
            -epsilon_E2F * theta_CA * y[7] * y[12]/(y[7] + k_E2FCA) + sigma_E2F * (E2F_tot - y[7])/(k_E2F + E2F_tot - y[7]),
            #mdm2 mRNA is promoted by p53 and degrades rapidly.
            alpha_mdm2r * theta_p53 * y[3] - omega_mdm2r * y[8],
            #MDM2 protein is translated from mdm2 mRNA, and is degraded at a
            #constant rate.
            alpha_MDM2 * y[8] - omega_MDM2 * y[9],
            #Cyclin D/CDK4-6 is promoted by growth factor, and can degrade either on its
            #own or under the influence of Ink4.
            alpha_CD - omega_CD * y[10] - y[10]/(y[10] + k_CD) * omega_CDInk4 * theta_Ink4 * y[1],
            #Cyclin E/CDK2 is also promoted by E2F, and degrades on its own.
            #When not inhibited by p21, it becomes Cyclin A/CDK2.
            alpha_CE * theta_E2F * f(y[7], y[4], y[5]) - omega_CE * y[11] - kappa_CECA * theta_CA * h(y[11], y[2], y[10], y[11], y[12], y[13]) * y[12],
            #Cyclin A/CDK2 forms from Cyclin E/CDK2.  It degrades over time, and
            #degrades faster under the influence of active CDC20.
            kappa_CECA * theta_CA * h(y[11], y[2], y[10], y[11], y[12], y[13]) * y[12] - omega_CA * y[12] - y[12]/(y[12] + k_CA) * omega_CACDC20 * theta_CDC20 * y[14],
            #Cyclin B/CDK1 is constantly produced, but normally gets degraded
            #quickly; active Cyclin A/CDK2 slows down the degradation.  Active
            #CDC20 also degrades it, however.
            alpha_CB - omega_CB * y[13] /(kappa_CBCA + theta_CA * h(y[12], y[2], y[10], y[11], y[12], y[13])) - y[13]/(y[13] + k_CB) * omega_CBCDC20 * theta_CDC20 * y[14],
            #CDC20 is activated by Cyclin B/CDK1.  It is inactivated gradually
            #over time.
            sigma_CDC20 * theta_CB * y[13] * (CDC20_tot - y[14])/(k_CDC20CB + CDC20_tot - y[14]) - epsilon_CDC20 * y[14]/(k_CDC20 + y[14]),
            #E7 viral protein will associate with retinoblastoma protein,
            #sequestering it into an inactive form.
            beta_E7pRB * j(E7(t),y[15],y[16]) * y[4] + beta_E7pRBP * j(E7(t),y[15],y[16]) * y[5] + beta_E7pRBPP * j(E7(t),y[15],y[16]) * y[6] - delta_E7pRB * y[15],
            #E7 viral protein will also associate with and sequester p21.
            beta_E7p21 * j(E7(t),y[15],y[16]) * y[2] - delta_E7p21 * y[16],
           ]

t = arange(0, 2000.0, 0.1)

y = odeint(func, y0, t, ixpr=False, mxstep=5000)

if dirname == "":
    dirname = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d-%H:%M:%S')
os.makedirs(dirname)
os.chdir(dirname)

for i in range(len(y0)):
    writer = open(names[i]+".txt", 'w')
    for j in xrange((len(t) * 9) / 10, len(t)):
        writer.write(str(t[j]) + " " + str(y[j][i]) + "\n")
    writer.close()

