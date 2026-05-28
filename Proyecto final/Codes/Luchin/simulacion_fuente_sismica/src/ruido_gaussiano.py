# ----------------------------------------------------------
# Fase 6: Incorporación de ruido gaussiano moderado
# Proyecto: Localización de una fuente sísmica
# ----------------------------------------------------------

import random

# ----------------------------------------------------------
# 1. Factor de ruido moderado
# alpha = 0.05 representa un ruido del 5 %
# ----------------------------------------------------------
alpha = 0.05

# ----------------------------------------------------------
# 2. Semilla aleatoria
# La semilla permite que los resultados sean reproducibles.
# Es decir, cada vez que se ejecute el programa, se obtendrán
# los mismos valores de ruido.
# ----------------------------------------------------------
random.seed(42)

# ----------------------------------------------------------
# 3. Amplitudes ideales calculadas previamente
# Estos valores vienen de la Fase 5
# ----------------------------------------------------------
amplitudes_ideales = [
    0.005257,
    0.009897,
    0.012081,
    0.023737,
    0.081101,
    0.077537,
    0.027250,
    0.003604,
    0.861541,
    0.377991,
    0.118404,
    0.035234
]

# ----------------------------------------------------------
# 4. Cálculo de sigma, ruido gaussiano y amplitud observada
# sigma_i = alpha * A_ideal_i
# epsilon_i ~ N(0, sigma_i)
# A_obs_i = A_ideal_i + epsilon_i
# ----------------------------------------------------------
sigmas = []
ruidos = []
amplitudes_observadas = []

for A_ideal_i in amplitudes_ideales:
    sigma_i = alpha * A_ideal_i
    epsilon_i = random.gauss(0, sigma_i)
    A_obs_i = A_ideal_i + epsilon_i

    sigmas.append(sigma_i)
    ruidos.append(epsilon_i)
    amplitudes_observadas.append(A_obs_i)

# ----------------------------------------------------------
# 5. Impresión de resultados
# ----------------------------------------------------------
print("--------------------------------------------------------------------------")
print("Incorporación de ruido gaussiano moderado")
print("--------------------------------------------------------------------------")
print("Sensor\t A_ideal\t Sigma\t\t Ruido\t\t A_observada")

for i in range(len(amplitudes_ideales)):
    print(
        f"S{i+1}\t "
        f"{amplitudes_ideales[i]:.6f}\t "
        f"{sigmas[i]:.6f}\t "
        f"{ruidos[i]:.6f}\t "
        f"{amplitudes_observadas[i]:.6f}"
    )

print("--------------------------------------------------------------------------")
print(f"Total de amplitudes observadas calculadas: {len(amplitudes_observadas)}")
print("--------------------------------------------------------------------------")