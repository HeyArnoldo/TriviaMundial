# juego.py
# Logica del juego: funciones puras, SIN tkinter.
# Mundial Trivia Challenge - UTP 2026

import random

from config import FASES, VIDAS_INICIALES, PREGUNTAS_POR_FASE
from preguntas import cargar_preguntas


def nuevo_estado(nombre_jugador):
    """Crea el estado inicial del juego para un jugador."""
    return {
        "jugador": nombre_jugador,
        "puntaje": 0,
        "vidas": VIDAS_INICIALES,
        "fase_actual": 0,                # indice dentro de FASES
        "preguntas_jugadas": [],         # ids ya usados, para no repetir
        "ranking_sesion": [],            # tuplas (nombre, puntaje) de la sesion
    }


def seleccionar_preguntas(lista, dificultad, n=PREGUNTAS_POR_FASE, excluir=None):
    """Filtra preguntas por dificultad (excluyendo ids ya jugados)
    y devuelve n preguntas aleatorias sin repetir."""
    if excluir is None:
        excluir = []
    disponibles = [p for p in lista
                   if p["dificultad"] == dificultad and p["id"] not in excluir]
    # Si no alcanzan de esa dificultad, completar con cualquier otra no jugada
    if len(disponibles) < n:
        extras = [p for p in lista
                  if p["id"] not in excluir and p not in disponibles]
        disponibles += extras
    return random.sample(disponibles, min(n, len(disponibles)))


def validar_respuesta(pregunta, indice_elegido):
    """True si el indice elegido es la opcion correcta."""
    return indice_elegido == pregunta["correcta"]


def actualizar_puntaje(estado, acierto, puntos_fase):
    """Suma puntos si acerto, resta una vida si fallo. Muta el estado."""
    if acierto:
        estado["puntaje"] += puntos_fase
    else:
        estado["vidas"] -= 1


def registrar_pregunta(estado, pregunta):
    """Marca una pregunta como jugada para no repetirla."""
    estado["preguntas_jugadas"].append(pregunta["id"])


def fase_terminada(estado, respondidas):
    """True si ya respondio todas las preguntas de la fase o se quedo sin vidas."""
    return respondidas >= PREGUNTAS_POR_FASE or estado["vidas"] <= 0


def juego_terminado(estado):
    """True si se quedo sin vidas o completo todas las fases."""
    return estado["vidas"] <= 0 or estado["fase_actual"] >= len(FASES)


def avanzar_fase(estado):
    """Pasa a la siguiente fase del torneo."""
    estado["fase_actual"] += 1


def fase_actual(estado):
    """Devuelve el dict de la fase actual (nombre, puntos, dificultad)."""
    return FASES[estado["fase_actual"]]


def clasificar_resultado(estado):
    """Clasifica el final del juego:
    - 'salon_fama': completo las 5 fases sin perder las vidas
    - 'derrota':    se quedo sin vidas
    """
    if estado["vidas"] > 0 and estado["fase_actual"] >= len(FASES):
        return "salon_fama"
    elif estado["vidas"] <= 0:
        return "derrota"
    else:
        return "en_juego"


def guardar_en_ranking(estado):
    """Agrega (nombre, puntaje) al ranking de la sesion, ordenado de mayor a menor."""
    estado["ranking_sesion"].append((estado["jugador"], estado["puntaje"]))
    estado["ranking_sesion"].sort(key=lambda t: t[1], reverse=True)


def reiniciar_para_nueva_partida(estado, nombre_jugador):
    """Reinicia el estado conservando el ranking de la sesion."""
    ranking = estado["ranking_sesion"]
    nuevo = nuevo_estado(nombre_jugador)
    nuevo["ranking_sesion"] = ranking
    return nuevo


# --- Prueba rapida por consola (sin GUI) ---
if __name__ == "__main__":
    lista = cargar_preguntas()
    print(f"Total de preguntas: {len(lista)}")

    estado = nuevo_estado("Tester")
    while not juego_terminado(estado):
        fase = fase_actual(estado)
        preguntas = seleccionar_preguntas(
            lista, fase["dificultad"], excluir=estado["preguntas_jugadas"])
        print(f"\n== {fase['nombre']} ({len(preguntas)} preguntas) ==")
        respondidas = 0
        for p in preguntas:
            registrar_pregunta(estado, p)
            acierto = random.choice([True, True, False])  # simula respuestas
            actualizar_puntaje(estado, acierto, fase["puntos"])
            respondidas += 1
            print(f"  P{p['id']}: {'OK' if acierto else 'X'} "
                  f"(vidas={estado['vidas']}, puntaje={estado['puntaje']})")
            if fase_terminada(estado, respondidas):
                break
        if estado["vidas"] > 0:
            avanzar_fase(estado)

    guardar_en_ranking(estado)
    print(f"\nResultado: {clasificar_resultado(estado)}")
    print(f"Ranking: {estado['ranking_sesion']}")
