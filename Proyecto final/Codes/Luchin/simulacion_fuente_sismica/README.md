# Simulación de Fuente Sísmica

## Descripción

Proyecto de simulación de una fuente sísmica con análisis de ondas y sensores.

## Estructura del Proyecto

```
simulacion_fuente_sismica/
│
├── datos/
│   └── datos_sismicos_simulados.csv    # Datos generados por la simulación
│
├── graficas/
│   └── sensores_fuente_real.png        # Visualización de sensores y fuente
│
├── src/
│   ├── fase_2_fuente_real.py           # Definición de la fuente sísmica
│   ├── fase_3_sensores.py              # Ubicación de sensores
│   ├── fase_4_distancias.py            # Cálculo de distancias
│   ├── fase_5_amplitudes.py            # Cálculo de amplitudes
│   └── simulacion_completa.py          # Orquestación de la simulación
│
├── informe/
│   └── tablas_generadas.txt            # Resultados tabulados
│
└── README.md                           # Este archivo
```

## Fases de la Simulación

- **Fase 2**: Definición de la fuente sísmica real
- **Fase 3**: Ubicación de sensores sísmicos
- **Fase 4**: Cálculo de distancias entre sensores y fuente
- **Fase 5**: Cálculo de amplitudes de ondas sísmicas

## Uso

```bash
python src/simulacion_completa.py
```

## Requisitos

- Python 3.7+
- NumPy (si se requiere para cálculos)
- Matplotlib (para gráficas)

## Autor

[Tu nombre]

## Licencia

[Especificar licencia]
