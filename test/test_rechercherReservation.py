import unittest
from pydantic import ValidationError
from DTO.reservationDTO import RechercherReservationDTO

class TestRechercherReservationDTO(unittest.TestCase):
    
    def test_numero_reservationDTO(self):
        for valeur in [None, "abc", 1.5, True, 0, -1]:
            with self.subTest(valeur=valeur):
                with self.assertRaises((ValidationError)):
                    RechercherReservationDTO(numero_reservation=valeur)