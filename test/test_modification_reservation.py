from datetime import date
import unittest
from sqlalchemy.orm import Session
from sqlalchemy import UUID, create_engine, select
from sqlalchemy import text
import urllib
from uuid import UUID
from modele.table import Chambre, Typechambre, Client, Reservation
from metier.reservationMetier import modifierReservation, ReservationDTO

server = '158.69.208.232,1433'
database = 'Hotels'
username = 'sa'
password = 'Automne,2026'
params = urllib.parse.quote_plus(
    f"DRIVER={{ODBC Driver 17 for SQL Server}};"
    f"SERVER={server};"
    f"DATABASE={database};"
    f"UID={username};"
    f"PWD={password};"
)
engine = create_engine(f"mssql+pyodbc:///?odbc_connect={params}")

with engine.connect() as connection:
    print("Connection réussie")

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
