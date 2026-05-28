# ----------------------------------------------------------
# Fase 4: Cálculo de distancias Ri
# Proyecto: Localización de una fuente sísmica
# ----------------------------------------------------------

import math

# ----------------------------------------------------------
# 1. Fuente sísmica real simulada
# ----------------------------------------------------------
x0 = 1.2
y0 = -0.8
z0 = -1.1

# ----------------------------------------------------------
# 2. Coordenadas de los sensores sísmicos
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
# 3. Cálculo de la distancia Ri para cada sensor
# Fórmula:
# Ri = sqrt((x_i - x0)^2 + (y_i - y0)^2 + (z_i - z0)^2)
# ----------------------------------------------------------
distancias = []

for sensor in sensores:
    x_i = sensor[0]
    y_i = sensor[1]
    z_i = sensor[2]

    diferencia_x = x_i - x0
    diferencia_y = y_i - y0
    diferencia_z = z_i - z0

    R_i = math.sqrt(
        diferencia_x**2 +
        diferencia_y**2 +
        diferencia_z**2
    )

    distancias.append(R_i)

# ----------------------------------------------------------
# 4. Impresión de resultados
# ----------------------------------------------------------
print("----------------------------------------------------------")
print("Cálculo de distancias entre sensores y fuente sísmica")
print("----------------------------------------------------------")
print("Sensor\t x_i\t y_i\t z_i\t R_i")

for i, sensor in enumerate(sensores, start=1):
    print(
        f"S{i}\t "
        f"{sensor[0]}\t "
        f"{sensor[1]}\t "
        f"{sensor[2]}\t "
        f"{distancias[i-1]:.4f}"
    )

print("----------------------------------------------------------")
print(f"Total de distancias calculadas: {len(distancias)}")
print("----------------------------------------------------------")