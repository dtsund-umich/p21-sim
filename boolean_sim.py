import boolean2
#TODO: Add E6, E7 effects
text = """
p53 = True
mdm2rna = True
MDM2 = True
p21 = True
Rb = True
E2F = True
p16 = True
Md = True
Me = True
Ma = True
Mb = True
Cdc20 = True

p53* = not MDM2
mdm2rna* = p53 or not Rb
MDM2* = (mdm2rna or MDM2) and not Ma
p21* = p53
Rb* = not Me
E2F* = (Md and Me and not Ma) or (E2F and not Ma) or (E2F and (Md or Me))
p16* = E2F and not Rb
Md* = not p16
Me* = (E2F and not Rb) or (Me and not Ma and not p21)
Ma* = (E2F and not Rb) or (Ma and not Cdc20 and not p21)
Mb* = Ma or (Mb and not Cdc20 and not p21)
Cdc20* = Mb 
"""
from boolean2 import Model

model = boolean2.Model(text, mode='sync')
model.initialize()
model.iterate(steps=10)
for state in model.states:
    print state.Mb
