import sys
import tempfile
import unittest
from pathlib import Path


RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "mundial_trivia"))

import simulador


class SimuladorTests(unittest.TestCase):
    def test_simulacion_es_reproducible(self):
        primera = simulador.simular_partidas(3, semilla=7)
        segunda = simulador.simular_partidas(3, semilla=7)
        self.assertEqual(
            [estado["puntaje"] for estado in primera],
            [estado["puntaje"] for estado in segunda],
        )

    def test_exporta_archivos_de_simulacion(self):
        estados = simulador.simular_partidas(3, semilla=10)
        with tempfile.TemporaryDirectory() as temporal:
            rutas = simulador.exportar_simulacion(estados, temporal)
            self.assertEqual(len(rutas), 4)
            self.assertTrue(all(ruta.exists() for ruta in rutas))

    def test_rechaza_cantidad_invalida(self):
        with self.assertRaises(ValueError):
            simulador.simular_partidas(0)


if __name__ == "__main__":
    unittest.main()
