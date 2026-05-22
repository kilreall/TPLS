import numpy as np 
import matplotlib.pyplot as plt 
from scipy.optimize import curve_fit 

def phadjuster(ph0_m):

    ph0 = ph0_m[0]
    ph_m = [ph0]
    for i in range(1, len(ph0_m)):
        phi_m = np.arange(-2, 3, 1)*2*np.pi + ph0_m[i]
        #print(phi_m)
        phi0_m = abs(phi_m - ph0)
        ind = np.argmin(phi0_m)
        phi = phi_m[ind]
        #print(phm1)
        ph_m.append(phi)

    return np.array(ph_m)

def draw():
    
    plt.scatter(We, ph-ph[0], color="red", label="data")

# constants

lam = 780e-9
ke = 4*np.pi/lam
T = 5e-3

typ = np.array([18, 22, 26, 46, 24])*1e-6
We = np.pi/typ
print(We)


ph0_m = np.array([0.7768613946477694,
                -0.4311475489130394,
                -1.2713537517034061,
                 0.9055077853163581,
                -0.8349867329968057])

ph = phadjuster(ph0_m)
print(ph)
#ph[3] = ph[3] - 2 *np.pi
ph = ph - ph[0]
print("Dg=", 5/ke/T**2*1e2*1e3, "mgal")
# draw

draw()

plt.legend()
plt.show()