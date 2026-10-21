import unittest
from metier.reservationMetier import rechercherReservation

class test_rechercheReservation(unittest.TestCase):
    def test_numero_null(self):
        with self.assertRaises(ValueError):
            rechercherReservation(None)

    def test_numero_pas_un_entier(self):
        with self.assertRaises(TypeError):
            rechercherReservation("abc")

    def test_numero_decimal(self):
        with self.assertRaises(TypeError):
            rechercherReservation(1.5)

    def test_numero_booleen(self):
        with self.assertRaises(TypeError):
            rechercherReservation(True)

    def test_numero_zero(self):
        with self.assertRaises(ValueError):
            rechercherReservation(0)

    def test_numero_negatif(self):
        with self.assertRaises(ValueError):
            rechercherReservation(-1)
