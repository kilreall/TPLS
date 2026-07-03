import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

def gaus(alp, A, k, alp0, B):
    return A*np.exp(-(alp-alp0)**2/2/k**2) + B

def lorentz(alp, A, k, alp0, B):
    return A * (k/2)**2/((k/2)**2+(alp-alp0)**2) + B

def Rabifit(t, w, A, B, tc):
    return -A*np.exp(-(t/tc))*np.cos(w*t)+B

def meanmin(arr, n):
    arr1 = arr.copy()
    S = 0
    for i in range(n):
        S += np.min(arr1)
        arr1[np.argmin(arr1)] = np.max(arr1)

    return S/n

ty_m = np.array([3, 4, 8, 12, 16, 20, 24, 26, 28, 30, 32, 34, 36, 40, 44, 48, 52, 56, 60, 64, 68, 72, 76, 80, 81, 84, 88, 90, 92, 96, 100])
A_m = []


for ty in ty_m:
    filename = f"ty{ty}.csv"
    sum1, sum2, norm, scan = np.loadtxt(filename, delimiter=',', skiprows=1, unpack=True)
    poi = 201
    if len(sum1) >=201:
        sum1 = sum1[:len(sum1)//poi*poi]
        sum2 = sum2[:len(sum2)//poi*poi]
        norm = norm[:len(norm)//poi*poi]
        scan = scan[:len(scan)//poi*poi]


    B0 = 2870
    B1 = 3000
    Bc = meanmin(sum1, 5)

    normB = (sum1-Bc)/(sum2-Bc)

    y = normB
    alp0 = scan[np.argmax(y)]
    scan = scan - alp0

    p0 = [np.max(y), (scan[-1]-scan[0])/7, 0, 0]
    lb = [0, 100, -50000, 0]
    ub = [0.5, 100000, 50000, 1]
    popt, pcov = curve_fit(gaus, scan, y, p0=p0, maxfev=1000, bounds=(lb,ub))
    A, k, alp0, B = popt
    A_m.append(A)



# show data
A_m = np.array(A_m)
plt.scatter(ty_m, A_m)
plt.plot(ty_m, A_m)

# fit
c1 = 0
c2 = -7
p0 = [np.pi/ty_m[np.argmax(A_m)],(np.max(A_m) - np.min(A_m))/2, np.min(A_m), 2*ty_m[np.argmax(A_m)]]
popt, pcov = curve_fit(Rabifit, ty_m[c1:c2], A_m[c1:c2], p0=p0)
w, A, B, tc = popt

# show fit
ty0 = np.linspace(ty_m[0], ty_m[-7], 1000)
plt.plot(ty0, Rabifit(ty0, w, A, B, tc))
print(f"Weff={w*1e3} кГц")
print(f"typ = {np.pi/w}")


plt.show()