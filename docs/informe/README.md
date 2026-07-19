# Generar el informe

El PDF y el archivo Word se construyen en contenedores. No hace falta instalar LaTeX ni Pandoc en Windows.

## Ruta rápida

1. Iniciar Docker Desktop.
2. Instalar las herramientas de documentación con `pip install -r requirements-documentacion.txt`.
3. Ejecutar `python mundial_trivia/simulador.py --partidas 10 --semilla 42`.
4. Ejecutar `python scripts/generar_evidencias.py`.
5. Ejecutar `python scripts/generar_referencia_word.py`.
6. Ejecutar `python scripts/generar_presentacion.py`.
7. Ejecutar `docker compose run --rm latex`.
8. Ejecutar `docker compose run --rm word`.
9. Revisar los documentos creados en `entregables/`.

## Imágenes

El informe busca las capturas en `docs/informe/figuras/` y el histograma en `resultados/simulacion/`. Si falta una captura, el PDF muestra un recuadro de evidencia pendiente en lugar de interrumpir la compilación.

## Índice de Word

El archivo Word incluye un índice automático. Microsoft Word lo actualiza al abrir el documento; si solicita confirmación, selecciona **Sí**. También puedes actualizarlo manualmente con clic derecho sobre el índice y **Actualizar campos**.

## Contenedores

| Servicio | Imagen | Salida |
|---|---|---|
| `latex` | `texlive/texlive:TL2025-historic` | `Informe_Trivia_Mundial.pdf` |
| `word` | Imagen local basada en `pandoc/latex:3.10.0.0` | `Informe_Trivia_Mundial.docx` |

Las imágenes están fijadas por versión para que el resultado sea reproducible.
