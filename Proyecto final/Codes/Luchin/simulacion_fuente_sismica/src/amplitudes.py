# ----------------------------------------------------------
# Fase 5: Cálculo de amplitudes ideales
# Proyecto: Localización de una fuente sísmica
# ----------------------------------------------------------

import math

# ----------------------------------------------------------
# 1. Amplitud inicial de la fuente sísmica
# ----------------------------------------------------------
A0 = 10.0

# ----------------------------------------------------------
# 2. Distancias calculadas previamente entre sensores y fuente
# Estos valores vienen de la Fase 4
# ----------------------------------------------------------
distancias = [
    5.7940,
    5.2583,
    5.0912,
    4.5321,
    3.5482,
    3.5833,
    4.4193,
    6.1172,
    1.8412,
    2.4000,
    3.2558,
    4.2107
]

# ----------------------------------------------------------
# 3. Cálculo de amplitudes ideales
# Fórmula:
# A_ideal_i = A0 * e^(-R_i) / R_i
# En Python:
# A_ideal_i = A0 * math.exp(-R_i) / R_i
# ----------------------------------------------------------
amplitudes_ideales = []

for R_i in distancias:
    A_ideal_i = A0 * math.exp(-R_i) / R_i
    amplitudes_ideales.append(A_ideal_i)

# ----------------------------------------------------------
# 4. Impresión de resultados
# ----------------------------------------------------------
print("----------------------------------------------------------")
print("Cálculo de amplitudes ideales sin ruido")
print("----------------------------------------------------------")
print("Sensor\t R_i\t\t Amplitud ideal")

for i, amplitud in enumerate(amplitudes_ideales, start=1):
    print(
        f"S{i}\t "
        f"{distancias[i-1]:.4f}\t\t "
        f"{amplitud:.6f}"
    )

print("----------------------------------------------------------")
print(f"Total de amplitudes ideales calculadas: {len(amplitudes_ideales)}")
print("----------------------------------------------------------")
