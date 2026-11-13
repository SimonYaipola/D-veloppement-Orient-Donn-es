import logging
import unittest
from datetime import date, datetime
from unittest.mock import patch
from uuid import UUID

from pydantic import ValidationError
from DTO.reservationDTO import ReservationCreerDTO
from modele.reservation import Reservation
from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.orm import Session
from engine.connexion import engine

logging.basicConfig()
logging.getLogger("sqlalchemy.engine").setLevel (logging.INFO)

with Session(engine) as session:

    # fausses variables pour les mock tests
    ID_CLIENT = "EC50134D-372B-4DFD-9627-02BE06BA6BD6"
    ID_CHAMBRE = "1276E513-BB05-41D9-B22E-0073772A006A"
    
    datetime_fin_Base = '2026-09-20 00:00:00.000'
    datetime_debut_Base = '2026-09-15 00:00:00.000'
    datetime_fin_Stripped = datetime.strptime(datetime_fin_Base, '%Y-%m-%d %H:%M:%S.%f')
    datetime_debut_Stripped = datetime.strptime(datetime_debut_Base, '%Y-%m-%d %H:%M:%S.%f')
    
    class test_reservation(unittest.TestCase):
        def test_getReservationParId(self):
            stmt = select(Reservation).where(Reservation.id_reservation == '88B53AB2-E147-4626-8BB9-075EA6D810C8')
            reservation = session.execute(stmt).scalar_one()
            self.assertEqual(reservation.id_reservation, '88B53AB2-E147-4626-8BB9-075EA6D810C8')
            self.assertEqual(reservation.date_fin_reservation, datetime_fin_Stripped)
            self.assertEqual(reservation.date_debut_reservation, datetime_debut_Stripped)
            self.assertEqual(reservation.prix_jour, 333.33)
            self.assertEqual(reservation.info_reservation, 'Test de modification')
            self.assertEqual(reservation.client.id_client, 'EC50134D-372B-4DFD-9627-02BE06BA6BD6')
            self.assertEqual(reservation.chambre.id_chambre, '1276E513-BB05-41D9-B22E-0073772A006A')

        @patch("metier.reservationMetier.Session")
        def test_reservationValiderPrix(self, mockSession):
            with self.assertRaises(ValidationError):
                DTO = ReservationCreerDTO(
                        date_debut_reservation=date(2026, 9, 20),
                        date_fin_reservation=date(2026, 9, 25),
                        prix_jour=-100.00,
                        info_reservation="Mock test de validation de prix",
                        id_client=UUID(ID_CLIENT),
                        id_chambre=UUID(ID_CHAMBRE),
                    )

        @patch("metier.reservationMetier.Session")
        def test_reservationValiderDates(self, mockSession):
            with self.assertRaises(ValidationError):
                DTO = ReservationCreerDTO(
                        date_debut_reservation=date(2026, 9, 25),
                        date_fin_reservation=date(2026, 9, 20),
                        prix_jour=200.00,
                        info_reservation="Mock test de validation des dates",
                        id_client=UUID(ID_CLIENT),
                        id_chambre=UUID(ID_CHAMBRE),
                    )