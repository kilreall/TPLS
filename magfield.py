import numpy as np
import matplotlib.pyplot as plt

filename = r"datav2\2026-07-01\TPLS\magnetic_field.csv"
freq, amp = np.loadtxt(filename, delimiter=',', skiprows=1, unpack=True)

plt.plot(freq, amp)

right = 6.834998e9
left = 6.834451e9
dif = right - left
print(f"dif={dif*1e-3} KHz")
gf = 2*0.7e6 # Hz/G

print(f"B = {dif/gf*1e3} mG")

plt.show()
