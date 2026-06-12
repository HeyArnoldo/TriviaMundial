# ⚽ Mundial Trivia Challenge

Juego de trivia de fútbol con estructura de torneo. 5 fases, 3 vidas, 25 preguntas, imágenes de jugadores y escudos.

**Proyecto Final · Programación de Computadoras · UTP 2026**

---

## Requisitos

- Python 3.8+
- Tkinter (viene incluido con Python en Windows)
- Pillow *(opcional — mejora la calidad de las imágenes)*

## Instalación

```bash
# 1. Clonar el repositorio
git clone https://github.com/tu-usuario/TriviaMundial.git
cd TriviaMundial

# 2. (Opcional) Instalar Pillow para mejor renderizado de imágenes
pip install pillow
```

> Sin Pillow el juego igual corre — las imágenes se muestran con el módulo estándar `tkinter.PhotoImage`.

## Ejecutar

```bash
python mundial_trivia/main.py
```

---

## Cómo se juega

| Fase | Puntos por acierto | Dificultad |
|---|---|---|
| Fase de Grupos | 10 pts | Fácil |
| Octavos de Final | 15 pts | Fácil |
| Cuartos de Final | 20 pts | Medio |
| Semifinal | 30 pts | Medio |
| Final | 50 pts | Difícil |

- **3 vidas** — no se recuperan entre fases.
- **5 preguntas por fase** — sin repetición entre fases.
- **Acierto** → suma puntos. **Fallo** → pierde una vida.
- **0 vidas** → Game Over con tu puntaje.
- **Superar las 5 fases** → Salón de la Fama 🏆

---

## Estructura del proyecto

```
mundial_trivia/
├── main.py          # Punto de entrada → ejecutar esto
├── config.py        # Constantes: colores, fuentes, fases, puntajes
├── preguntas.py     # Base de 50 preguntas (lista de dicts, opciones en tuplas)
├── juego.py         # Lógica pura del juego (sin GUI)
├── interfaz.py      # GUI completa en Tkinter (5 pantallas)
└── assets/
    ├── jugadores/   # Fotos de jugadores (PNG)
    ├── escudos/     # Logos de selecciones (PNG)
    └── goles/       # Fotos de protagonistas de goles históricos (PNG)
```

---

## Integrantes

| Nombre | Código |
|---|---|
| Mamani Aguilar, Luis Enrique | U23259985 |
| Cortez Benites, Eduardo Franco | U1421099 |
| Gallardo Villa, Paul Williams | U1614474 |
