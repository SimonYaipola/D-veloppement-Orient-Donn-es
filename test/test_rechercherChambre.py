import unittest
import urllib
from metier.chambreMetier import getChambreParNumero

class test_getChambreParNumero(unittest.TestCase):

    def test_numero_null(self):
        with self.assertRaises(ValueError):
            getChambreParNumero(None)

    def test_numero_pas_un_entier(self):
        with self.assertRaises(TypeError):
            getChambreParNumero("501")

    def test_numero_negatif(self):
        with self.assertRaises(ValueError):
            getChambreParNumero(-1)

    def test_numero_zero(self):
        with self.assertRaises(ValueError):
            getChambreParNumero(0)

    def test_numero_booleen(self):
        with self.assertRaises(TypeError):
            getChambreParNumero(True)