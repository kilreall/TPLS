import numpy as np

lam = 780e-9
keff = 4*np.pi/lam

typ = 16e-6
Weff = np.pi/typ 
g = 9.8
T = 5e-3
v1 = g*17e-3
v3 = v1 + g*T*2
d1 = 2*keff*v1/2/np.pi
d3 = 2*keff*v3/2/np.pi
DTPLS = Weff/4*(1/d1-1/d3)
print("dph=", DTPLS)
print("dg=", DTPLS/keff/T**2*1e2*1e3, "mGal")