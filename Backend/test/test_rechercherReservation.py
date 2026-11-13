import unittest
from pydantic import ValidationError
from metier.reservationMetier import rechercherReservation

class TestRechercherReservationDTO(unittest.TestCase):
    
    def test_numero_null(self):
        with self.assertRaises(ValueError):
            rechercherReservation(no_reservation=None, no_chambre=490)

    def test_numero_pas_un_entier(self):
        with self.assertRaises(TypeError):
            rechercherReservation(no_reservation="1")

    def test_numero_negatif(self):
        with self.assertRaises(ValueError):
            rechercherReservation(no_reservation=-1, no_chambre=490)

    def test_numero_zero(self):
        with self.assertRaises(ValueError):
            rechercherReservation(no_reservation=0, no_chambre=490)

    def test_numero_booleen(self):
        with self.assertRaises(TypeError):
            rechercherReservation(no_reservation=True)

# --------------------------------------------------------------------
# -------------------------- Chambre ---------------------------------
# --------------------------------------------------------------------

    def test_numero_null_chambre(self):
        with self.assertRaises(ValueError):
            rechercherReservation(no_reservation=1, no_chambre=None)

    def test_numero_pas_un_entier_chambre(self):
        with self.assertRaises(TypeError):
            rechercherReservation(no_chambre="1")

    def test_numero_negatif_chambre(self):
        with self.assertRaises(ValueError):
            rechercherReservation(no_reservation=1, no_chambre=-1)

    def test_numero_zero_chambre(self):
        with self.assertRaises(ValueError):
            rechercherReservation(no_reservation=1, no_chambre=0)

    def test_numero_booleen_chambre(self):
        with self.assertRaises(TypeError):
            rechercherReservation(no_chambre=True)
