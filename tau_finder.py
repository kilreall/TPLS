import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

def gaus(alp, A, k, alp0, B):
    return A*np.exp(-(alp-alp0)**2/2/k**2) + B

def lorentz(alp, A, k, alp0, B):
    return A * (k/2)**2/((k/2)**2+(alp-alp0)**2) + B


ty = 28
filename = f"ty{ty}.csv"
sum1, sum2, norm, scan = np.loadtxt(filename, delimiter=',', skiprows=1, unpack=True)
poi = 201
sum1 = sum1[:len(sum1)//poi*poi]
sum2 = sum2[:len(sum2)//poi*poi]
norm = norm[:len(norm)//poi*poi]
scan = scan[:len(scan)//poi*poi]

print(len(sum1))

B0 = 2870
B1 = 3000
Bc = sum1[200]

normB = (sum1-Bc)/(sum2-Bc)

y = normB
alp0 = scan[np.argmax(y)]
scan = scan - alp0
# show data
plt.plot(scan, y)
p0 = [np.max(y), (scan[-1]-scan[0])/7, 0, 0]
lb = [0, 100, -50000, 0]
ub = [0.5, 100000, 50000, 1]
popt, pcov = curve_fit(gaus, scan, y, p0=p0, maxfev=1000, bounds=(lb,ub))
A, k, alp0, B = popt
print(A, k, alp0, B)

# show fit
scan0 = np.linspace(scan[0], scan[-1], 5000)
plt.plot(scan0, gaus(scan0, A, k, alp0, B))
print(A)
dA = np.sqrt(pcov[0,0])
print(dA, dA/A*100)


plt.show()


