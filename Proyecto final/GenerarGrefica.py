import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import os

# ============================================================
# DATOS DEL PROYECTO
# ============================================================

# Sensores: (x, y, z, A_obs)
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

A0            = 10.0
fuente_real   = np.array([1.2, -0.8, -1.1])
fuente_est    = np.array([1.200079, -0.776502, -1.138095])

os.makedirs("Imagenes", exist_ok=True)

# ============================================================
# FUNCIÓN DE ERROR
# ============================================================

def error(x, y, z):
    xi, yi, zi, Aobs = sensores[:,0], sensores[:,1], sensores[:,2], sensores[:,3]
    Ri    = np.sqrt((xi - x)**2 + (yi - y)**2 + (zi - z)**2)
    Apred = A0 * np.exp(-Ri) / Ri
    return np.sum((Aobs - Apred)**2)

# ============================================================
# GRILLA BASE
# ============================================================

N  = 300
xs = np.linspace(-5, 5, N)
ys = np.linspace(-5, 5, N)
XX, YY = np.meshgrid(xs, ys)

# ============================================================
# 1. MAPAS DE CALOR — 4 cortes de profundidad
# ============================================================

cortes = {
    "z = -0.50  (plano superficial)":  (-0.50, "corte_z_050.png"),
    "z = -1.10  (profundidad real)":   (-1.10, "corte_z_110.png"),
    "z = -1.14  (profundidad estimada)":(-1.14, "corte_z_114.png"),
    "z = -1.70  (plano profundo)":     (-1.70, "corte_z_170.png"),
}

for titulo, (z_val, nombre) in cortes.items():

    EE = np.zeros_like(XX)
    for i in range(N):
        for j in range(N):
            EE[i, j] = error(XX[i, j], YY[i, j], z_val)

    # Recorte para visualizar mejor (percentil 95)
    vmax = np.percentile(EE, 95)

    fig, ax = plt.subplots(figsize=(6, 5))

    pcm = ax.pcolormesh(XX, YY, EE,
                        cmap="coolwarm_r",
                        vmin=EE.min(), vmax=vmax,
                        shading="auto")

    # Curvas de nivel
    niveles = np.linspace(EE.min(), vmax, 12)
    ax.contour(XX, YY, EE, levels=niveles,
               colors="black", linewidths=0.5, alpha=0.5)

    # Fuente real y estimada
    ax.plot(*fuente_real[:2], "w*", markersize=12,
            label="Fuente real", zorder=5)
    ax.plot(*fuente_est[:2],  "yx", markersize=10,
            markeredgewidth=2, label="Fuente estimada", zorder=5)

    # Sensores
    ax.scatter(sensores[:,0], sensores[:,1],
               c="white", edgecolors="black",
               s=40, zorder=6, label="Sensores")

    plt.colorbar(pcm, ax=ax, label="$E(x,y,z)$")
    ax.set_xlabel("$x$", fontsize=11)
    ax.set_ylabel("$y$", fontsize=11)
    ax.set_title(f"Mapa de calor — {titulo}", fontsize=10)
    ax.legend(fontsize=8, loc="upper left")
    ax.set_aspect("equal")

    plt.tight_layout()
    plt.savefig(f"Imagenes/{nombre}", dpi=150, bbox_inches="tight")
    plt.close()
    print(f"Guardada: Imagenes/{nombre}")

# ============================================================
# 2. GRÁFICA Emin(z)
# ============================================================

zs     = np.linspace(-3, 1, 200)
Emin_z = []

for z_val in zs:
    EE = np.array([error(XX[i,j], YY[i,j], z_val)
                   for i in range(N) for j in range(N)])
    Emin_z.append(EE.min())

Emin_z = np.array(Emin_z)

fig, ax = plt.subplots(figsize=(7, 4))
ax.plot(zs, Emin_z, color="steelblue", linewidth=2)

# Marcar profundidades clave
for z_mark, etiqueta, color in [
    (-0.50,  "$z=-0.50$",  "gray"),
    (-1.10,  "$z=-1.10$ (real)",  "green"),
    (-1.14,  "$z=-1.14$ (est.)", "orange"),
    (-1.70,  "$z=-1.70$",  "red"),
]:
    idx   = np.argmin(np.abs(zs - z_mark))
    ax.axvline(z_mark, color=color, linestyle="--", linewidth=1, alpha=0.7)
    ax.plot(zs[idx], Emin_z[idx], "o", color=color, markersize=6)
    ax.text(z_mark + 0.04, Emin_z[idx] * 1.05,
            etiqueta, fontsize=8, color=color)

ax.set_xlabel("Profundidad $z$", fontsize=11)
ax.set_ylabel("$E_{\\min}(z)$",  fontsize=11)
ax.set_title("Valor mínimo del error por profundidad $E_{\\min}(z)$", fontsize=11)
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("Imagenes/emin_z.png", dpi=150, bbox_inches="tight")
plt.close()
print("Guardada: Imagenes/emin_z.png")

# ============================================================
# 3. TRAYECTORIA DEL MÍNIMO en el plano (x,y)
# ============================================================

zs_tray = np.linspace(-3, 1, 100)
tray_x, tray_y, tray_E = [], [], []

for z_val in zs_tray:
    EE   = np.array([[error(XX[i,j], YY[i,j], z_val)
                       for j in range(N)] for i in range(N)])
    idx  = np.unravel_index(EE.argmin(), EE.shape)
    tray_x.append(XX[idx])
    tray_y.append(YY[idx])
    tray_E.append(EE[idx])

tray_x = np.array(tray_x)
tray_y = np.array(tray_y)
tray_E = np.array(tray_E)

fig, ax = plt.subplots(figsize=(6, 5))

sc = ax.scatter(tray_x, tray_y, c=zs_tray,
                cmap="plasma", s=15, zorder=3)
plt.colorbar(sc, ax=ax, label="Profundidad $z$")

# Fuente real y estimada
ax.plot(*fuente_real[:2], "g*", markersize=14,
        label="Fuente real", zorder=6)
ax.plot(*fuente_est[:2],  "rx", markersize=10,
        markeredgewidth=2, label="Fuente estimada", zorder=6)

# Sensores
ax.scatter(sensores[:,0], sensores[:,1],
           c="gray", edgecolors="black",
           s=40, zorder=5, label="Sensores")

ax.set_xlabel("$x$", fontsize=11)
ax.set_ylabel("$y$", fontsize=11)
ax.set_title("Trayectoria del mínimo en el plano $(x,y)$", fontsize=11)
ax.legend(fontsize=8)
ax.set_aspect("equal")
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("Imagenes/trayectoria_minimo.png", dpi=150, bbox_inches="tight")
plt.close()
print("Guardada: Imagenes/trayectoria_minimo.png")

print("\nTodas las imágenes generadas correctamente.")