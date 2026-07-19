# Guion de exposición y funcionamiento

Duración objetivo: 8 a 10 minutos. Grabar la presentación y la aplicación en una sola toma o unir ambos segmentos durante la edición.

## Distribución

| Tiempo | Responsable | Contenido |
|---|---|---|
| 0:00-0:40 | Luis | Presentación del equipo, problema y objetivo general. |
| 0:40-2:10 | Eduardo | Reglas, fases, entradas, salidas y estructuras de datos. |
| 2:10-3:40 | Paul | Arquitectura modular, interfaz y captura de respuestas. |
| 3:40-5:20 | Luis | Matriz NumPy, indicadores y clasificación. |
| 5:20-6:30 | Eduardo | Gráficos, simulación con semilla y resultados. |
| 6:30-8:15 | Paul | Demostración del juego y archivos generados. |
| 8:15-9:10 | Equipo | Pruebas, conclusiones y cierre. |

## Demostración

1. Ejecutar `python mundial_trivia/main.py`.
2. Mostrar la validación con un nombre inválido.
3. Ingresar un nombre correcto y comenzar una fase.
4. Responder una pregunta correctamente y otra incorrectamente.
5. Mostrar el cambio de puntaje y vidas.
6. Abrir `resultados/ultima_partida/` y enseñar el CSV, la matriz, el reporte y los gráficos.
7. Ejecutar `python mundial_trivia/simulador.py --partidas 10 --semilla 42`.
8. Mostrar que la simulación vuelve a producir los mismos resultados.
9. Ejecutar `python -m unittest discover -s tests -v` y enseñar las pruebas superadas.

## Evidencia final

- La grabación debe mostrar los rostros o voces de los tres integrantes según las indicaciones del curso.
- Evitar notificaciones, ventanas personales o credenciales visibles.
- Verificar audio, resolución y legibilidad antes de entregar.
