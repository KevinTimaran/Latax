import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import os

os.makedirs("Imagenes", exist_ok=True)

# ============================================================
# DATOS CORRECTOS — Tabla 1 de David
# ============================================================

sensores = np.array([
    [-4.0, -3.0,  0.2, 0.005219],
    [-2.5,  2.8, -0.1, 0.009811],
    [ 0.0,  4.0,  0.1, 0.012014],
    [ 3.5,  3.0, -0.2, 0.024570],
    [ 4.5, -1.5,  0.0, 0.080580],
    [ 2.0, -4.0,  0.3, 0.071733],
    [-1.0, -4.5, -0.1, 0.027704],
    [-4.5,  1.0,  0.2, 0.003556],
    [ 0.5,  0.5,  0.0, 0.852201],
    [ 2.8,  0.8, -0.3, 0.380182],
    [-1.8, -1.2,  0.1, 0.119785],
    [ 1.0,  3.2,  0.2, 0.037284],
])

A0_est      = 10.0142
fuente_real = np.array([1.2,    -0.8,    -1.1])
fuente_est  = np.array([1.1995, -0.8012, -1.1024])
z_fijo      = -1.10

# ============================================================
# FUNCIÓN DE ERROR
# ============================================================

def error(x, y, z):
    xi, yi, zi, Aobs = sensores[:,0], sensores[:,1], sensores[:,2], sensores[:,3]
    Ri    = np.sqrt((xi-x)**2 + (yi-y)**2 + (zi-z)**2)
    Apred = A0_est * np.exp(-Ri) / Ri
    return np.sum((Aobs - Apred)**2)

# ============================================================
# SUPERFICIE 3D
# ============================================================

N  = 200
xs = np.linspace(-5, 5, N)
ys = np.linspace(-5, 5, N)
XX, YY = np.meshgrid(xs, ys)

EE = np.zeros_like(XX)
for i in range(N):
    for j in range(N):
        EE[i, j] = error(XX[i,j], YY[i,j], z_fijo)

vmax    = np.percentile(EE, 92)
EE_plot = np.clip(EE, None, vmax)

idx_min = np.unravel_index(EE.argmin(), EE.shape)
x_min   = XX[idx_min]
y_min   = YY[idx_min]
E_min   = EE[idx_min]

fig = plt.figure(figsize=(8, 6))
ax  = fig.add_subplot(111, projection='3d')

surf = ax.plot_surface(XX, YY, EE_plot,
                       cmap=cm.viridis,
                       linewidth=0, antialiased=True,
                       alpha=0.92)

# Mínimo
ax.scatter(x_min, y_min, E_min,
           color='red', s=80, depthshade=False,
           label='Mínimo global', zorder=10)
ax.plot([x_min, x_min], [y_min, y_min], [E_min, vmax],
        color='red', linestyle='--', linewidth=1.5)

# Fuente real proyectada
ax.scatter(fuente_real[0], fuente_real[1], 0,
           color='green', s=80, marker='*',
           depthshade=False, label='Fuente real', zorder=10)

ax.set_xlabel('$x$ [km]', fontsize=10, labelpad=8)
ax.set_ylabel('$y$ [km]', fontsize=10, labelpad=8)
ax.set_zlabel('$E(x,y)$',  fontsize=10, labelpad=8)
ax.set_title(f'Superficie de error $E(x,y)$\n'
             f'$z = {z_fijo}$ km, $A_0^* = {A0_est}$', fontsize=11)
ax.view_init(elev=28, azim=-130)
ax.legend(fontsize=8, loc='upper right')
fig.colorbar(surf, ax=ax, shrink=0.5, aspect=12, label='Error $E$')

plt.tight_layout()
plt.savefig("Imagenes/superficie_error_3d.png", dpi=150, bbox_inches="tight")
plt.close()
print("Guardada: Imagenes/superficie_error_3d.png")