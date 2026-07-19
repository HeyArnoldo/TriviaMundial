import random
import sys
import unittest
from pathlib import Path


RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "mundial_trivia"))

import juego
from preguntas import cargar_preguntas


class JuegoTests(unittest.TestCase):
    def setUp(self):
        self.preguntas = cargar_preguntas()

    def test_valida_y_normaliza_nombre(self):
        self.assertEqual(juego.validar_nombre("  Luis   Mamani  "), "Luis Mamani")
        with self.assertRaises(ValueError):
            juego.validar_nombre("1234")

    def test_valida_banco_de_preguntas(self):
        self.assertTrue(juego.validar_banco_preguntas(self.preguntas))

        preguntas_invalidas = [dict(self.preguntas[0]), dict(self.preguntas[1])]
        preguntas_invalidas[1]["id"] = preguntas_invalidas[0]["id"]
        with self.assertRaises(ValueError):
            juego.validar_banco_preguntas(preguntas_invalidas)

    def test_seleccion_reproducible_y_sin_excluidos(self):
        seleccion = juego.seleccionar_preguntas(
            self.preguntas, "facil", n=5, excluir=[1, 2], rng=random.Random(42))
        self.assertEqual(len(seleccion), 5)
        self.assertNotIn(1, [pregunta["id"] for pregunta in seleccion])
        self.assertNotIn(2, [pregunta["id"] for pregunta in seleccion])

    def test_actualiza_y_registra_respuesta(self):
        estado = juego.nuevo_estado("Tester")
        pregunta = self.preguntas[0]
        fase = juego.fase_actual(estado)

        juego.actualizar_puntaje(estado, True, fase["puntos"])
        juego.registrar_respuesta(estado, pregunta, fase, True, 3.5)

        self.assertEqual(estado["puntaje"], 10)
        self.assertEqual(estado["historial_respuestas"][0]["pregunta_id"], 1)
        self.assertEqual(estado["historial_respuestas"][0]["tiempo_respuesta"], 3.5)

    def test_no_permite_registrar_dos_veces_la_misma_pregunta(self):
        estado = juego.nuevo_estado("Tester")
        pregunta = self.preguntas[0]
        fase = juego.fase_actual(estado)
        juego.registrar_respuesta(estado, pregunta, fase, False)
        with self.assertRaises(ValueError):
            juego.registrar_respuesta(estado, pregunta, fase, False)


if __name__ == "__main__":
    unittest.main()
