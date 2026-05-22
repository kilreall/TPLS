import numpy as np 
import matplotlib.pyplot as plt 
from scipy.optimize import curve_fit 


def read_csv_xy(filename, points): # points - amount of points in one passage

    x, y = np.loadtxt(filename, delimiter=',', skiprows=1, unpack=True)
    cycles = len(y) // points
    y = y[:int(cycles*points)]
    x = x[:int(cycles*points)]
    y = y.reshape((cycles, points))
    x = x.reshape((cycles, points))

    y = np.mean(y, axis=0)
    x = np.mean(x, axis=0)
    return x, y

def fitf(alph, A, B, ph):
    return A*np.cos(2*np.pi*T**2*alph + ph) + B

def fitt(x, y, p0, bounds):
    popt, pcov = curve_fit(fitf, x, y, p0=p0, bounds=bounds)
    A, B, ph = popt
    return A, B, ph

def phFinder(php, phm):

    phm_m = np.arange(-2, 3, 1)*2*np.pi + phm
    #print(phm_m)
    ph_m = abs(phm_m - php)
    ind = np.argmin(ph_m)
    phm1 = phm_m[ind]
    #print(phm1)
    ph = (phm1 + php)/2

    return ph

def draw_pm():

    fig, ax = plt.subplots()
    ax.scatter(alphap * 2*np.pi*T**2, signalp, color="blue", label="k+ data")
    ax.plot(alphap* 2*np.pi*T**2, fitf(alphap, Ap, Bp, php), color="blue", label="k+ fit")
    ax.scatter(alpham* 2*np.pi*T**2, signalm, color="red", label="k- data")
    ax.plot(alpham* 2*np.pi*T**2, fitf(alpham, Am, Bm, phm), color="red", label="k- fit")

    fig, ax1 = plt.subplots()
    alph = np.linspace(-2*np.pi, 2*np.pi, 1000)
    ax1.plot(alph, fitf(alph/2/np.pi/T**2, Ap, Bp, php), color="blue", label="k+ fit")
    ax1.plot(alph, fitf(alph/2/np.pi/T**2, Am, Bm, phm), color="red", label="k- fit")


# constants
g = 9.8
lam = 780e-9
ke = 4*np.pi/lam

# data acquiring
alphap, signalp = read_csv_xy( r"2026-05-14_15\k+_800mV.csv", 201)
alpham, signalm = read_csv_xy( r"2026-05-14_15\k-_800mV.csv", 201)
alpham = abs(alpham)

# data analyze
T = 5e-3
# ph0 = ke*g*T**2
# ph1 = alphap[len(alphap)//2]
# print("ke*g*T**2 =", ph0)
Ap, Bp, php = fitt(alphap, signalp, [-0.05, 0.27, 0], ([-0.5, 0, -2*np.pi], [0, 0.5, 2*np.pi]))
# print(Ap, Bp, php)
Am, Bm, phm = fitt(alpham, signalm, [-0.05, 0.27, 0], ([-0.5, 0, -2*np.pi], [0, 0.5, 2*np.pi]))
# print(Am, Bm, phm)

print("ph+ =", php)
print("ph-=", phm)


print("ph=", phFinder(php, phm))

# draw
draw_pm()

plt.legend()
plt.show()
