import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

def fitf(a, A, B, phi0):
    return A*np.sin(2*np.pi*T**2*a + phi0) + B

def noisef(normc):
    y = normc
    p0 = [(np.max(y)-np.min(y))/2, np.min(y), 0]

    popt, pcov = curve_fit(fitf, scan, y, p0)

    noise = np.sqrt(pcov[2,2])

    return noise

def B_func(B1, B2):
    normc = (sum1 - B1) / (sum2 - B2)
    return noisef(normc)

# --------------------
# data initializing
# --------------------
T = 7e-3
filename = r"datav2\2026-06-30\TPLS\800mv_k-.csv"
data = np.loadtxt(filename, delimiter=',', skiprows=1, unpack=True)

scan = data[3]
sum1 = data[0]
sum2 = data[1]
normd = data[2]



# диапазоны B1 и B2
Bm = 0
Bb = np.min(sum1)
B1_m = np.linspace(Bm, Bb, 100)
B2_m = np.linspace(Bm, Bb, 100)

B1_grid, B2_grid = np.meshgrid(B1_m, B2_m)

# --------------------
# расчет поверхности
# --------------------
Z = np.empty_like(B1_grid)

for i in range(B1_grid.shape[0]):
    for j in range(B1_grid.shape[1]):
        Z[i, j] = B_func(B1_grid[i, j], B2_grid[i, j])

# --------------------
# draw
# --------------------
fig = plt.figure(figsize=(8, 8))
ax = fig.add_subplot(111, projection='3d')

ax.plot_surface(B1_grid, B2_grid, Z)

ax.set_xlabel('B1')
ax.set_ylabel('B2')
ax.set_zlabel('noise')

fig1, ax1 = plt.subplots(figsize=(8, 8))

im = ax1.contourf(
    B1_grid,
    B2_grid,
    Z,
    levels=50,
    cmap='viridis'
)

ax1.set_xlabel('B1')
ax1.set_ylabel('B2')

cbar = plt.colorbar(im)
cbar.set_label('Noise')

# B1Z

Z_xz = np.nanmin(Z, axis=0)

fig_xz, ax_xz = plt.subplots(figsize=(8, 6))

ax_xz.plot(
    B1_m,
    Z_xz,
    lw=2
)

ax_xz.set_xlabel('B1')
ax_xz.set_ylabel('Noise')
ax_xz.set_title('B1N projection')

ax_xz.grid(True)

# B2Z

Z_xy = np.nanmin(Z, axis=1)

fig_xy, ax_xy = plt.subplots(figsize=(8, 6))

ax_xy.plot(
    B1_m,
    Z_xy,
    lw=2
)

ax_xy.set_xlabel('B2')
ax_xy.set_ylabel('Noise')
ax_xy.set_title('B2N projection')

ax_xy.grid(True)

# поиска минимума
idx = np.unravel_index(np.nanargmin(Z), Z.shape)

i_min, j_min = idx

B1_min = B1_grid[i_min, j_min]
B2_min = B2_grid[i_min, j_min]
Noise_min = Z[i_min, j_min]

print("\nMinimum found:")
print(f"B1    = {B1_min:.6f}")
print(f"B2    = {B2_min:.6f}")
print(f"Noise = {Noise_min:.6e}")


plt.show()