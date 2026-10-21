import unittest
import urllib
from modele.client import Client
from metier.clientMetier import creerClient, ClientDTO
from sqlalchemy.orm import Session
from engine.connexion import engine
from sqlalchemy import create_engine, delete
from uuid import UUID

with Session(engine) as session:

    class test_creerClient(unittest.TestCase):
        def test_creerClient(self):
            clientDTO = ClientDTO(
                Client(
                    nom='Peletier',
                    prenom='Boss',
                    adresse='246 rue Mgr Leblanc, Gaspé, QC',
                    mot_de_passe='Noah:3',
                    mobile='4186667777',
                    id_client='3F2B8C1A-7D4E-4B9A-9C6E-1A2B3C4D5E6F'
                )
            )

            clientDTOCree = creerClient(clientDTO)

            self.assertEqual(clientDTOCree.nom_client, 'Peletier')
            self.assertEqual(clientDTOCree.prenom_client, 'Boss')
            self.assertEqual(clientDTOCree.adresse_client, '246 rue Mgr Leblanc, Gaspé, QC')
            self.assertEqual(clientDTOCree.mot_de_passe_client, 'Noah:3')
            self.assertEqual(clientDTOCree.mobile_client, '4186667777')
            self.assertEqual(clientDTOCree.id_client, UUID('3F2B8C1A-7D4E-4B9A-9C6E-1A2B3C4D5E6F'))

            with Session(engine) as session:
                stmt = delete(Client).where(Client.id_client == '3F2B8C1A-7D4E-4B9A-9C6E-1A2B3C4D5E6F')
                session.execute(stmt)
                session.commit()