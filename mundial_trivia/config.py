# config.py
# Constantes del juego: colores, fuentes, puntajes y fases.
# Mundial Trivia Challenge - UTP 2026

# --- Ventana ---
ANCHO = 1024
ALTO = 600
TITULO = "Mundial Trivia Challenge"

# --- Reglas del juego ---
VIDAS_INICIALES = 3
PREGUNTAS_POR_FASE = 5

# --- Fases del torneo (tupla: no debe mutarse durante el juego) ---
FASES = (
    {"nombre": "Fase de Grupos",   "puntos": 10, "dificultad": "facil"},
    {"nombre": "Octavos de Final", "puntos": 15, "dificultad": "facil"},
    {"nombre": "Cuartos de Final", "puntos": 20, "dificultad": "medio"},
    {"nombre": "Semifinal",        "puntos": 30, "dificultad": "medio"},
    {"nombre": "Final",            "puntos": 50, "dificultad": "dificil"},
)

# --- Colores ---
COLOR_FONDO        = "#0f2557"   # azul noche
COLOR_FONDO_2      = "#1e3a8a"   # azul oscuro (degradado)
COLOR_CARD         = "#ffffff"   # card blanca de la pregunta
COLOR_TEXTO        = "#1f2937"   # gris muy oscuro (texto sobre card)
COLOR_TEXTO_CLARO  = "#ffffff"
COLOR_BOTON        = "#1e3a8a"   # azul oscuro
COLOR_BOTON_HOVER  = "#3b82f6"   # azul brillante
COLOR_ACIERTO      = "#22c55e"   # verde
COLOR_FALLO        = "#ef4444"   # rojo
COLOR_DORADO       = "#fbbf24"   # dorado (titulos, salon de la fama)

# --- Fuentes ---
FUENTE = "Segoe UI"
FUENTE_TITULO   = (FUENTE, 32, "bold")
FUENTE_SUBTITULO = (FUENTE, 18, "bold")
FUENTE_PREGUNTA = (FUENTE, 16, "bold")
FUENTE_OPCION   = (FUENTE, 13, "bold")
FUENTE_NORMAL   = (FUENTE, 12)
FUENTE_HUD      = (FUENTE, 14, "bold")

# --- Tiempos (ms) ---
PAUSA_FEEDBACK = 1200   # pausa tras responder antes de la siguiente pregunta

# --- Assets ---
RUTA_ASSETS = "assets"
TAM_IMAGEN = (260, 260)  # tamano al que se ajustan las imagenes de pregunta
