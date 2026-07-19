"""Procesamiento NumPy, clasificación y visualización de resultados."""

import csv
from pathlib import Path

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt


COLUMNAS_MATRIZ = (
    "numero",
    "pregunta_id",
    "fase_indice",
    "categoria_codigo",
    "dificultad_codigo",
    "acierto",
    "puntos_obtenidos",
    "puntaje_acumulado",
    "vidas_restantes",
    "tiempo_respuesta",
)

CODIGOS_CATEGORIA = {
    "jugadores": 1,
    "escudos": 2,
    "goles": 3,
    "datos": 4,
}

CODIGOS_DIFICULTAD = {
    "facil": 1,
    "medio": 2,
    "dificil": 3,
}

DIRECTORIO_RESULTADOS = Path(__file__).resolve().parent.parent / "resultados"


def crear_matriz(historial):
    """Convierte el historial de diccionarios en una matriz numérica."""
    if not historial:
        return np.empty((0, len(COLUMNAS_MATRIZ)), dtype=float)

    filas = []
    for registro in historial:
        try:
            categoria = CODIGOS_CATEGORIA[registro["categoria"]]
            dificultad = CODIGOS_DIFICULTAD[registro["dificultad"]]
        except KeyError as error:
            raise ValueError(f"Valor no reconocido en el historial: {error.args[0]}") from error

        filas.append((
            registro["numero"],
            registro["pregunta_id"],
            registro["fase_indice"],
            categoria,
            dificultad,
            int(registro["acierto"]),
            registro["puntos_obtenidos"],
            registro["puntaje_acumulado"],
            registro["vidas_restantes"],
            registro["tiempo_respuesta"],
        ))
    return np.asarray(filas, dtype=float)


def clasificar_desempeno(porcentaje):
    """Clasifica el rendimiento de acuerdo con el porcentaje de aciertos."""
    if not 0 <= porcentaje <= 100:
        raise ValueError("El porcentaje debe estar entre 0 y 100.")
    if porcentaje >= 80:
        return "Excelente"
    if porcentaje >= 60:
        return "Bueno"
    if porcentaje >= 40:
        return "En proceso"
    return "Necesita refuerzo"


def _porcentaje_por_campo(historial, campo):
    """Agrupa los aciertos con NumPy conservando el orden de aparición."""
    resultados = {}
    valores = np.asarray([int(registro["acierto"]) for registro in historial], dtype=float)
    etiquetas = [registro[campo] for registro in historial]
    for etiqueta in dict.fromkeys(etiquetas):
        mascara = np.asarray([valor == etiqueta for valor in etiquetas], dtype=bool)
        resultados[etiqueta] = float(np.mean(valores[mascara]) * 100)
    return resultados


def procesar_historial(historial):
    """Calcula indicadores estadísticos a partir del historial registrado."""
    matriz = crear_matriz(historial)
    if matriz.size == 0:
        return {
            "total_respuestas": 0,
            "aciertos": 0,
            "errores": 0,
            "porcentaje_aciertos": 0.0,
            "puntaje_total": 0,
            "tiempo_promedio": 0.0,
            "desviacion_tiempo": 0.0,
            "clasificacion": "Sin datos",
            "por_fase": {},
            "por_categoria": {},
        }

    aciertos = int(np.sum(matriz[:, 5]))
    total = matriz.shape[0]
    porcentaje = float(np.mean(matriz[:, 5]) * 100)
    return {
        "total_respuestas": total,
        "aciertos": aciertos,
        "errores": total - aciertos,
        "porcentaje_aciertos": porcentaje,
        "puntaje_total": int(matriz[-1, 7]),
        "tiempo_promedio": float(np.mean(matriz[:, 9])),
        "desviacion_tiempo": float(np.std(matriz[:, 9])),
        "clasificacion": clasificar_desempeno(porcentaje),
        "por_fase": _porcentaje_por_campo(historial, "fase"),
        "por_categoria": _porcentaje_por_campo(historial, "categoria"),
    }


def generar_graficos(historial, directorio):
    """Genera cuatro gráficos PNG y devuelve sus rutas."""
    if not historial:
        return []

    directorio = Path(directorio)
    directorio.mkdir(parents=True, exist_ok=True)
    resumen = procesar_historial(historial)
    matriz = crear_matriz(historial)
    rutas = []

    plt.style.use("seaborn-v0_8-whitegrid")

    figura, eje = plt.subplots(figsize=(7, 4))
    eje.bar(
        ("Aciertos", "Errores"),
        (resumen["aciertos"], resumen["errores"]),
        color=("#22c55e", "#ef4444"),
    )
    eje.set_title("Resultado general de la partida")
    eje.set_ylabel("Cantidad de respuestas")
    rutas.append(_guardar_figura(figura, directorio / "aciertos_errores.png"))

    figura, eje = plt.subplots(figsize=(8, 4))
    eje.bar(resumen["por_fase"].keys(), resumen["por_fase"].values(), color="#2563eb")
    eje.set_title("Porcentaje de aciertos por fase")
    eje.set_ylabel("Aciertos (%)")
    eje.set_ylim(0, 100)
    eje.tick_params(axis="x", rotation=20)
    rutas.append(_guardar_figura(figura, directorio / "rendimiento_fase.png"))

    figura, eje = plt.subplots(figsize=(7, 4))
    eje.bar(
        [categoria.title() for categoria in resumen["por_categoria"]],
        resumen["por_categoria"].values(),
        color="#f59e0b",
    )
    eje.set_title("Porcentaje de aciertos por categoría")
    eje.set_ylabel("Aciertos (%)")
    eje.set_ylim(0, 100)
    rutas.append(_guardar_figura(figura, directorio / "rendimiento_categoria.png"))

    figura, eje = plt.subplots(figsize=(8, 4))
    eje.plot(matriz[:, 0], matriz[:, 7], marker="o", color="#1e3a8a")
    eje.set_title("Evolución del puntaje")
    eje.set_xlabel("Número de respuesta")
    eje.set_ylabel("Puntaje acumulado")
    eje.set_xticks(matriz[:, 0].astype(int))
    rutas.append(_guardar_figura(figura, directorio / "evolucion_puntaje.png"))

    return rutas


def _guardar_figura(figura, ruta):
    figura.tight_layout()
    figura.savefig(ruta, dpi=160, bbox_inches="tight")
    plt.close(figura)
    return ruta


def generar_reporte_partida(estado, directorio=None):
    """Exporta historial, matriz, resumen textual y gráficos de una partida."""
    directorio = Path(directorio or DIRECTORIO_RESULTADOS / "ultima_partida")
    directorio.mkdir(parents=True, exist_ok=True)
    historial = estado["historial_respuestas"]
    resumen = procesar_historial(historial)
    matriz = crear_matriz(historial)

    ruta_historial = directorio / "historial_respuestas.csv"
    if historial:
        with ruta_historial.open("w", newline="", encoding="utf-8-sig") as archivo:
            escritor = csv.DictWriter(archivo, fieldnames=historial[0].keys())
            escritor.writeheader()
            escritor.writerows(historial)
    else:
        ruta_historial.write_text("", encoding="utf-8")

    ruta_matriz = directorio / "matriz_numpy.csv"
    np.savetxt(
        ruta_matriz,
        matriz,
        delimiter=",",
        header=",".join(COLUMNAS_MATRIZ),
        comments="",
        fmt="%.2f",
    )

    ruta_reporte = directorio / "reporte_final.txt"
    lineas = (
        "REPORTE FINAL - MUNDIAL TRIVIA CHALLENGE",
        f"Jugador: {estado['jugador']}",
        f"Puntaje final: {estado['puntaje']}",
        f"Respuestas: {resumen['total_respuestas']}",
        f"Aciertos: {resumen['aciertos']}",
        f"Errores: {resumen['errores']}",
        f"Porcentaje de aciertos: {resumen['porcentaje_aciertos']:.2f}%",
        f"Tiempo promedio: {resumen['tiempo_promedio']:.2f} segundos",
        f"Clasificación: {resumen['clasificacion']}",
        f"Resultado del juego: {estado.get('resultado', 'finalizado')}",
    )
    ruta_reporte.write_text("\n".join(lineas) + "\n", encoding="utf-8")

    rutas_graficos = generar_graficos(historial, directorio / "graficos")
    return {
        "historial": ruta_historial,
        "matriz": ruta_matriz,
        "reporte": ruta_reporte,
        "graficos": rutas_graficos,
    }
