# 🎤 Guión de Exposición — Kevin
## Proyecto: Localización de la Fuente Sísmica

> **Total de diapositivas:** 8  
> **Números:** 7, 8, 18, 19, 39, 40, 41, 42  
> **Módulos:** Parte 1 (introducción matemática) + Parte 2 (ruido gaussiano) + Parte 5 (conclusiones y defensa)

---

## PARTE 1 — Introducción y Modelo Matemático

---

### Diapositiva 7 — Modelo de Atenuación Sísmica
**Archivo:** `secciones/Parte_1/05_Introducir_atenuación_sísmica.tex`

#### ¿Qué hay en esta diapositiva?
La diapositiva presenta la **fórmula central de todo el proyecto**:

$$A_{pred,i} = A_0 \frac{e^{-R_i}}{R_i}$$

A la izquierda hay una imagen que muestra cómo se propaga y atenúa la onda sísmica desde la fuente. A la derecha se explica el significado de cada componente:

- **A₀** — amplitud inicial de la fuente (cuánta energía libera el sismo en el origen).
- **e^{−Rᵢ}** — factor de atenuación: la energía de la onda se pierde a medida que viaja por el suelo.
- **1/Rᵢ** — dispersión geométrica: la onda se "abre" en el espacio, por eso pierde fuerza.
- **Rᵢ** — distancia entre la fuente sísmica y el sensor *i*.

Al final hay una frase resumen: *"La amplitud disminuye a medida que aumenta la distancia entre la fuente y el sensor."*

#### ¿Qué debes explicar?
1. **Presentar la fórmula** como el modelo matemático que conecta la posición de la fuente con lo que miden los sensores.
2. **Explicar A₀**: es la amplitud inicial, cuánta energía liberó el sismo. No la conocemos con exactitud al principio —es una de las 4 incógnitas que el algoritmo va a estimar.
3. **Explicar e^{−Rᵢ}**: mientras más lejos está el sensor, más se ha absorbido la energía en el camino. Ese decaimiento exponencial lo representa el término *e* elevado a *-R*.
4. **Explicar 1/Rᵢ**: además de la absorción, la onda se dispersa geométricamente —como cuando tiras una piedra al agua y los círculos se hacen más grandes y menos altos.

---

### Diapositiva 8 — Distancia Euclidiana en ℝ³
**Archivo:** `secciones/Parte_1/06_distancia_euclidiana.tex`

#### ¿Qué hay en esta diapositiva?
La diapositiva presenta la **fórmula de la distancia euclidiana en el espacio tridimensional**:

$$R_i = \sqrt{(x_i - x)^2 + (y_i - y)^2 + (z_i - z)^2}$$

A la izquierda está la fórmula con la explicación de sus variables:
- **(xᵢ, yᵢ, zᵢ)** — coordenadas conocidas del sensor *i* (las tenemos de antemano).
- **(x, y, z)** — posición estimada de la fuente sísmica (esto es lo que queremos encontrar).
- **Rᵢ** — distancia tridimensional entre la fuente y el sensor.

A la derecha hay una imagen que ilustra la geometría en 3D.

#### ¿Qué debes explicar?
1. Esta fórmula es el **puente entre la geometría y la física**: para saber cuánta amplitud llega a cada sensor, primero necesitamos saber qué tan lejos está ese sensor de la fuente.
2. **Rᵢ** entra directamente en la fórmula de atenuación de la diapositiva anterior — sin Rᵢ no podemos calcular A_pred.
3. Las coordenadas del sensor **(xᵢ, yᵢ, zᵢ)** son datos conocidos (los colocamos nosotros al diseñar la red). Las coordenadas **(x, y, z)** de la fuente son las que el algoritmo va a estimar —son las incógnitas del problema inverso.
4. Recalcar que trabajamos en **ℝ³** (espacio tridimensional), porque los terremotos ocurren a profundidad — no solo en la superficie.

---

## PARTE 2 — Implementación y Resultados

---

### Diapositiva 18 — Incorporación de Ruido Gaussiano
**Archivo:** `secciones/Parte_2/16_Incorporación_ruido_gaussiano.tex`

#### ¿Qué hay en esta diapositiva?
La diapositiva explica **por qué y cómo se añade ruido a los datos simulados**. Está dividida en dos bloques:

**Bloque izquierdo — ¿Por qué añadir ruido?**
- Los instrumentos reales no son perfectos: tienen errores de medición.
- El medio geológico no es homogéneo: tiene irregularidades.
- Existen perturbaciones externas que afectan las lecturas.

**Bloque derecho — Modelado matemático:**
- Factor de variación: **5%**
- Desviación estándar por sensor: σᵢ = 0.05 · A_ideal,i
- El ruido se genera con distribución normal: εᵢ ~ N(0, σᵢ)
- Amplitud observada final: **A_obs,i = A_ideal,i + εᵢ**

#### ¿Qué debes explicar?
1. Las amplitudes ideales calculadas antes son perfectas en teoría, pero en la **realidad los sensores no miden perfectamente** —siempre hay algo de error.
2. Para simular esa realidad, se agrega **ruido gaussiano** (distribución normal con media cero): esto significa que el ruido puede subir o bajar el valor ideal, pero sin sesgo —no siempre sube ni siempre baja.
3. El **5% de variación** es moderado: suficiente para que el problema sea realista, pero no tan grande como para que el algoritmo falle.
4. La fórmula final **A_obs = A_ideal + ε** es lo que convierte una simulación perfecta en datos que se comportan como mediciones reales. Estos son los datos que le vamos a dar al problema inverso.

---

### Diapositiva 19 — Tabulación: Amplitudes Observadas (A_obs)
**Archivo:** `secciones/Parte_2/17_Operacion_Ruido_Gaussiano.tex`

#### ¿Qué hay en esta diapositiva?
Una **tabla completa con los 12 sensores**, mostrando:
- Distancia Rᵢ al sensor
- Amplitud ideal A_ideal
- Ruido εᵢ aplicado (al 5%)
- Amplitud observada final **A_obs** (en negrita)

Se destacan los valores del sensor S9 (el más cercano a la fuente) que presenta la mayor amplitud observada: **0.904624**. A la derecha se indica que estas amplitudes con ruido son el **conjunto de datos de entrada para el problema inverso**.

#### ¿Qué debes explicar?
1. Mostrar la tabla y señalar que ahora tenemos las **amplitudes "reales" (con ruido)** que simulan lo que medirían los sensores en un sismo real.
2. Resaltar a **S9**: tiene la menor distancia (1.84 km) y por tanto la mayor amplitud observada (≈ 0.90). Esto es coherente con la física —el sensor más cercano recibe más energía.
3. Estos datos son el **punto de partida del problema inverso**: el algoritmo Gauss-Newton va a recibir estas amplitudes y, a partir de ellas, deberá estimar dónde estuvo la fuente —sin saber las coordenadas reales.
4. Enfatizar que el ruido del 5% es pequeño pero hace que el problema sea más difícil de resolver —el algoritmo tiene que "filtrar" ese ruido para llegar a la solución correcta.

---

## PARTE 5 — Conclusiones y Defensa Final

---

### Diapositiva 39 — Resultados Finales: Validación del Modelo
**Archivo:** `secciones/Parte_5/33_conclusion_luis.tex`

#### ¿Qué hay en esta diapositiva?
La diapositiva presenta la **tabla de comparación entre la fuente real y la fuente estimada** por Gauss-Newton:

| Parámetro | Real | Estimado | Error |Δ| |
|-----------|------|----------|--------|
| x [km] | 1.2000 | 1.1995 | 0.0005 |
| y [km] | -0.8000 | -0.8012 | 0.0012 |
| z [km] | -1.1000 | -1.1024 | 0.0024 |
| A₀ | 10.0000 | 10.0142 | 0.0142 |

**Distancia posicional neta:** ‖Δm‖ ≈ 0.0027 km  
**Precisión:** > 99.7%

También se explica que la amplitud disminuye con la distancia y que las regiones de menor error coinciden con posiciones cercanas a la fuente real.

#### ¿Qué debes explicar?
1. **Leer la tabla** y señalar que la diferencia entre la posición real y la estimada es de solo **0.0027 km** — menos de 3 metros en un espacio de kilómetros. Eso es una precisión del 99.7%.
2. Recalcar que **A₀ también fue estimado** correctamente: el error es solo del 0.142% — prácticamente perfecto.
3. Explicar por qué hay algo de error (pequeño): el **ruido gaussiano del 5%** que se agregó en la simulación es la razón — sin ruido, la estimación sería exacta.
4. Conclusión: el modelo matemático **funciona** — puede localizar la fuente sísmica a partir solo de las amplitudes registradas por los sensores.

---

### Diapositiva 40 — El Mínimo: Significado Físico y Cálculo Multivariado
**Archivo:** `secciones/Parte_5/34_defensa_kevin_1.tex`

#### ¿Qué hay en esta diapositiva?
A la izquierda hay una **imagen 3D de la superficie de error E(x,y)** — se ve como un "valle" con un punto mínimo marcado en rojo. A la derecha se explica:

- **¿Qué significa el mínimo?** No es solo un número pequeño: es la **ubicación espacial que mejor explica físicamente** el comportamiento de la señal sísmica.
  
$$m^* = \arg\min_{m \in \mathbb{R}^4} E(m)$$

- **Conexión con Cálculo Multivariado:**
  - La función de error depende de 4 parámetros: E = E(x, y, z, A₀)
  - Gauss-Newton analiza y minimiza esa función iterativamente
  - Las funciones de varias variables permiten modelar fenómenos espaciales complejos

#### ¿Qué debes explicar?
1. Señalar la imagen: la **superficie de error es una función de varias variables** —tiene "montañas" donde el error es alto y un "valle" donde el error es mínimo. Ese valle es donde está la fuente.
2. **El mínimo no es solo matemático**: significa que en ese punto las amplitudes que predice el modelo coinciden mejor con las que midieron los sensores en la realidad.
3. Explicar la **conexión con Cálculo Multivariado**: estudiar E(x, y, z, A₀) es exactamente un problema de funciones de varias variables — la herramienta central del curso. Sin el cálculo multivariado, no podríamos analizar esta superficie.
4. El operador **arg min** significa "los valores de m que hacen que E sea mínima" — es la notación formal de "encontrar la posición donde el error es más pequeño".

---

### Diapositiva 41 — Optimización y Limitaciones del Modelo
**Archivo:** `secciones/Parte_5/35_defensa_kevin_2.tex`

#### ¿Qué hay en esta diapositiva?
Dos bloques bien diferenciados:

**¿Por qué fue importante optimizar?**
- Gauss-Newton identificó automáticamente la región del espacio ℝ⁴ donde el error era mínimo.
- Sin optimización, habría que evaluar manualmente infinitas combinaciones de (x, y, z, A₀).
- Convergió en solo **8 iteraciones** con precisión > 99.7%.
- Es el puente entre el modelo matemático y la solución física.
- Idea clave: *"Buscar el mínimo de E(x,y,z,A₀) equivale a encontrar la fuente sísmica."*

**Limitaciones del modelo:**
- **Medio homogéneo:** se asumió propagación uniforme, sin variaciones del terreno.
- **Sensibilidad al punto inicial:** Gauss-Newton necesita un buen punto de partida.
- **Sensibilidad al ruido:** el ruido en mediciones afecta la precisión.
- **Sensores limitados:** solo 12 estaciones restringen la resolución espacial.

#### ¿Qué debes explicar?
1. **Por qué Gauss-Newton es esencial**: sin un algoritmo de optimización, tendríamos que probar cada combinación posible de coordenadas — algo computacionalmente imposible. El algoritmo hace eso de forma inteligente en solo 8 pasos.
2. La **idea clave**: encontrar el mínimo de la función de error *es exactamente lo mismo* que localizar la fuente. El problema geofísico y el problema matemático son la misma cosa.
3. **Limitaciones honestas del modelo** — esta parte es importante para la defensa. Los profesores suelen preguntar sobre las limitaciones. Mencionar:
   - En la realidad, el suelo no es homogéneo (tiene capas, rocas distintas, etc.)
   - Si el punto de inicio del algoritmo es muy malo, puede converger a un mínimo falso
   - Con más sensores, la estimación sería más precisa

---

### Diapositiva 42 — Conclusión Final del Proyecto
**Archivo:** `secciones/Parte_5/36_cierre_final.tex`

#### ¿Qué hay en esta diapositiva?
La diapositiva de cierre tiene dos bloques y un resumen final:

**Mejoras Futuras:**
- Incorporar modelos físicos más complejos de propagación.
- Considerar medios no homogéneos (terreno realista).
- Aumentar la cantidad de sensores para mayor resolución espacial.
- Extender la estimación a parámetros adicionales del modelo sísmico.

**El Problema Inverso se Resolvió:**
El problema inverso pudo resolverse correctamente utilizando:
- Funciones multivariables E(x, y, z, A₀)
- Gauss-Newton — 8 iteraciones, precisión > 99.7%
- Análisis visual de la función de error
- Estimación simultánea de las 4 incógnitas

**Bloque final:** *"Este proyecto permitió integrar conceptos de cálculo multivariado, geometría espacial y optimización en un problema aplicado de localización sísmica."*

#### ¿Qué debes explicar?
1. **Cerrar el círculo**: recordar el objetivo del inicio —localizar una fuente sísmica— y confirmar que se logró con una precisión del 99.7%.
2. **Las herramientas que lo hicieron posible**: funciones de varias variables (para modelar), distancia euclidiana (para geometría), ruido gaussiano (para realismo) y Gauss-Newton (para optimización). Todo conectado.
3. **Mejoras futuras**: mostrar que el equipo entiende las limitaciones y sabe cómo evolucionaría el modelo en una aplicación real. Esto demuestra madurez técnica.
4. **Cierre formal**: agradecer y dejar abierta la sesión de preguntas.

---

## 📋 RESUMEN RÁPIDO DE DIAPOSITIVAS

| # | Título | Concepto clave | Duración estimada |
|---|--------|----------------|-------------------|
| 7 | Modelo de Atenuación Sísmica | Fórmula A_pred = A₀·e^(-R)/R | ~2 min |
| 8 | Distancia Euclidiana en ℝ³ | Fórmula Rᵢ = √((xᵢ-x)²+…) | ~1.5 min |
| 18 | Incorporación de Ruido Gaussiano | A_obs = A_ideal + ε, σ=5% | ~2 min |
| 19 | Tabulación: Amplitudes Observadas | Tabla completa 12 sensores con ruido | ~1.5 min |
| 39 | Resultados Finales: Validación | Comparativa real vs estimado, 99.7% | ~2 min |
| 40 | El Mínimo: Significado Físico | Superficie de error, arg min, cálculo multivariado | ~2.5 min |
| 41 | Optimización y Limitaciones | Por qué Gauss-Newton + limitaciones honestas | ~2 min |
| 42 | Conclusión Final | Cierre, mejoras futuras, agradecimiento | ~1.5 min |

**Total estimado: ~15 minutos**

---

## 💡 POSIBLES PREGUNTAS DE DEFENSA

**Sobre la fórmula de atenuación (diap. 7):**
> *¿Por qué se usa e^(-R) y no otra función de decaimiento?*  
> Porque el decaimiento exponencial modela bien la absorción de energía en medios continuos. La forma e^(-R)/R combina la absorción (exponencial) con la dispersión geométrica (1/R).

**Sobre el ruido gaussiano (diap. 18-19):**
> *¿Por qué distribución normal y no otro tipo de ruido?*  
> El ruido gaussiano (normal) es el más común en instrumentos de medición reales. Tiene media cero (no sesga los datos) y es matemáticamente conveniente para trabajar con mínimos cuadrados.

**Sobre el mínimo (diap. 40):**
> *¿Cómo saben que el mínimo que encontró Gauss-Newton es el global y no un mínimo local?*  
> La función de error en este problema tiene un mínimo global bien definido (verificado visualmente con los mapas de calor). Además, el resultado coincide con la fuente real simulada, lo que confirma que es el mínimo correcto.

**Sobre las limitaciones (diap. 41):**
> *¿Qué pasaría si el terreno no fuera homogéneo?*  
> La fórmula de atenuación cambiaría —la velocidad de propagación y la absorción variarían según la capa geológica. Sería necesario un modelo más complejo que considere la estructura interna del suelo.
