import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm

# ============================================================
# DATOS ORIGINALES (SIN CAMBIOS)
# ============================================================
source_label = "Fuente Real"
source_coords = np.array([1.2, -0.8, -1.1])

sensors_data = [
    ("S1",  -4.0, -3.0,  0.2),
    ("S2",  -2.5,  2.8, -0.1),
    ("S3",   0.0,  4.0,  0.1),
    ("S4",   3.5,  3.0, -0.2),
    ("S5",   4.5, -1.5,  0.0),
    ("S6",   2.0, -4.0,  0.3),
    ("S7",  -1.0, -4.0, -0.1),
    ("S8",  -4.5,  1.0,  0.2),
    ("S9",   0.5,  0.5,  0.0),
    ("S10",  2.8,  0.8, -0.3),
    ("S11", -1.8, -1.2,  0.1),
    ("S12",  1.0,  3.2,  0.2)
]

SURFACE_Z = 10.0   # plano del terreno

# Conversión de la fuente al sistema de coordenadas con superficie en z=10
source_plot = np.array([source_coords[0], source_coords[1], source_coords[2]])

# ============================================================
# CONFIGURACIÓN DE LA FIGURA (ESTILO OSCURO MINIMALISTA)
# ============================================================
plt.style.use('dark_background')
fig = plt.figure(figsize=(18, 14), dpi=150)
ax = fig.add_subplot(111, projection='3d', facecolor='#0b0b10')

# Paneles y rejilla sutiles
ax.xaxis.pane.fill = False
ax.yaxis.pane.fill = False
ax.zaxis.pane.fill = False
ax.grid(True, color='#2a2a3a', linestyle='-', linewidth=0.4, alpha=0.7)

# ============================================================
# SUPERFICIE SEMITRANSPARENTE MEJORADA
# ============================================================
x_surf = np.linspace(-6, 6, 50)
y_surf = np.linspace(-6, 6, 50)
X, Y = np.meshgrid(x_surf, y_surf)
Z = np.full_like(X, SURFACE_Z)

# Superficie principal con efecto vidrio esmerilado
surf = ax.plot_surface(X, Y, Z, alpha=0.3, color='#1a4a6a', 
                       rstride=1, cstride=1, linewidth=0, 
                       antialiased=True, shade=True)

# Contorno fino para resaltar el plano
ax.contour(X, Y, Z, levels=[SURFACE_Z], colors='cyan', 
           linewidths=0.8, alpha=0.4, linestyles='-')

# Líneas de rejilla sobre la superficie (opcional)
# ax.plot_wireframe(X, Y, Z, color='cyan', alpha=0.1, linewidth=0.2)

# ============================================================
# FUENTE SÍSMICA (ROJA BRILLANTE, CLARAMENTE SUBTERRÁNEA)
# ============================================================
ax.scatter(*source_plot, color='#FF2222', s=350, marker='*', 
           edgecolors='white', linewidth=1.5, zorder=20, 
           label='_nolegend_', alpha=1.0)

# Línea vertical desde la fuente hasta la superficie (indica profundidad)
ax.plot([source_plot[0], source_plot[0]], 
        [source_plot[1], source_plot[1]], 
        [source_plot[2], SURFACE_Z], 
        color='red', linewidth=1.2, alpha=0.5, linestyle='--')

# Etiqueta de la fuente con caja limpia
ax.text(source_plot[0] + 0.5, source_plot[1] - 0.8, source_plot[2] - 0.6,
        f'{source_label}\n(1.2, -0.8, -1.1)',
        color='#FF4444', fontsize=12, fontweight='bold',
        bbox=dict(boxstyle='round,pad=0.3', facecolor='#0b0b10', 
                 edgecolor='red', alpha=0.85))

# ============================================================
# SENSORES CON ATENUACIÓN (TAMAÑO Y COLOR SEGÚN DISTANCIA)
# ============================================================
sensor_coords = np.array([(x, y, z) for _, x, y, z in sensors_data])
distances = np.sqrt(np.sum((sensor_coords - source_plot)**2, axis=1))
dist_max = distances.max()
dist_min = distances.min()

# Mapeo de distancia a tamaño y opacidad (más cercano = más grande, más opaco)
sizes = 50 + 110 * (1 - (distances - dist_min) / (dist_max - dist_min + 1e-6))
alphas = 0.6 + 0.4 * (1 - (distances - dist_min) / (dist_max - dist_min + 1e-6))

# Paleta azul personalizada
cmap = cm.Blues
colors = cmap(0.4 + 0.6 * (1 - (distances - dist_min) / (dist_max - dist_min + 1e-6)))

for i, (name, x, y, z) in enumerate(sensors_data):
    ax.scatter(x, y, z, color=colors[i], s=sizes[i], edgecolors='white', 
               linewidth=0.8, alpha=alphas[i], zorder=10)
    # Etiqueta compacta con fuente pequeña
    ax.text(x + 0.15, y + 0.15, z + 0.3,
            f'{name} ({x:.1f}, {y:.1f}, {z:.1f})',
            color='white', fontsize=7, alpha=0.9,
            bbox=dict(facecolor='#0b0b10', alpha=0.5, edgecolor='none', pad=0.2))

# ============================================================
# CONEXIONES BLANCAS FINAS (DISTANCIAS EUCLIDIANAS)
# ============================================================
for i, (_, x, y, z) in enumerate(sensors_data):
    ax.plot([source_plot[0], x], [source_plot[1], y], [source_plot[2], z],
            color='white', linewidth=0.5, alpha=0.2, linestyle='-', zorder=1)

# Destacar Ri (S9)
hx, hy, hz = sensors_data[8][1], sensors_data[8][2], sensors_data[8][3]
mid = ((source_plot[0] + hx)/2, (source_plot[1] + hy)/2, (source_plot[2] + hz)/2)
ax.plot([source_plot[0], hx], [source_plot[1], hy], [source_plot[2], hz],
        color='yellow', linewidth=2.0, alpha=0.95, linestyle='-', zorder=15)
ax.text(mid[0] + 0.4, mid[1] - 0.3, mid[2] + 0.1,
        r'$\mathbf{R_i}$', color='yellow', fontsize=16, fontweight='bold')

# ============================================================
# ANILLOS DE PROPAGACIÓN DE ONDAS (ONDAS SÍSMICAS)
# ============================================================
theta = np.linspace(0, 2*np.pi, 100)
radii = np.arange(1.5, 7.5, 1.0)
for r in radii:
    xc = source_plot[0] + r * np.cos(theta)
    yc = source_plot[1] + r * np.sin(theta)
    zc = np.full_like(xc, source_plot[2])
    ax.plot(xc, yc, zc, color='cyan', alpha=0.25 - r*0.03, 
            linewidth=1.0, linestyle='-', zorder=2)
    # Anillo secundario desplazado verticalmente para efecto 3D
    ax.plot(xc, yc, zc - 0.3, color='cyan', alpha=0.1, 
            linewidth=0.5, linestyle=':', zorder=1)

# ============================================================
# EJES Y ETIQUETAS
# ============================================================
ax.set_xlabel('X (km) →', color='white', fontsize=14, labelpad=20)
ax.set_ylabel('Y (km) →', color='white', fontsize=14, labelpad=20)
ax.set_zlabel('Z (km)   Profundidad / Elevación', color='white', fontsize=14, labelpad=20)

ax.tick_params(axis='x', colors='white', labelsize=10)
ax.tick_params(axis='y', colors='white', labelsize=10)
ax.tick_params(axis='z', colors='white', labelsize=10)

ax.set_xlim(-5.5, 5.5)
ax.set_ylim(-5.5, 5.5)
ax.set_zlim(-3, 12)

# Indicador visual del nivel del terreno
ax.text(-5.2, 5.2, SURFACE_Z + 0.5, 'Superficie (z = 10)', 
        color='cyan', fontsize=10, alpha=0.9)

# Marcas de profundidad
ax.text(-5.5, 5.0, source_plot[2] - 0.3, 'Profundidad\nsubterránea', 
        color='#FF6666', fontsize=9, alpha=0.8)

# ============================================================
# ECUACIONES DEL PROBLEMA DIRECTO (MULTIVARIABLE)
# ============================================================
eq_text = (r'$\mathbf{Problema\ Directo\ Sísmico}$' + '\n' +
           r'$D_i(t) = \dfrac{W(t - R_i/v)}{R_i}\, e^{-\alpha R_i}$' + '\n' +
           r'$R_i(\mathbf{x}) = \sqrt{(x-x_0)^2 + (y-y_0)^2 + (z-z_0)^2}$')
ax.text2D(0.02, 0.97, eq_text, transform=ax.transAxes,
          fontsize=14, color='white', va='top',
          bbox=dict(boxstyle='round,pad=0.8', facecolor='#0b0b10', 
                   edgecolor='cyan', alpha=0.8))

# ============================================================
# ÁNGULO DE VISIÓN Y RENDERIZADO FINAL
# ============================================================
ax.view_init(elev=22, azim=-60)  # perspectiva elegante
plt.tight_layout()
plt.savefig('problema_directo_sismico_mejorado.png', dpi=300, 
            bbox_inches='tight', facecolor=fig.get_facecolor())
plt.show()
print("✓ Gráfica mejorada generada con éxito.")