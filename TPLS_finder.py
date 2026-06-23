import numpy as np 
import matplotlib.pyplot as plt 
from scipy.optimize import curve_fit 

def fitf(x, a, b):
    return a*x+b

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
    We_f = np.linspace(0, We[0]+1e4, 100)
    plt.plot(We_f, fitf(We_f, a, b), color="blue", label="линейная аппроксимация")
    plt.scatter(np.delete(We, 3), np.delete((ph-ph[0]), 3), color="red", label="данные")
    

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

# fit
popt, pcov = curve_fit(fitf, np.delete(We, 3), np.delete((ph-ph[0]), 3))
a, b = popt

draw()

plt.xlabel(r"$\Omega_{eff}$, [МГц]")
plt.ylabel(r"Разность фаз, [рад]")
print(b/ke/T/T*1e5)
plt.legend()
plt.show()