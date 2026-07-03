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
    We_f = np.linspace(0, np.max(We)+1e4, 100)
    plt.plot(We_f, (fitf(We_f, a, b)-fitf(We[2], a, b))/ke/T**2*1e5, color="blue", label="линейная аппроксимация")
    plt.scatter(We, (ph_m-ph_m[2])/ke/T**2*1e5, color="red", label="данные")
    

# constants

lam = 780e-9
ke = 4*np.pi/lam
T = 7e-3

# V = 800, 1200
typ = np.array([20, 18, 32])*1e-6
We = np.array([np.pi/typ[0], np.pi/typ[1],  93*1e3])


php = [1.791136736009665, 0.5787226673687026, -0.943691555661724]
ph_m = np.array([2.9035787144262066, 1.838890228890672, 0.06198267339774577])
ph_m = phadjuster(ph_m)



# draw

# fit
p0 = [(ph_m[-1]-ph_m[0])/(We[-1]-We[0]), ph_m[0]]
popt, pcov = curve_fit(fitf, We, ph_m, p0=p0)
a, b = popt

draw()

plt.xlabel(r"$\Omega_{eff}$, [Hz]")
plt.ylabel(r"$\Delta$, [mGal]")
plt.legend()
plt.show()