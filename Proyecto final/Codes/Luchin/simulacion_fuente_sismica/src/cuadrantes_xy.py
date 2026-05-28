# ----------------------------------------------------------
# Visualizacion 2D de sensores por cuadrantes (plano XY)
# Proyecto: Localizacion de una fuente sismica
# ----------------------------------------------------------

import os
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

# Coordenadas de sensores [x_i, y_i, z_i]
sensores = [
    [-4.0, -3.0,  0.2],
    [-2.5,  2.8, -0.1],
    [ 0.0,  4.0,  0.1],
    [ 3.5,  3.0, -0.2],
    [ 4.5, -1.5,  0.0],
    [ 2.0, -4.0,  0.3],
    [-1.0, -4.5, -0.1],
    [-4.5,  1.0,  0.2],
    [ 0.5,  0.5,  0.0],
    [ 2.8,  0.8, -0.3],
    [-1.8, -1.2,  0.1],
    [ 1.0,  3.2,  0.2]
]

# Fuente sismica real
x0 = 1.2
y0 = -0.8

# Salidas
carpeta_graficas = "graficas"
if not os.path.exists(carpeta_graficas):
    os.makedirs(carpeta_graficas)

# Datos XY
x_sensores = [s[0] for s in sensores]
y_sensores = [s[1] for s in sensores]

fig, ax = plt.subplots(figsize=(8, 8))

# Lineas de ejes para cuadrantes
ax.axhline(0, color="black", linewidth=1.2)
ax.axvline(0, color="black", linewidth=1.2)

# Determinar limites con margen
margin = 1.0
xmin = min(x_sensores + [x0]) - margin
xmax = max(x_sensores + [x0]) + margin
ymin = min(y_sensores + [y0]) - margin
ymax = max(y_sensores + [y0]) + margin
ax.set_xlim(xmin, xmax)
ax.set_ylim(ymin, ymax)

# Sombrear cuadrantes: QI (x>0,y>0), QII (x<0,y>0), QIII (x<0,y<0), QIV (x>0,y<0)
ax.add_patch(Rectangle((0, 0), xmax - 0, ymax - 0, facecolor="#ffe6e6", alpha=0.3, zorder=0))
ax.add_patch(Rectangle((xmin, 0), 0 - xmin, ymax - 0, facecolor="#e6f0ff", alpha=0.25, zorder=0))
ax.add_patch(Rectangle((xmin, ymin), 0 - xmin, 0 - ymin, facecolor="#f0f0f0", alpha=0.25, zorder=0))
ax.add_patch(Rectangle((0, ymin), xmax - 0, 0 - ymin, facecolor="#e6ffe6", alpha=0.25, zorder=0))

# Etiquetas de cuadrantes en su centro aproximado
ax.text((xmax + 0) / 2, (ymax + 0) / 2, "QI", fontsize=14, fontweight="bold", ha="center", va="center", alpha=0.6)
ax.text((xmin + 0) / 2, (ymax + 0) / 2, "QII", fontsize=14, fontweight="bold", ha="center", va="center", alpha=0.6)
ax.text((xmin + 0) / 2, (ymin + 0) / 2, "QIII", fontsize=14, fontweight="bold", ha="center", va="center", alpha=0.6)
ax.text((xmax + 0) / 2, (ymin + 0) / 2, "QIV", fontsize=14, fontweight="bold", ha="center", va="center", alpha=0.6)

# Sensores
ax.scatter(x_sensores, y_sensores, marker="^", s=90, label="Sensores sismicos")

# Etiquetas de sensores
for i, sensor in enumerate(sensores, start=1):
    ax.text(sensor[0] + 0.08, sensor[1] + 0.08, f"S{i}", fontsize=9, ha="left", va="bottom")

# Fuente real (proyeccion en XY)
ax.scatter(x0, y0, marker="x", s=160, label="Fuente sismica real (XY)")

# Estetica
ax.set_title("Sensores y fuente real en el plano XY")
ax.set_xlabel("Eje x")
ax.set_ylabel("Eje y")
ax.set_aspect("equal", adjustable="box")
ax.grid(True, linestyle="--", alpha=0.4)
ax.legend(loc="upper right")

ruta_grafica = os.path.join(carpeta_graficas, "sensores_cuadrantes_xy.png")
plt.tight_layout()
plt.savefig(ruta_grafica, dpi=300)
plt.show()

print("Grafica XY generada:")
print(ruta_grafica)
