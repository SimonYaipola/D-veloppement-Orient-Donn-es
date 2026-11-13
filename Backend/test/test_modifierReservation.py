import unittest
import urllib
from datetime import date
from sqlalchemy.orm import Session
from sqlalchemy import UUID, select
from sqlalchemy import text
from uuid import UUID
from modele.chambre import Chambre
from modele.typeChambre import TypeChambre
from modele.reservation import Reservation
from modele.client import Client
from metier.reservationMetier import modifierReservation, ReservationDTO
from sqlalchemy.orm import Session
from engine.connexion import engine

with Session(engine) as session:

    class test_modification_Chambre(unittest.TestCase):
        def test_modifierReservation(self):
            with Session(engine) as session:
                numReservation = 1
                reservationAModifier = session.execute(select(Reservation).where(Reservation.numero_reservation == numReservation)).scalars().first()


                self.assertIsNotNone(reservationAModifier, "La réservation" + str(numReservation) + " n'existe pas")

                DTO = ReservationDTO(reservationAModifier)

                DTO.date_debut_reservation = date(2026, 9, 15)
                DTO.date_fin_reservation = date(2026, 9, 20)
                DTO.prix_jour = 333.33
                DTO.info_reservation = "Test de modification"

                reservationModifiee = modifierReservation(DTO)

                self.assertEqual(reservationModifiee.numero_reservation, numReservation)
                self.assertEqual(reservationModifiee.prix_jour, 333.33)
                self.assertEqual(reservationModifiee.info_reservation, "Test de modification")
