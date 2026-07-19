import sys
import tempfile
import unittest
from pathlib import Path


RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "mundial_trivia"))

import analitica
import juego
from preguntas import cargar_preguntas


def crear_estado_prueba():
    estado = juego.nuevo_estado("Analista")
    preguntas = cargar_preguntas()
    fase = juego.fase_actual(estado)
    for pregunta, acierto, tiempo in (
            (preguntas[0], True, 3.0),
            (preguntas[1], False, 5.0)):
        juego.actualizar_puntaje(estado, acierto, fase["puntos"])
        juego.registrar_respuesta(estado, pregunta, fase, acierto, tiempo)
    estado["resultado"] = "derrota"
    return estado


class AnaliticaTests(unittest.TestCase):
    def test_crea_matriz_y_procesa_indicadores(self):
        estado = crear_estado_prueba()
        matriz = analitica.crear_matriz(estado["historial_respuestas"])
        resumen = analitica.procesar_historial(estado["historial_respuestas"])

        self.assertEqual(matriz.shape, (2, len(analitica.COLUMNAS_MATRIZ)))
        self.assertEqual(resumen["aciertos"], 1)
        self.assertEqual(resumen["errores"], 1)
        self.assertEqual(resumen["porcentaje_aciertos"], 50.0)
        self.assertEqual(resumen["clasificacion"], "En proceso")

    def test_clasifica_limites(self):
        self.assertEqual(analitica.clasificar_desempeno(80), "Excelente")
        self.assertEqual(analitica.clasificar_desempeno(60), "Bueno")
        self.assertEqual(analitica.clasificar_desempeno(40), "En proceso")
        self.assertEqual(analitica.clasificar_desempeno(39.9), "Necesita refuerzo")

    def test_exporta_reporte_matriz_y_cuatro_graficos(self):
        estado = crear_estado_prueba()
        with tempfile.TemporaryDirectory() as temporal:
            rutas = analitica.generar_reporte_partida(estado, temporal)
            self.assertTrue(rutas["historial"].exists())
            self.assertTrue(rutas["matriz"].exists())
            self.assertTrue(rutas["reporte"].exists())
            self.assertEqual(len(rutas["graficos"]), 4)
            self.assertTrue(all(ruta.exists() for ruta in rutas["graficos"]))


if __name__ == "__main__":
    unittest.main()
