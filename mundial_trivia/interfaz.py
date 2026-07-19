# interfaz.py
# Toda la GUI tkinter: 5 pantallas (bienvenida, intro de fase,
# pregunta, resumen de fase, salon de la fama / game over).
# Mundial Trivia Challenge - UTP 2026

import os
import time
import tkinter as tk

import analitica
import config
import juego
from preguntas import cargar_preguntas

# PIL es opcional: si no esta instalado, se usa un placeholder dibujado.
try:
    from PIL import Image, ImageTk
    PIL_DISPONIBLE = True
except ImportError:
    PIL_DISPONIBLE = False


class App:
    """Controla la ventana y el flujo entre pantallas."""

    def __init__(self, root):
        self.root = root
        self.root.title(config.TITULO)
        self.root.geometry(f"{config.ANCHO}x{config.ALTO}")
        self.root.resizable(False, False)

        self.lista_trivia = cargar_preguntas()
        juego.validar_banco_preguntas(self.lista_trivia)
        self.estado = None
        self.preguntas_fase = []     # preguntas de la fase en curso
        self.indice_pregunta = 0     # cual de las 5 va
        self.respondiendo = False    # bloquea doble click durante feedback
        self._imagen_actual = None   # referencia viva (tkinter la necesita)
        self.inicio_pregunta = 0.0
        self._tarea_siguiente = None

        self.pantalla_bienvenida()

    # ---------- utilidades ----------

    def limpiar(self):
        """Borra todos los widgets de la ventana."""
        for widget in self.root.winfo_children():
            widget.destroy()

    def fondo(self):
        """Canvas con degradado azul + lineas de cancha. Devuelve el canvas."""
        canvas = tk.Canvas(self.root, width=config.ANCHO, height=config.ALTO,
                           highlightthickness=0)
        canvas.pack(fill="both", expand=True)
        # degradado vertical simple por franjas
        pasos = 40
        for i in range(pasos):
            f = i / pasos
            r = int(0x0f + (0x1e - 0x0f) * f)
            g = int(0x25 + (0x3a - 0x25) * f)
            b = int(0x57 + (0x8a - 0x57) * f)
            color = f"#{r:02x}{g:02x}{b:02x}"
            y0 = int(config.ALTO * i / pasos)
            y1 = int(config.ALTO * (i + 1) / pasos)
            canvas.create_rectangle(0, y0, config.ANCHO, y1,
                                    fill=color, outline=color)
        # lineas de cancha sutiles
        cx = config.ANCHO // 2
        canvas.create_oval(cx - 90, config.ALTO - 90, cx + 90, config.ALTO + 90,
                           outline="#3b82f6", width=2)
        canvas.create_line(0, config.ALTO - 1, config.ANCHO, config.ALTO - 1,
                           fill="#3b82f6", width=2)
        return canvas

    def boton(self, parent, texto, comando, color=None, ancho=24):
        """Boton estilizado con efecto hover."""
        base = color or config.COLOR_BOTON
        btn = tk.Button(parent, text=texto, command=comando,
                        font=config.FUENTE_OPCION, width=ancho,
                        bg=base, fg=config.COLOR_TEXTO_CLARO,
                        activebackground=config.COLOR_BOTON_HOVER,
                        activeforeground=config.COLOR_TEXTO_CLARO,
                        relief="flat", cursor="hand2", pady=10)
        btn.bind("<Enter>", lambda e: btn.config(bg=config.COLOR_BOTON_HOVER)
                 if btn["state"] == "normal" else None)
        btn.bind("<Leave>", lambda e: btn.config(bg=base)
                 if btn["state"] == "normal" else None)
        return btn

    def cargar_imagen(self, ruta):
        """Carga una imagen ajustada a TAM_IMAGEN.
        Si falta el archivo o PIL no esta, devuelve None (try/except del silabo)."""
        if not ruta:
            return None
        ruta_abs = os.path.join(os.path.dirname(__file__), ruta)
        try:
            if PIL_DISPONIBLE:
                img = Image.open(ruta_abs)
                img.thumbnail(config.TAM_IMAGEN)
                return ImageTk.PhotoImage(img)
            else:
                return tk.PhotoImage(file=ruta_abs)
        except Exception:
            return None  # la GUI mostrara un placeholder

    def hud_vidas(self, vidas):
        """Texto de corazones segun vidas restantes."""
        return "❤️" * vidas + "🖤" * (config.VIDAS_INICIALES - vidas)

    # ---------- pantalla 1: bienvenida ----------

    def pantalla_bienvenida(self):
        self.limpiar()
        canvas = self.fondo()

        canvas.create_text(config.ANCHO // 2, 120, text="⚽ MUNDIAL ⚽",
                           font=config.FUENTE_TITULO, fill=config.COLOR_DORADO)
        canvas.create_text(config.ANCHO // 2, 175, text="PROYECTO FINAL UTP",
                           font=config.FUENTE_TITULO, fill=config.COLOR_TEXTO_CLARO)
        canvas.create_text(config.ANCHO // 2, 240,
                           text="5 fases · 3 vidas · 25 preguntas · ¿Llegarás al Salón de la Fama?",
                           font=config.FUENTE_NORMAL, fill="#cbd5e1")

        canvas.create_text(config.ANCHO // 2, 300, text="Escribe tu nombre:",
                           font=config.FUENTE_SUBTITULO, fill=config.COLOR_TEXTO_CLARO)

        entry = tk.Entry(self.root, font=config.FUENTE_SUBTITULO,
                         justify="center", width=22)
        canvas.create_window(config.ANCHO // 2, 350, window=entry)
        entry.focus_set()

        aviso = canvas.create_text(config.ANCHO // 2, 390, text="",
                                   font=config.FUENTE_NORMAL, fill=config.COLOR_FALLO)

        def comenzar():
            try:
                nombre = juego.validar_nombre(entry.get())
            except ValueError as error:
                canvas.itemconfig(aviso, text=f"⚠ {error}")
                return
            if self.estado is None:
                self.estado = juego.nuevo_estado(nombre)
            else:
                self.estado = juego.reiniciar_para_nueva_partida(self.estado, nombre)
            self.pantalla_intro_fase()

        btn = self.boton(self.root, "🏆  JUGAR", comenzar)
        canvas.create_window(config.ANCHO // 2, 450, window=btn)
        entry.bind("<Return>", lambda e: comenzar())

    # ---------- pantalla 2: intro de fase ----------

    def pantalla_intro_fase(self):
        self.limpiar()
        canvas = self.fondo()
        fase = juego.fase_actual(self.estado)

        canvas.create_text(config.ANCHO // 2, 150, text=f"🏆 {fase['nombre'].upper()}",
                           font=config.FUENTE_TITULO, fill=config.COLOR_DORADO)
        canvas.create_text(config.ANCHO // 2, 230,
                           text=f"Vidas: {self.hud_vidas(self.estado['vidas'])}     "
                                f"Puntaje: ⭐ {self.estado['puntaje']}",
                           font=config.FUENTE_SUBTITULO, fill=config.COLOR_TEXTO_CLARO)
        canvas.create_text(config.ANCHO // 2, 300,
                           text=f"{config.PREGUNTAS_POR_FASE} preguntas · "
                                f"+{fase['puntos']} puntos por acierto · "
                                f"dificultad: {fase['dificultad']}",
                           font=config.FUENTE_NORMAL, fill="#cbd5e1")

        def comenzar_fase():
            self.preguntas_fase = juego.seleccionar_preguntas(
                self.lista_trivia, fase["dificultad"],
                excluir=self.estado["preguntas_jugadas"])
            self.indice_pregunta = 0
            self.pantalla_pregunta()

        btn = self.boton(self.root, "⚽ Comenzar", comenzar_fase)
        canvas.create_window(config.ANCHO // 2, 400, window=btn)

    # ---------- pantalla 3: pregunta ----------

    def pantalla_pregunta(self):
        self.limpiar()
        canvas = self.fondo()
        fase = juego.fase_actual(self.estado)
        pregunta = self.preguntas_fase[self.indice_pregunta]
        self.respondiendo = False

        # header: fase, puntaje y vidas
        canvas.create_text(20, 25, anchor="w", text=fase["nombre"],
                           font=config.FUENTE_HUD, fill=config.COLOR_DORADO)
        canvas.create_text(config.ANCHO // 2, 25,
                           text=f"⭐ {self.estado['puntaje']}",
                           font=config.FUENTE_HUD, fill=config.COLOR_TEXTO_CLARO)
        canvas.create_text(config.ANCHO - 20, 25, anchor="e",
                           text=self.hud_vidas(self.estado["vidas"]),
                           font=config.FUENTE_HUD, fill=config.COLOR_TEXTO_CLARO)
        canvas.create_text(20, 50, anchor="w",
                           text=f"Pregunta {self.indice_pregunta + 1} de "
                                f"{len(self.preguntas_fase)}",
                           font=config.FUENTE_NORMAL, fill="#cbd5e1")

        # card central blanca
        card = tk.Frame(self.root, bg=config.COLOR_CARD)
        canvas.create_window(config.ANCHO // 2, 330, window=card,
                             width=920, height=500)

        tk.Label(card, text=pregunta["pregunta"], font=config.FUENTE_PREGUNTA,
                 bg=config.COLOR_CARD, fg=config.COLOR_TEXTO,
                 wraplength=860, justify="center").pack(pady=(18, 8))

        # imagen (o placeholder si falta)
        self._imagen_actual = self.cargar_imagen(pregunta["imagen"])
        if self._imagen_actual is not None:
            tk.Label(card, image=self._imagen_actual,
                     bg=config.COLOR_CARD).pack(pady=4)
        elif pregunta["imagen"]:
            tk.Label(card, text="🖼️ ⚽", font=(config.FUENTE, 60),
                     bg=config.COLOR_CARD).pack(pady=14)
        else:
            tk.Label(card, text="⚽", font=(config.FUENTE, 60),
                     bg=config.COLOR_CARD).pack(pady=14)

        # 4 opciones en grilla 2x2
        marco_opciones = tk.Frame(card, bg=config.COLOR_CARD)
        marco_opciones.pack(pady=10, fill="x", padx=30)
        letras = ("A", "B", "C", "D")
        self.botones_opcion = []
        for i, opcion in enumerate(pregunta["opciones"]):
            btn = self.boton(marco_opciones, f"{letras[i]})  {opcion}",
                             lambda i=i: self.responder(i), ancho=34)
            btn.grid(row=i // 2, column=i % 2, padx=8, pady=6, sticky="ew")
            self.botones_opcion.append(btn)
        marco_opciones.columnconfigure(0, weight=1)
        marco_opciones.columnconfigure(1, weight=1)
        self.inicio_pregunta = time.perf_counter()

    def responder(self, indice_elegido):
        """Valida la respuesta, pinta feedback verde/rojo y avanza."""
        if self.respondiendo:
            return
        self.respondiendo = True

        pregunta = self.preguntas_fase[self.indice_pregunta]
        fase = juego.fase_actual(self.estado)
        acierto = juego.validar_respuesta(pregunta, indice_elegido)
        tiempo_respuesta = time.perf_counter() - self.inicio_pregunta

        juego.actualizar_puntaje(self.estado, acierto, fase["puntos"])
        juego.registrar_respuesta(
            self.estado, pregunta, fase, acierto, tiempo_respuesta)

        # feedback visual: verde la correcta, rojo la elegida si fallo
        for i, btn in enumerate(self.botones_opcion):
            btn.config(state="disabled", disabledforeground="white")
            if i == pregunta["correcta"]:
                btn.config(bg=config.COLOR_ACIERTO)
            elif i == indice_elegido:
                btn.config(bg=config.COLOR_FALLO)

        self._tarea_siguiente = self.root.after(
            config.PAUSA_FEEDBACK, self.siguiente_pregunta)

    def siguiente_pregunta(self):
        self._tarea_siguiente = None
        self.indice_pregunta += 1
        if juego.fase_terminada(self.estado, self.indice_pregunta):
            self.terminar_fase()
        else:
            self.pantalla_pregunta()

    def terminar_fase(self):
        if self.estado["vidas"] > 0:
            juego.avanzar_fase(self.estado)
        if juego.juego_terminado(self.estado):
            juego.guardar_en_ranking(self.estado)
            self.pantalla_final()
        else:
            self.pantalla_resumen_fase()

    # ---------- pantalla 4: resumen de fase ----------

    def pantalla_resumen_fase(self):
        self.limpiar()
        canvas = self.fondo()
        siguiente = juego.fase_actual(self.estado)

        canvas.create_text(config.ANCHO // 2, 160, text="✅ ¡FASE SUPERADA!",
                           font=config.FUENTE_TITULO, fill=config.COLOR_ACIERTO)
        canvas.create_text(config.ANCHO // 2, 240,
                           text=f"¡Pasaste a {siguiente['nombre']}!",
                           font=config.FUENTE_SUBTITULO, fill=config.COLOR_TEXTO_CLARO)
        canvas.create_text(config.ANCHO // 2, 310,
                           text=f"Vidas: {self.hud_vidas(self.estado['vidas'])}     "
                                f"Puntaje: ⭐ {self.estado['puntaje']}",
                           font=config.FUENTE_SUBTITULO, fill=config.COLOR_TEXTO_CLARO)

        btn = self.boton(self.root, "Continuar ➡", self.pantalla_intro_fase)
        canvas.create_window(config.ANCHO // 2, 420, window=btn)

    # ---------- pantalla 5: salon de la fama / game over ----------

    def pantalla_final(self):
        self.limpiar()
        canvas = self.fondo()
        resultado = juego.clasificar_resultado(self.estado)
        self.estado["resultado"] = resultado
        resumen = analitica.procesar_historial(self.estado["historial_respuestas"])
        try:
            analitica.generar_reporte_partida(self.estado)
            mensaje_archivos = "Reporte y gráficos guardados en la carpeta resultados"
        except OSError:
            mensaje_archivos = "No se pudieron guardar los archivos de resultados"

        if resultado == "salon_fama":
            # confeti simple con ovalos de colores
            import random as rnd
            colores = (config.COLOR_DORADO, config.COLOR_ACIERTO,
                       config.COLOR_BOTON_HOVER, config.COLOR_FALLO, "#ffffff")
            for _ in range(80):
                x = rnd.randint(0, config.ANCHO)
                y = rnd.randint(0, config.ALTO)
                r = rnd.randint(3, 7)
                canvas.create_oval(x, y, x + r, y + r,
                                   fill=rnd.choice(colores), outline="")
            canvas.create_text(config.ANCHO // 2, 100, text="🏆 SALÓN DE LA FAMA 🏆",
                               font=config.FUENTE_TITULO, fill=config.COLOR_DORADO)
            canvas.create_text(config.ANCHO // 2, 165,
                               text=f"¡{self.estado['jugador']}, eres CAMPEÓN DEL MUNDO!",
                               font=config.FUENTE_SUBTITULO,
                               fill=config.COLOR_TEXTO_CLARO)
        else:
            canvas.create_text(config.ANCHO // 2, 100, text="❌ GAME OVER",
                               font=config.FUENTE_TITULO, fill=config.COLOR_FALLO)
            canvas.create_text(config.ANCHO // 2, 165,
                               text=f"{self.estado['jugador']}, te quedaste sin vidas.",
                               font=config.FUENTE_SUBTITULO,
                               fill=config.COLOR_TEXTO_CLARO)

        canvas.create_text(config.ANCHO // 2, 225,
                            text=f"Puntaje final: ⭐ {self.estado['puntaje']}",
                            font=config.FUENTE_SUBTITULO, fill=config.COLOR_DORADO)
        canvas.create_text(
            config.ANCHO // 2, 265,
            text=f"Rendimiento: {resumen['clasificacion']} "
                 f"({resumen['porcentaje_aciertos']:.1f}% de aciertos)",
            font=config.FUENTE_HUD, fill=config.COLOR_TEXTO_CLARO)
        canvas.create_text(config.ANCHO // 2, 292, text=mensaje_archivos,
                           font=(config.FUENTE, 10), fill="#cbd5e1")

        # ranking de la sesion (tuplas nombre, puntaje)
        canvas.create_text(config.ANCHO // 2, 320, text="— Ranking de la sesión —",
                            font=config.FUENTE_HUD, fill="#cbd5e1")
        medallas = ("🥇", "🥈", "🥉")
        y = 350
        for pos, (nombre, puntaje) in enumerate(self.estado["ranking_sesion"][:5]):
            icono = medallas[pos] if pos < len(medallas) else f"{pos + 1}."
            canvas.create_text(config.ANCHO // 2, y,
                               text=f"{icono}  {nombre} — {puntaje} pts",
                               font=config.FUENTE_NORMAL,
                               fill=config.COLOR_TEXTO_CLARO)
            y += 30

        btn = self.boton(self.root, "🔁 Jugar de nuevo", self.pantalla_bienvenida)
        canvas.create_window(config.ANCHO // 2 - 130, 530, window=btn, width=230)
        btn_salir = self.boton(self.root, "Salir", self.root.destroy,
                               color="#475569")
        canvas.create_window(config.ANCHO // 2 + 130, 530, window=btn_salir, width=230)


def iniciar():
    """Crea la ventana principal y arranca el loop de eventos."""
    root = tk.Tk()
    App(root)
    root.mainloop()
