import unittest
import logging
from modele.chambre import Chambre
from engine.connexion import engine
from sqlalchemy.orm import Session
from sqlalchemy import select
logging.basicConfig()
logging.getLogger("sqlalchemy.engine").setLevel (logging.INFO)

with Session(engine) as session:

    class test_chambre(unittest.TestCase):
        def test_getChambreParNumero(self):
            with Session(engine) as session:
                stmt = select(Chambre).where(Chambre.numero_chambre == 243)
                chambre = session.execute(stmt).scalar_one()
                self.assertEqual(chambre.numero_chambre, 243)
                self.assertIsNone (chambre.autre_informations)
                self.assertTrue(chambre.disponible_reservation)
                self.assertEqual(chambre.id_chambre, 'E5872679-D5AB-4A4D-8090-C0AFCC6D47C0')
                self.assertEqual(chambre.type_chambre.nom_type, 'VIP')
                self.assertEqual(chambre.type_chambre.prix_plancher, 400.00)
                self.assertEqual(chambre.type_chambre.prix_plafond, 1220.00)
                self.assertEqual(chambre.type_chambre.description_chambre, 'Pour le monde qui on trops dargent')
                self.assertEqual(chambre.type_chambre.id_type_chambre, '12633C57-4790-4516-BFC5-BD0E5A3C920C')

                                    
