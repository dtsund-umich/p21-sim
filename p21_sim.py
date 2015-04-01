from scipy.integrate import odeint
from numpy import arange
import time
import datetime
import os

#Constants.  Do not add constants directly to the derivative function; violators
#will have rabid weasels set upon them.
beta_vp = 1 #dummy
alpha_mpa = 1 #dummy
alpha_epa = 1 #dummy
beta_mm = 1 #dummy
beta_mi = 1 #dummy
kappa_rb = 1 #dummy
alpha_m = 1 #dummy
beta_m = 1 #dummy
alpha_M = 1 #dummy
alpha_mm = 1 #dummy
beta_p21 = 1 #dummy
beta_pp = 1 #dummy
kappa_p = 1 #dummy
alpha_p21 = 1 #dummy
alpha_ep21 = 1 #dummy
beta_rb = 1 #dummy
alpha_rb = 1 #dummy
alpha_crb = 1 #dummy
k_a = 1 #dummy
k_d = 1 #dummy
k_6 = 0.1 #Tyson, adjustable 0.1-10
k_3 = 200 #Tyson, maybe misinterpreted
k_5 = 0 #Tyson
k_7 = 1 #dummy
k_10 = 1 #dummy
beta_cyc = 0.015 #Tyson, maybe misinterpreted
k_2 = 0 #Tyson
k_8 = k_6 * 10000 #Tyson; >>k_9
k_9 = k_6 * 100 #Tyson; >>k_6

#Functions to be called from the derivative functions.
def E6(t):
    return 0 #dummy

def E7(t):
    return 0 #dummy

def fM(y):
    #The 0.0001 in the denominator is to ensure we never divide by 0
    return 0.018+10*y[8]**2/(y[5]+y[6]+y[7]+y[8]+0.0001)**2 #Tyson, adjustable

#Variable key
#y[0] = p53_active
#y[1] = mdm2
#y[2] = MDM2
#y[3] = p21
#y[4] = Rb
#y[5] = CDK1
#y[6] = pMPF
#y[7] = pMPF-p21
#y[8] = MPF
#y[9] = Cyclin
#y[10] = Cyclin-p21
#y[11] = E7-rb
names = []
names.append("p53")
names.append("mdm2")
names.append("MDM2")
names.append("p21")
names.append("Rb")
names.append("CDK1")
names.append("pMPF")
names.append("pMPF-p21")
names.append("MPF")
names.append("Cyclin")
names.append("Cyclin-p21")
names.append("E7-Rb")

#Dummy initial conditions
y0 = [0,0,0,0,0,0,0,0,0,0,0,0]

#The derivative function for the differential equation system.
def func(y,t):
    return [
            #p53: synth - MDM2 degradation - E6 degradation
            beta_vp - alpha_mpa * y[2] * y[0] - alpha_epa * E6(t) * y[0],
            #mdm2: p53 transcription + Rb transcription - degradation
            beta_mm * y[0] + beta_mi * kappa_rb / (kappa_rb + y[4]) - alpha_m * y[1],
            #MDM2: translation - degradation - MPF degradation
            beta_m * y[1] - alpha_M * y[2] - alpha_mm * y[8] * y[2],
            #p21: Um, lots of things.
            beta_p21 + beta_pp*y[3]*y[0]/(y[0]+kappa_p) - alpha_p21*y[3] - alpha_ep21*E7(t)*y[3] - k_7*y[3]*y[6] - k_8*y[3]*y[9] + k_10*y[7] + k_9*y[10],
            #Rb: synth - degrad - cyclin - E7 sequestration + E7 unsequestration
            beta_rb - alpha_rb*y[4] - alpha_crb*y[9]*y[4] - k_a*E7(t)*y[4] + k_d*y[11],
            #CDK1: MPF-driven synth - complexing with cyclin
            k_6*y[8] - k_3*y[5]*y[9],
            #pMPF: complex formation - phosphorylation + hydrolysis - p21 sequestr. + p21 unsequestr.
            k_3*y[5]*y[9] - y[6]*fM(y) + k_5*y[8] - k_7*y[3]*y[6] + k_10*y[7],
            #pMPF-p21: sequestration - unsequestration
            k_7*y[3]*y[6] - k_10*y[7],
            #MPF: phosphorylation - dissociation - hydrolysis
            y[6]*fM(y) - k_6*y[8] - k_5*y[8],
            #Cyclin: synth - breakdown - p21 sequestration + Cyc-p21 dissociation + p21 unsequestr.
            beta_cyc - k_2*y[9] - k_3*y[5]*y[9] - k_8*y[3]*y[9] + k_9*y[10] + k_6*y[8],
            #Cyclin-p21: sequestration - unsequestration
            k_8*y[3]*y[9] - k_9*y[10],
            #E7-Rb: sequestration - unsequestration
            k_a*E7(t)*y[4] - k_d*y[11]
           ]

t = arange(0, 10.0, 0.01)

y = odeint(func, y0, t, ixpr=True)


dirname = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d-%H:%M:%S')
os.makedirs(dirname)
os.chdir(dirname)

for i in range(len(y0)):
    writer = open(names[i]+".txt", 'w')
    for j in xrange(len(t)):
        writer.write(str(t[j]) + " " + str(y[j][i]) + "\n")
    writer.close()

