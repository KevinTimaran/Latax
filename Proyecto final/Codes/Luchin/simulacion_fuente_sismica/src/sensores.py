# ----------------------------------------------------------
# Fase 3: Definición de sensores sísmicos
# Proyecto: Localización de una fuente sísmica
# ----------------------------------------------------------

# Lista de sensores sísmicos.
# Cada sensor se representa como una lista con tres valores:
# [x_i, y_i, z_i]

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

print("--------------------------------------------------")
print("Coordenadas de los sensores sísmicos")
print("--------------------------------------------------")
print("Sensor\t x_i\t y_i\t z_i")

for i, sensor in enumerate(sensores, start=1):
    x_i = sensor[0]
    y_i = sensor[1]
    z_i = sensor[2]
    print(f"S{i}\t {x_i}\t {y_i}\t {z_i}")

print("--------------------------------------------------")
print(f"Total de sensores definidos: {len(sensores)}")
print("--------------------------------------------------")