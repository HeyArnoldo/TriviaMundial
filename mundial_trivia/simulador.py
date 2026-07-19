"""Simulación reproducible de partidas de Mundial Trivia Challenge."""

import argparse
import csv
import random
from pathlib import Path

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt

import analitica
import juego
from preguntas import cargar_preguntas


PROBABILIDAD_ACIERTO = {
    "facil": 0.80,
    "medio": 0.60,
    "dificil": 0.40,
}


def _codigo_alfabetico(numero):
    """Convierte 1, 2, ..., 27 en A, B, ..., AA para nombres válidos."""
    codigo = ""
    while numero > 0:
        numero, resto = divmod(numero - 1, 26)
        codigo = chr(65 + resto) + codigo
    return codigo


def simular_partida(numero, rng, preguntas=None):
    """Ejecuta una partida automática usando probabilidades por dificultad."""
    preguntas = preguntas or cargar_preguntas()
    estado = juego.nuevo_estado(f"Simulado {_codigo_alfabetico(numero)}")

    while not juego.juego_terminado(estado):
        fase = juego.fase_actual(estado)
        preguntas_fase = juego.seleccionar_preguntas(
            preguntas,
            fase["dificultad"],
            excluir=estado["preguntas_jugadas"],
            rng=rng,
        )
        respondidas = 0
        for pregunta in preguntas_fase:
            acierto = rng.random() < PROBABILIDAD_ACIERTO[pregunta["dificultad"]]
            tiempo_respuesta = rng.uniform(2.0, 15.0)
            juego.actualizar_puntaje(estado, acierto, fase["puntos"])
            juego.registrar_respuesta(
                estado, pregunta, fase, acierto, tiempo_respuesta)
            respondidas += 1
            if juego.fase_terminada(estado, respondidas):
                break
        if estado["vidas"] > 0:
            juego.avanzar_fase(estado)

    estado["resultado"] = juego.clasificar_resultado(estado)
    return estado


def simular_partidas(cantidad=100, semilla=42):
    """Ejecuta varias partidas con una semilla para resultados repetibles."""
    if not isinstance(cantidad, int) or cantidad <= 0:
        raise ValueError("La cantidad de partidas debe ser un entero positivo.")
    rng = random.Random(semilla)
    preguntas = cargar_preguntas()
    juego.validar_banco_preguntas(preguntas)
    return [simular_partida(numero, rng, preguntas) for numero in range(1, cantidad + 1)]


def crear_matriz_simulacion(estados):
    """Crea una matriz: partida, puntaje, vidas, respuestas, aciertos y victoria."""
    filas = []
    for numero, estado in enumerate(estados, start=1):
        resumen = analitica.procesar_historial(estado["historial_respuestas"])
        filas.append((
            numero,
            estado["puntaje"],
            estado["vidas"],
            resumen["total_respuestas"],
            resumen["porcentaje_aciertos"],
            int(estado["resultado"] == "salon_fama"),
        ))
    return np.asarray(filas, dtype=float)


def exportar_simulacion(estados, directorio):
    """Guarda la matriz, el resumen CSV y gráficos de la simulación."""
    directorio = Path(directorio)
    directorio.mkdir(parents=True, exist_ok=True)
    matriz = crear_matriz_simulacion(estados)

    ruta_matriz = directorio / "matriz_simulacion.csv"
    np.savetxt(
        ruta_matriz,
        matriz,
        delimiter=",",
        header="partida,puntaje,vidas,respuestas,porcentaje_aciertos,victoria",
        comments="",
        fmt="%.2f",
    )

    ruta_resumen = directorio / "resumen_simulacion.csv"
    with ruta_resumen.open("w", newline="", encoding="utf-8-sig") as archivo:
        campos = (
            "partida", "jugador", "puntaje", "vidas", "respuestas",
            "porcentaje_aciertos", "clasificacion", "resultado",
        )
        escritor = csv.DictWriter(archivo, fieldnames=campos)
        escritor.writeheader()
        for numero, estado in enumerate(estados, start=1):
            resumen = analitica.procesar_historial(estado["historial_respuestas"])
            escritor.writerow({
                "partida": numero,
                "jugador": estado["jugador"],
                "puntaje": estado["puntaje"],
                "vidas": estado["vidas"],
                "respuestas": resumen["total_respuestas"],
                "porcentaje_aciertos": f"{resumen['porcentaje_aciertos']:.2f}",
                "clasificacion": resumen["clasificacion"],
                "resultado": estado["resultado"],
            })

    ruta_grafico = directorio / "puntajes_simulados.png"
    figura, eje = plt.subplots(figsize=(8, 4))
    eje.hist(matriz[:, 1], bins=min(10, len(estados)), color="#2563eb", edgecolor="white")
    eje.set_title("Distribución de puntajes simulados")
    eje.set_xlabel("Puntaje")
    eje.set_ylabel("Cantidad de partidas")
    figura.tight_layout()
    figura.savefig(ruta_grafico, dpi=160, bbox_inches="tight")
    plt.close(figura)

    ruta_reporte = directorio / "reporte_simulacion.txt"
    victorias = int(np.sum(matriz[:, 5]))
    lineas = (
        "SIMULACIÓN - MUNDIAL TRIVIA CHALLENGE",
        f"Partidas ejecutadas: {len(estados)}",
        f"Puntaje promedio: {np.mean(matriz[:, 1]):.2f}",
        f"Puntaje máximo: {np.max(matriz[:, 1]):.0f}",
        f"Puntaje mínimo: {np.min(matriz[:, 1]):.0f}",
        f"Desviación estándar: {np.std(matriz[:, 1]):.2f}",
        f"Victorias: {victorias}",
        f"Derrotas: {len(estados) - victorias}",
    )
    ruta_reporte.write_text("\n".join(lineas) + "\n", encoding="utf-8")
    return (ruta_matriz, ruta_resumen, ruta_grafico, ruta_reporte)


def main():
    parser = argparse.ArgumentParser(description="Simula partidas de Mundial Trivia Challenge")
    parser.add_argument("--partidas", type=int, default=100)
    parser.add_argument("--semilla", type=int, default=42)
    parser.add_argument("--salida", default="resultados/simulacion")
    argumentos = parser.parse_args()

    estados = simular_partidas(argumentos.partidas, argumentos.semilla)
    rutas = exportar_simulacion(estados, argumentos.salida)
    print(f"Simulación completada: {len(estados)} partidas")
    for ruta in rutas:
        print(f"- {ruta}")


if __name__ == "__main__":
    main()
