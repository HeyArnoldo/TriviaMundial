# Mundial Trivia Challenge

Aplicación de escritorio desarrollada en Python y Tkinter. Presenta una trivia de
fútbol con 50 preguntas, cinco fases de dificultad progresiva, tres vidas,
analítica de resultados y simulaciones reproducibles.

## Inicio rápido

Requisitos:

- Python 3.11 o superior.
- Tkinter, incluido normalmente con Python en Windows.

```bash
python -m venv venv
venv\Scripts\activate
python -m pip install -r requirements.txt
python mundial_trivia/main.py
```

En macOS o Linux, activa el entorno con `source venv/bin/activate`. Si Tkinter no
está incluido en tu distribución, instálalo desde el gestor de paquetes del
sistema operativo.

## Funcionalidades

- Banco validado de 50 preguntas sobre jugadores, selecciones, goles y datos.
- Cinco fases con puntajes y dificultades progresivas.
- Interfaz gráfica con retroalimentación inmediata y recursos visuales.
- Ranking de la sesión y opción para jugar nuevamente.
- Registro de respuestas, puntaje, vidas y tiempo empleado.
- Procesamiento de resultados mediante matrices NumPy.
- Clasificación automática del rendimiento.
- Exportación de archivos CSV, reportes de texto y gráficos con Matplotlib.
- Simulación de partidas con una semilla configurable.

## Reglas

| Fase | Puntos por acierto | Dificultad |
|---|---:|---|
| Fase de Grupos | 10 | Fácil |
| Octavos de Final | 15 | Fácil |
| Cuartos de Final | 20 | Media |
| Semifinal | 30 | Media |
| Final | 50 | Difícil |

Cada fase contiene cinco preguntas. Una respuesta incorrecta elimina una vida;
la partida termina al perder las tres vidas o al completar la final.

## Analítica

Al finalizar una partida, el programa crea `resultados/ultima_partida/` con:

- El historial de respuestas en CSV.
- La matriz numérica procesada con NumPy.
- Un resumen textual del rendimiento.
- Cuatro gráficos sobre aciertos, fases, categorías y evolución del puntaje.

Estos archivos son resultados de ejecución y no forman parte del código fuente
versionado.

## Simulación

Ejecuta partidas automáticas indicando la cantidad, la semilla y, opcionalmente,
el directorio de salida:

```bash
python mundial_trivia/simulador.py --partidas 10 --semilla 42
python mundial_trivia/simulador.py --partidas 100 --semilla 7 --salida resultados/simulacion
```

Usar la misma configuración produce los mismos puntajes, lo que permite repetir
y comparar experimentos.

## Pruebas

```bash
python -m unittest discover -s tests -v
```

Las pruebas cubren la lógica del juego, el procesamiento analítico, la generación
de archivos y la reproducibilidad de las simulaciones.

## Estructura

```text
mundial_trivia/
|-- main.py          # Punto de entrada
|-- config.py        # Reglas y configuración visual
|-- preguntas.py     # Banco de preguntas
|-- juego.py         # Lógica del dominio sin interfaz gráfica
|-- interfaz.py      # Interfaz de escritorio con Tkinter
|-- analitica.py     # Procesamiento NumPy y gráficos
|-- simulador.py     # Simulación reproducible de partidas
`-- assets/          # Imágenes utilizadas por las preguntas

tests/
|-- test_juego.py
|-- test_analitica.py
`-- test_simulador.py
```
