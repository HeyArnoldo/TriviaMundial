# 🏆 Mundial Trivia Challenge — Plan de Proyecto

> Proyecto Final · Programación de Computadoras (100000I42M) · UTP · 2026 Ciclo 1 Marzo

**Integrantes:**
- Mamani Aguilar, Luis Enrique — U23259985
- Cortez Benites, Eduardo Franco — U1421099
- Gallardo Villa, Paul Williams — U1614474

---

## 1. Concepto del juego

El jugador escribe su nombre y avanza por **6 fases tipo torneo**, respondiendo trivia con imágenes:

**Fase de Grupos → Octavos → Cuartos → Semifinal → Final → Salón de la Fama**

- 3 vidas (corazones), no se recargan entre fases.
- Cada fase = 5 preguntas aleatorias (sin repetir entre fases).
- Acierto: suma puntos (más puntos en fases avanzadas). Fallo: −1 vida.
- Si pierde las 3 vidas → Game Over con su puntaje final.
- Si supera las 5 fases → desbloquea el **Salón de la Fama**.

Total: 30 preguntas jugadas de una base de **50+**.

**Decisiones clave acordadas:**
- 4 opciones por pregunta (A/B/C/D)
- Imágenes en carpeta local `/assets`
- Tkinter pulido (canvas, fondos, hover states)
- Estructura de torneo con varios niveles
- Sin persistencia (solo en memoria durante la sesión)
- Pantalla de bienvenida con input para el nombre del jugador

---

## 2. Estructura de archivos

```
mundial_trivia/
├── main.py                  # punto de entrada, lanza la app
├── juego.py                 # lógica del juego (funciones puras)
├── interfaz.py              # toda la GUI tkinter (pantallas)
├── preguntas.py             # base de 50 preguntas como lista de dicts
├── config.py                # constantes: colores, fuentes, puntajes, fases
└── assets/
    ├── jugadores/           # neymar.png, messi.png, mbappe.png...
    ├── escudos/             # brasil.png, argentina.png...
    ├── goles/               # gol_maradona_86.png...
    └── ui/                  # fondo_cancha.png, corazon.png, estrella.png
```

**Por qué separar así:** el sílabo de la Unidad 2 (semana 8) pide explícitamente *"Diseño modular de programas… Definición, invocación y reutilización de funciones"*. Tener módulos separados es exactamente eso.

---

## 3. Estructuras de datos (mapeo al sílabo)

### Una pregunta = diccionario

Cubre Unidad 2, semana 9: diccionarios.

```python
{
    "id": 1,
    "categoria": "jugadores",        # jugadores | escudos | goles | datos
    "dificultad": "facil",           # facil | medio | dificil
    "pregunta": "¿Quién es el mejor jugador de Brasil?",
    "imagen": "assets/jugadores/vinicius.png",
    "opciones": ("Neymar Jr.", "Vinícius Jr.", "Raphinha", "Endrick"),  # TUPLA → inmutable
    "correcta": 1                    # índice de la opción correcta
}
```

**Por qué tupla en `opciones`:** las opciones no deben mutarse durante el juego → tupla. Esto da puntos con el profe porque usa **tupla con propósito real** (no decorativa).

**Lista de todas las preguntas** = `lista_trivia` (lista de diccionarios → exactamente lo que pide el brief).

### Estado del juego = diccionario

En memoria, sin persistencia.

```python
estado = {
    "jugador": "Luis Enrique",
    "puntaje": 0,
    "vidas": 3,
    "fase_actual": 0,                # índice de FASES
    "preguntas_jugadas": [],         # ids ya usados, para no repetir
    "ranking_sesion": []             # tuplas (nombre, puntaje) de la sesión
}
```

### Configuración de fases

En `config.py`:

```python
FASES = (
    {"nombre": "Fase de Grupos",  "puntos": 10, "dificultad": "facil"},
    {"nombre": "Octavos de Final","puntos": 15, "dificultad": "facil"},
    {"nombre": "Cuartos de Final","puntos": 20, "dificultad": "medio"},
    {"nombre": "Semifinal",       "puntos": 30, "dificultad": "medio"},
    {"nombre": "Final",           "puntos": 50, "dificultad": "dificil"},
)
```

---

## 4. Lógica del juego — funciones clave

Todas en `juego.py`, sin tkinter dentro (separación clara):

| Función | Para qué | Concepto del sílabo |
|---|---|---|
| `cargar_preguntas()` | Devuelve la lista de 50 dicts | listas + diccionarios |
| `seleccionar_preguntas(lista, dificultad, n, excluir)` | Filtra por dificultad y devuelve 5 aleatorias | `random.sample`, list comprehension |
| `validar_respuesta(pregunta, indice_elegido)` | Devuelve `True/False` | `if/else` |
| `actualizar_puntaje(estado, acierto, puntos_fase)` | Suma puntos o resta vida | mutación de dict |
| `fase_terminada(estado, preguntas_fase)` | `True` si acabó las 5 o se quedó sin vidas | lógica `and`/`or` |
| `juego_terminado(estado)` | `True` si vidas == 0 **or** completó todas las fases | lógica `and`/`or` |
| `clasificar_resultado(estado)` | Devuelve `"salon_fama"`, `"victoria"`, `"derrota"` | `if/elif/else` |

### Bucle principal conceptual

En realidad lo maneja tkinter por eventos, pero la lógica es esta:

```python
while estado["vidas"] > 0 and estado["fase_actual"] < len(FASES):
    preguntas_fase = seleccionar_preguntas(...)
    for pregunta in preguntas_fase:           # for de Unidad 2
        mostrar_pregunta(pregunta)
        # ... usuario responde ...
        if validar_respuesta(...):            # if/elif/else
            estado["puntaje"] += puntos
        else:
            estado["vidas"] -= 1
            if estado["vidas"] == 0:
                break
    estado["fase_actual"] += 1
```

Cubre: `while`, `for`, `if/elif/else`, `and`, `or`, `break` (Unidad 2, semana 6: "Sentencias de interrupción").

---

## 5. Interfaz (tkinter pulido)

5 pantallas, cada una en una función que limpia el root y dibuja:

1. **Bienvenida** → fondo cancha, título "MUNDIAL TRIVIA CHALLENGE", `Entry` para nombre, botón "JUGAR".
2. **Intro de fase** → "🏆 OCTAVOS DE FINAL — Vidas: ❤️❤️❤️ — Puntaje: 25" + botón "Comenzar".
3. **Pregunta** (la principal, tipo el mockup de referencia):
   - Header: puntaje + vidas (con ⭐ y ❤️).
   - Card central blanca con la pregunta arriba.
   - Imagen grande (cargada con `PIL.Image` + `ImageTk.PhotoImage`).
   - 4 botones A/B/C/D con hover (cambio de color al pasar el mouse).
   - Feedback visual: verde si acierta, rojo si falla, pausa de 1s con `root.after()`, luego siguiente pregunta.
4. **Resumen de fase** → "¡Pasaste a Cuartos!" o "Game Over".
5. **Salón de la Fama** → confeti, puntaje final, ranking de la sesión.

### Estética

- Fondo: azul degradado con cancha de fútbol sutil (`Canvas` con `create_image`).
- Botones: azul oscuro `#1e3a8a`, hover azul `#3b82f6`, verde acierto `#22c55e`, rojo fallo `#ef4444`.
- Fuente: `Montserrat` o `Segoe UI Bold`.
- Tamaño ventana fijo: 1024×600.

---

## 6. Las 50 preguntas — distribución sugerida

Para que la base sea variada y cubra el tema "Mundial":

| Categoría | Cantidad | Ejemplos |
|---|---|---|
| Identificar jugador por foto | 20 | Messi, Mbappé, Neymar, Vinícius, Haaland, Pedri… |
| Identificar escudo de selección | 10 | Brasil, Argentina, Francia, Alemania, Croacia… |
| Identificar gol histórico | 8 | Maradona vs Inglaterra '86, Iniesta 2010, Messi 2022… |
| Datos del Mundial (texto, sin imagen obligatoria) | 12 | "¿Quién ganó el Mundial 2022?", "¿Sede del Mundial 2026?"… |

**Distribución por dificultad:** 20 fáciles + 20 medias + 10 difíciles.

---

## 7. Mapeo al sílabo (para defender el proyecto)

| Concepto del sílabo | Dónde lo aplicas |
|---|---|
| Variables y tipos (int, str, bool) | puntaje, vidas, nombre, acierto |
| Operadores de comparación + lógicos (`and`, `or`) | `vidas > 0 and fase < 5` |
| `if / elif / else` | validar respuesta, clasificar resultado final |
| `for` | recorrer 5 preguntas de la fase |
| `while` | loop principal del juego |
| `break` / `continue` | salir si vidas == 0 |
| Funciones con parámetros y return | todo `juego.py` |
| Listas | `lista_trivia`, `preguntas_jugadas` |
| Diccionarios (key/value) | cada pregunta, estado del juego |
| Tuplas | opciones de cada pregunta, `FASES` |
| Acceso por índice | `lista_trivia[indice_actual]`, `opciones[correcta]` |
| Diseño modular | 5 archivos separados |
| Manejo de errores (try/except) | cargar imágenes (si falta el archivo) |

---

## 8. Cronograma sugerido (4–5 sesiones de trabajo)

| # | Sesión | Responsable principal |
|---|---|---|
| 1 | Estructura de archivos + `config.py` + las 50 preguntas en `preguntas.py` (lo más tedioso, hazlo primero). | Luis Enrique Mamani |
| 2 | `juego.py` completo + tests rápidos por consola sin GUI todavía. | Eduardo Cortez |
| 3 | `interfaz.py`: pantallas de bienvenida, intro de fase y pregunta (la principal). | Paul Gallardo |
| 4 | Pantallas de resumen y Salón de la Fama + pulido visual (hover, colores, fuentes). | Equipo completo |
| 5 | Buscar/recortar las imágenes de assets, pruebas finales, grabar video demo. | Equipo completo |

---

## 9. Decisiones que aún podrías reconsiderar

- **`random.sample` vs `random.shuffle`** → usar `sample` para no repetir.
- **Imágenes**: tamaño uniforme 200×200 px PNG con fondo recortado. Si no, el layout se rompe.
- **¿Sonidos?** No estaban en el brief, pero con `winsound` (Windows) o `pygame.mixer` agregas un "ding" en acierto y queda muy pro. Decidir si vale la pena.

---

## 10. Siguiente paso inmediato

Arrancar con `preguntas.py` (la base de 50). Es la tarea más tediosa y la que desbloquea al resto del equipo para empezar a integrar y probar.
