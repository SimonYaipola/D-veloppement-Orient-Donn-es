import urllib
import unittest
import modele 
from datetime import datetime
from modele import chambre
from modele.chambre import Reservation
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, select

import logging
logging.basicConfig()
logging.getLogger("sqlalchemy.engine").setLevel (logging.INFO)

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


    
class test_reservation(unittest.TestCase):
    def test_getReservationParId(self):
        with Session(engine) as session:
            stmt = select(chambre.Reservation).where(chambre.Reservation.id_reservation == '88B53AB2-E147-4626-8BB9-075EA6D810C8')
            Reservation = session.execute(stmt).scalar_one()
            self.assertEqual(Reservation.id_reservation, '88B53AB2-E147-4626-8BB9-075EA6D810C8')
            datetime_fin_Base = '2026-09-15 00:00:00.000'
            datetime_debut_Base = '2026-09-20 00:00:00.000'
            datetime_fin_Stripped = datetime.strptime(datetime_fin_Base, '%Y-%m-%d %H:%M:%S.%f')
            datetime_debut_Stripped = datetime.strptime(datetime_debut_Base, '%Y-%m-%d %H:%M:%S.%f')
            self.assertEqual(Reservation.date_fin_reservation, datetime_fin_Stripped)
            self.assertEqual(Reservation.date_debut_reservation, datetime_debut_Stripped)
            self.assertEqual(Reservation.prix_jour, 333.33)
            self.assertEqual(Reservation.info_reservation, 'Pas de ménage')
            self.assertEqual(Reservation.client.id_client, 'EC50134D-372B-4DFD-9627-02BE06BA6BD6')
            self.assertEqual(Reservation.chambre.id_chambre, '1276E513-BB05-41D9-B22E-0073772A006A')