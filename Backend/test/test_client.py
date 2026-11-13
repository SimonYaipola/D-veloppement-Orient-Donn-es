import unittest
import logging
from modele.client import Client
from sqlalchemy.orm import Session
from sqlalchemy import select
from engine.connexion import engine
logging.basicConfig()
logging.getLogger("sqlalchemy.engine").setLevel (logging.INFO)

with Session(engine) as session:

    class test_client(unittest.TestCase):
        def test_Unclient(self):
            with Session(engine) as session:
                stmt = select(Client).where(Client.id_client == 'EC50134D-372B-4DFD-9627-02BE06BA6BD6')
                client = session.execute(stmt).scalar_one()
                self.assertEqual(client.prenom, 'Pier-Davide')
                self.assertEqual(client.nom, 'Morel')
                self.assertEqual(client.adresse, '80 Bd de Gaspé, QC')
                self.assertEqual(client.mobile, '4183681534')
                self.assertEqual(client.mot_de_passe, 'PDestSolide!')
