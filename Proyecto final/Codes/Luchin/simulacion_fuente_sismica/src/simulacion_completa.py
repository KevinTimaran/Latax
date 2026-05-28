# ----------------------------------------------------------
# Simulación completa de datos sísmicos
# Proyecto: Localización de una fuente sísmica
# Materia: Cálculo Multivariado
# ----------------------------------------------------------

import os
import csv
import math
import random
import matplotlib.pyplot as plt

# ----------------------------------------------------------
# 1. Parámetros de la fuente sísmica real simulada
# ----------------------------------------------------------

x0 = 1.2
y0 = -0.8
z0 = -1.1
A0 = 10

# ----------------------------------------------------------
# 2. Parámetros del ruido gaussiano
# ----------------------------------------------------------

alpha = 0.05
random.seed(42)

# ----------------------------------------------------------
# 3. Coordenadas de los sensores sísmicos
# Cada sensor se representa como [x_i, y_i, z_i]
# ----------------------------------------------------------

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

# ----------------------------------------------------------
# 4. Listas donde se guardarán los resultados
# ----------------------------------------------------------

distancias = []
amplitudes_ideales = []
sigmas = []
ruidos = []
amplitudes_observadas = []
datos_simulados = []

# ----------------------------------------------------------
# 5. Cálculo de distancias, amplitudes ideales,
#    ruido gaussiano y amplitudes observadas
# ----------------------------------------------------------

for i, sensor in enumerate(sensores, start=1):
    x_i = sensor[0]
    y_i = sensor[1]
    z_i = sensor[2]

    # Distancia entre la fuente y el sensor
    R_i = math.sqrt(
        (x_i - x0) ** 2 +
        (y_i - y0) ** 2 +
        (z_i - z0) ** 2
    )

    # Amplitud ideal sin ruido
    A_ideal_i = A0 * math.exp(-R_i) / R_i

    # Desviación estándar del ruido
    sigma_i = alpha * A_ideal_i

    # Ruido gaussiano
    ruido_i = random.gauss(0, sigma_i)

    # Amplitud observada
    A_observada_i = A_ideal_i + ruido_i

    # Guardar resultados en listas
    distancias.append(R_i)
    amplitudes_ideales.append(A_ideal_i)
    sigmas.append(sigma_i)
    ruidos.append(ruido_i)
    amplitudes_observadas.append(A_observada_i)

    # Guardar fila completa
    datos_simulados.append([
        f"S{i}",
        x_i,
        y_i,
        z_i,
        R_i,
        A_ideal_i,
        sigma_i,
        ruido_i,
        A_observada_i
    ])

# ----------------------------------------------------------
# 6. Mostrar tabla final en terminal
# ----------------------------------------------------------

print("--------------------------------------------------------------------------------------------------------------")
print("Tabla final de datos simulados")
print("--------------------------------------------------------------------------------------------------------------")
print("Sensor\t x_i\t y_i\t z_i\t R_i\t A_ideal\t Sigma\t\t Ruido\t\t A_observada")

for fila in datos_simulados:
    print(
        f"{fila[0]}\t "
        f"{fila[1]:.1f}\t "
        f"{fila[2]:.1f}\t "
        f"{fila[3]:.1f}\t "
        f"{fila[4]:.4f}\t "
        f"{fila[5]:.6f}\t "
        f"{fila[6]:.6f}\t "
        f"{fila[7]:.6f}\t "
        f"{fila[8]:.6f}"
    )

print("--------------------------------------------------------------------------------------------------------------")
print(f"Total de registros simulados: {len(datos_simulados)}")
print("--------------------------------------------------------------------------------------------------------------")

# ----------------------------------------------------------
# 7. Crear carpetas de salida si no existen
# ----------------------------------------------------------

carpeta_datos = "datos"
carpeta_graficas = "graficas"

if not os.path.exists(carpeta_datos):
    os.makedirs(carpeta_datos)

if not os.path.exists(carpeta_graficas):
    os.makedirs(carpeta_graficas)

# ----------------------------------------------------------
# 8. Exportar datos a CSV
# ----------------------------------------------------------

ruta_csv = os.path.join(carpeta_datos, "datos_sismicos_simulados_completo.csv")

encabezados = [
    "Sensor",
    "x_i",
    "y_i",
    "z_i",
    "R_i",
    "A_ideal",
    "Sigma",
    "Ruido",
    "A_observada"
]

with open(ruta_csv, mode="w", newline="", encoding="utf-8") as archivo_csv:
    escritor = csv.writer(archivo_csv)
    escritor.writerow(encabezados)
    escritor.writerows(datos_simulados)

print("Archivo CSV generado correctamente:")
print(ruta_csv)

# ----------------------------------------------------------
# 9. Crear gráfica 3D de sensores y fuente sísmica real
# ----------------------------------------------------------

x_sensores = [sensor[0] for sensor in sensores]
y_sensores = [sensor[1] for sensor in sensores]
z_sensores = [sensor[2] for sensor in sensores]

fig = plt.figure(figsize=(9, 7))
ax = fig.add_subplot(111, projection="3d")

# Sensores
ax.scatter(
    x_sensores,
    y_sensores,
    z_sensores,
    marker="^",
    s=80,
    label="Sensores sísmicos"
)

# Fuente real
ax.scatter(
    x0,
    y0,
    z0,
    marker="x",
    s=180,
    label="Fuente sísmica real"
)

# Etiquetas de sensores
for i, sensor in enumerate(sensores, start=1):
    ax.text(
        sensor[0],
        sensor[1],
        sensor[2],
        f"S{i}",
        fontsize=8
    )

ax.set_title("Distribución espacial de sensores y fuente sísmica real")
ax.set_xlabel("Eje x")
ax.set_ylabel("Eje y")
ax.set_zlabel("Eje z")
ax.legend()
ax.grid(True)

ruta_grafica = os.path.join(carpeta_graficas, "sensores_fuente_real_completo.png")

plt.tight_layout()
plt.savefig(ruta_grafica, dpi=300)
plt.show()

print("Gráfica generada correctamente:")
print(ruta_grafica)

# ----------------------------------------------------------
# 10. Resumen final
# ----------------------------------------------------------

print("--------------------------------------------------------------------------------------------------------------")
print("Simulación completa finalizada")
print("--------------------------------------------------------------------------------------------------------------")
print(f"Fuente real simulada: ({x0}, {y0}, {z0})")
print(f"Amplitud inicial A0: {A0}")
print(f"Factor de ruido alpha: {alpha}")
print(f"Número de sensores: {len(sensores)}")
print(f"Archivo CSV: {ruta_csv}")
print(f"Gráfica: {ruta_grafica}")
print("--------------------------------------------------------------------------------------------------------------")