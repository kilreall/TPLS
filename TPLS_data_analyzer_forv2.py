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

    return phm1

def draw_pm():

    fig, ax = plt.subplots()
    #ax.scatter(scankp, signalkp, color="blue", label="k+ data")
    ax.plot(scankp0, fitf(scankp0, Ap, Bp, php), color="blue", label="k+ fit")
    #ax.scatter(scankm, signalkm, color="red", label="k- data")
    ax.plot(scankm0, fitf(scankm0, Am, Bm, phm), color="red", label="k- fit")

    # fig1, ax1 = plt.subplots()
    # alph = np.linspace(-2*np.pi, 2*np.pi, 1000)
    # ax1.plot(alph, fitf(alph/2/np.pi/T**2, Ap, Bp, php), color="blue", label="k+ fit")
    # ax1.plot(alph, fitf(alph/2/np.pi/T**2, Am, Bm, phm), color="red", label="k- fit")


# constants
g = 9.8
lam = 780e-9
ke = 4*np.pi/lam

# data acquiring
poi = 201


kp = r"datav2\2026-07-01\TPLS\600mV\k+.csv"
sum1kp, sum2kp, normkp, scankp = np.loadtxt(kp, delimiter=',', skiprows=1, unpack=True)
sum1kp = sum1kp[:len(sum1kp)//poi*poi]
sum2kp = sum2kp[:len(sum2kp)//poi*poi]
normkp = normkp[:len(normkp)//poi*poi]
scankp = scankp[:len(scankp)//poi*poi]
# B1kp = 2762.9
# B2kp = 4274
# normkp = (sum1kp-B1kp)/(sum2kp-B2kp) 

km = r"datav2\2026-07-01\TPLS\600mV\k-.csv"
sum1km, sum2km, normkm, scankm = np.loadtxt(km, delimiter=',', skiprows=1, unpack=True)
sum1km = sum1km[:len(sum1km)//poi*poi]
sum2km = sum2km[:len(sum2km)//poi*poi]
normkm = normkm[:len(normkm)//poi*poi]
scankm = scankm[:len(scankm)//poi*poi]
scankm = abs(scankm)

# B1km = 2249.15
# B2km = 2954.767677
# normkm = (sum1km-B1km)/(sum2km-B2km) 

# data analyze
T = 7e-3
# ph0 = ke*g*T**2
# ph1 = alphap[len(alphap)//2]
# print("ke*g*T**2 =", ph0)
signalkp = normkp
signalkm = normkm
Ap, Bp, php = fitt(scankp, signalkp, [-0.05, 0.27, 0], ([-0.5, 0, -2*np.pi], [0, 0.5, 2*np.pi]))
# print(Ap, Bp, php)
Am, Bm, phm = fitt(scankm, signalkm, [-0.05, 0.27, 0], ([-0.5, 0, -2*np.pi], [0, 0.5, 2*np.pi]))
# print(Am, Bm, phm)

scankp0 = np.linspace(np.min(scankp), np.max(scankp), 10000)
alpkp = scankp0[np.argmin(fitf(scankp0, Ap, Bp, php)[:5000])]
print("alp+ =", alpkp)
scankm0 = np.linspace(np.min(scankm), np.max(scankm), 10000)
alpkm = scankm0[np.argmin(fitf(scankm0, Am, Bm, phm)[:5000])]
print("alp- =", alpkm)

print(f"alp0 = {alpkp/2 + alpkm/2}")
print(f"Dg k+k- = {abs(alpkp-alpkm)*2*np.pi/ke*1e5} mGal")
print(f"Dph k+k- = {abs(alpkp-alpkm)*2*np.pi*T**2} rad")

print(f"ph0+ = {-php}")
print(f"ph0- = {-phm}")

print(f"ph+ = {-php}")
print(f"ph- = {phFinder(-php, -phm)}")
print(f"phc = {phFinder(-php, -phm)/2 +(-php)/2}")

#print("ph=", phFinder(php, phm))

# draw
draw_pm()

plt.legend()
plt.show()
