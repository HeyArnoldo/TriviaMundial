"""Genera capturas reproducibles de las pantallas principales de la aplicación."""

import random
import sys
import time
import tkinter as tk
from pathlib import Path

from PIL import ImageGrab


RAIZ = Path(__file__).resolve().parents[1]
MODULOS = RAIZ / "mundial_trivia"
SALIDA = RAIZ / "docs" / "informe" / "figuras"
sys.path.insert(0, str(MODULOS))

import juego
from interfaz import App


def capturar(root, nombre):
    """Captura únicamente el área de contenido de la ventana Tkinter."""
    root.update()
    time.sleep(0.4)
    root.update()
    x = root.winfo_rootx()
    y = root.winfo_rooty()
    ancho = root.winfo_width()
    alto = root.winfo_height()
    ruta = SALIDA / nombre
    ImageGrab.grab((x, y, x + ancho, y + alto)).save(ruta)
    print(f"Captura creada: {ruta}")


def main():
    SALIDA.mkdir(parents=True, exist_ok=True)
    root = tk.Tk()
    root.geometry("1024x600+80+80")
    root.attributes("-topmost", True)
    app = App(root)

    capturar(root, "01_bienvenida.png")

    app.estado = juego.nuevo_estado("Equipo UTP")
    app.pantalla_intro_fase()
    capturar(root, "02_fase.png")

    fase = juego.fase_actual(app.estado)
    app.preguntas_fase = juego.seleccionar_preguntas(
        app.lista_trivia, fase["dificultad"], rng=random.Random(42))
    app.indice_pregunta = 0
    app.pantalla_pregunta()
    capturar(root, "03_pregunta.png")

    pregunta = app.preguntas_fase[0]
    respuesta_incorrecta = (pregunta["correcta"] + 1) % len(pregunta["opciones"])
    app.responder(respuesta_incorrecta)
    capturar(root, "04_retroalimentacion.png")
    if app._tarea_siguiente is not None:
        root.after_cancel(app._tarea_siguiente)
        app._tarea_siguiente = None

    app.estado["vidas"] = 0
    juego.guardar_en_ranking(app.estado)
    app.pantalla_final()
    capturar(root, "05_resultado.png")

    root.destroy()


if __name__ == "__main__":
    main()
