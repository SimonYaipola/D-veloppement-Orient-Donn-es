import unittest
from pydantic import ValidationError
from metier.reservationMetier import rechercherReservation

class TestRechercherReservationDTO(unittest.TestCase):
    
    def test_numero_null(self):
        with self.assertRaises(ValueError):
            rechercherReservation(None)

    def test_numero_pas_un_entier(self):
        with self.assertRaises(TypeError):
            rechercherReservation("1")

    def test_numero_negatif(self):
        with self.assertRaises(ValueError):
            rechercherReservation(-1)

    def test_numero_zero(self):
        with self.assertRaises(ValueError):
            rechercherReservation(0)

    def test_numero_booleen(self):
        with self.assertRaises(TypeError):
            rechercherReservation(True)
