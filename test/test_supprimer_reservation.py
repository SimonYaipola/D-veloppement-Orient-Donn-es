import unittest
from unittest.mock import Mock, patch
from modele.table import Reservation
from metier.reservationMetier import supprimerReservation

class test_supprimerReservation(unittest.TestCase):
    @patch("metier.reservationMetier.Session")
    def test_supprimerReservation(self, mock_session):
        session = mock_session.return_value.__enter__.return_value

        reservation_existante = Reservation(numero_reservation=1)
        session.execute.return_value.scalars.return_value.one.return_value = reservation_existante

        supprimerReservation(1)

        session.delete.assert_called_once_with(reservation_existante)
        session.commit.assert_called_once()