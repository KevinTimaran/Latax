import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import ScalarFormatter
import os

# ============================================================
# DATOS DEL PROYECTO (sin cambios)
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
    [ 0.5,  0.5,  0.0, 0.852685],
    [ 2.8,  0.8, -0.3, 0.380182],
    [-1.8, -1.2,  0.1, 0.119785],
    [ 1.0,  3.2,  0.2, 0.037284],
])

A0          = 10.0
fuente_real = np.array([1.2, -0.8, -1.1])
z_fijo      = -1.10   # profundidad real

os.makedirs("Imagenes", exist_ok=True)

# ============================================================
# FUNCIÓN DE ERROR (sin cambios)
# ============================================================

def error(x, y, z):
    xi, yi, zi, Aobs = sensores[:,0], sensores[:,1], sensores[:,2], sensores[:,3]
    Ri    = np.sqrt((xi - x)**2 + (yi - y)**2 + (zi - z)**2)
    Apred = A0 * np.exp(-Ri) / Ri
    return np.sum((Aobs - Apred)**2)

# ============================================================
# SUPERFICIE 3D SEMI‑TRANSPARENTE – LÍNEA SIEMPRE VISIBLE
# ============================================================

N  = 200
xs = np.linspace(-5, 5, N)
ys = np.linspace(-5, 5, N)
XX, YY = np.meshgrid(xs, ys)

EE = np.zeros_like(XX)
for i in range(N):
    for j in range(N):
        EE[i, j] = error(XX[i, j], YY[i, j], z_fijo)

vmax = np.percentile(EE, 92)
EE_plot = np.clip(EE, None, vmax)

idx_min = np.unravel_index(EE.argmin(), EE.shape)
x_min, y_min, E_min = XX[idx_min], YY[idx_min], EE[idx_min]

# -------------------- Configuración visual --------------------
plt.style.use('dark_background')
fig = plt.figure(figsize=(9, 7), facecolor='black')
ax  = fig.add_subplot(111, projection='3d', facecolor='black')

stride = 6
surf = ax.plot_surface(XX, YY, EE_plot,
                       cmap=cm.plasma,
                       rstride=stride, cstride=stride,
                       linewidth=0.15,
                       edgecolor='#cccccc',
                       antialiased=True,
                       alpha=0.75,          # ← ¡clave! transparencia ligera
                       shade=True,
                       lightsource=plt.matplotlib.colors.LightSource(azdeg=320, altdeg=45))

offset = np.min(EE_plot) * 0.95
ax.contourf(XX, YY, EE_plot, zdir='z', offset=offset,
            levels=50, cmap=cm.plasma, alpha=0.6, antialiased=True)

# ---------- Punto mínimo con halo ----------
ax.scatter(x_min, y_min, E_min,
           color='red', s=400, alpha=0.25, edgecolors='none',
           depthshade=False, zorder=9)
ax.scatter(x_min, y_min, E_min,
           color='red', s=200, alpha=0.4, edgecolors='none',
           depthshade=False, zorder=10)
ax.scatter(x_min, y_min, E_min,
           color='#ff0000', s=160, edgecolor='white',
           linewidth=2.8, depthshade=False,
           label='Mínimo global', zorder=11)

# ---------- Línea vertical siempre visible ----------
# Capa blanca de fondo (ancha y semitransparente)
ax.plot([x_min, x_min], [y_min, y_min], [E_min, vmax],
        color='white', linewidth=5, alpha=0.7, zorder=8)
# Línea roja principal con marcadores cada 10% del recorrido
ax.plot([x_min, x_min], [y_min, y_min], [E_min, vmax],
        color='#ff0000', linestyle='-', linewidth=2.8, alpha=1.0,
        marker='o', markevery=(1, 0.1), markersize=9,
        markerfacecolor='#ff0000', markeredgecolor='white',
        markeredgewidth=2.2, zorder=12)

# ---------- Ejes y etiquetas ----------
ax.set_xlabel("$x$ [km]", fontsize=13, color='white', labelpad=12)
ax.set_ylabel("$y$ [km]", fontsize=13, color='white', labelpad=12)
ax.set_zlabel("$E(x,y)$", fontsize=13, color='white', labelpad=12)

for axis in [ax.xaxis, ax.yaxis, ax.zaxis]:
    axis.set_major_formatter(ScalarFormatter(useMathText=True))
    axis.set_tick_params(labelsize=9, colors='white')
ax.ticklabel_format(style='sci', scilimits=(-2,3), axis='z')

ax.xaxis.pane.fill = False
ax.yaxis.pane.fill = False
ax.zaxis.pane.fill = False
ax.xaxis.pane.set_edgecolor('white')
ax.yaxis.pane.set_edgecolor('white')
ax.zaxis.pane.set_edgecolor('white')

ax.grid(True, color='white', alpha=0.15, linestyle=':')

ax.set_title("Superficie de error $E(x,y)$\n"
             f"(corte en $z = {z_fijo}$ km)",
             fontsize=14, color='white', pad=20,
             bbox=dict(facecolor='black', edgecolor='white',
                       boxstyle='round,pad=0.5', alpha=0.8))

ax.legend(fontsize=10, loc='upper right', framealpha=0.7,
          facecolor='gray', edgecolor='white')

ax.view_init(elev=25, azim=-125)

cbar = fig.colorbar(surf, ax=ax, shrink=0.55, aspect=15, pad=0.08)
cbar.set_label("Error $E$", fontsize=12, color='white')
cbar.ax.yaxis.set_tick_params(color='white', labelcolor='white')
cbar.outline.set_edgecolor('white')

plt.tight_layout()

# ============================================================
# GUARDAR Y MOSTRAR INTERACTIVO
# ============================================================
plt.savefig("Imagenes/superficie_error_3d.png", dpi=200,
            facecolor=fig.get_facecolor(), bbox_inches="tight")
plt.show()

print(f"Mínimo en: x={x_min:.3f}, y={y_min:.3f}, E={E_min:.6e}")
print("Guardada: Imagenes/superficie_error_3d.png")