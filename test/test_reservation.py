import logging
import unittest
from datetime import datetime
from modele.reservation import Reservation
from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.orm import Session
from engine.connexion import engine

logging.basicConfig()
logging.getLogger("sqlalchemy.engine").setLevel (logging.INFO)

with Session(engine) as session:

    
    class test_reservation(unittest.TestCase):
        def test_getReservationParId(self):
            with Session(engine) as session:
                stmt = select(Reservation).where(Reservation.id_reservation == '88B53AB2-E147-4626-8BB9-075EA6D810C8')
                reservation = session.execute(stmt).scalar_one()
                self.assertEqual(reservation.id_reservation, '88B53AB2-E147-4626-8BB9-075EA6D810C8')
                datetime_fin_Base = '2026-09-20 00:00:00.000'
                datetime_debut_Base = '2026-09-15 00:00:00.000'
                datetime_fin_Stripped = datetime.strptime(datetime_fin_Base, '%Y-%m-%d %H:%M:%S.%f')
                datetime_debut_Stripped = datetime.strptime(datetime_debut_Base, '%Y-%m-%d %H:%M:%S.%f')
                self.assertEqual(reservation.date_fin_reservation, datetime_fin_Stripped)
                self.assertEqual(reservation.date_debut_reservation, datetime_debut_Stripped)
                self.assertEqual(reservation.prix_jour, 333.33)
                self.assertEqual(reservation.info_reservation, 'Test de modification')
                self.assertEqual(reservation.client.id_client, 'EC50134D-372B-4DFD-9627-02BE06BA6BD6')
                self.assertEqual(reservation.chambre.id_chambre, '1276E513-BB05-41D9-B22E-0073772A006A')
